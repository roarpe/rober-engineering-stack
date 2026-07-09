"""Telemetry validation pipeline implementing the ICD contract."""

from __future__ import annotations

import math
from typing import Any, Dict, Optional

from .models import (
    ContractValidation,
    QualityCode,
    Status,
    TelemetryFrame,
    ValidationClassification,
    ValidationResult,
)
from .utils.clock import Clock, SystemClock

TEMPERATURE_RANGE = (0.0, 120.0)
VIBRATION_RANGE = (0.0, 50.0)
MAX_TIMESTAMP_SKEW_MS = 5000
CADENCE_TOLERANCE_MS = 200

TEMP_MINOR_BAND = (90.0, 100.0)
TEMP_MAJOR_THRESHOLD = 100.0
VIB_MINOR_BAND = (30.0, 40.0)
VIB_MAJOR_THRESHOLD = 40.0


class Validator:
    def __init__(self, clock: Clock = SystemClock()) -> None:
        self.clock = clock
        self._last_timestamp: Optional[int] = None
        self._last_cycle: Optional[int] = None
        self._maintenance_active = False

    def validate(self, raw_frame: Dict[str, Any]) -> ValidationResult:
        frame, rejection = self._build_frame(raw_frame)
        if rejection is not None:
            return ValidationResult(
                frame=None,
                is_valid=False,
                reason=rejection[0],
                violations=[rejection[0]],
                classification=ValidationClassification.INVALID,
            )

        assert frame is not None

        if frame.quality_code == QualityCode.NO_DATA:
            if any(v is not None for v in (frame.temperature_c, frame.vibration_mm_s, frame.cycle_count)):
                return ValidationResult(
                    frame=None,
                    is_valid=False,
                    reason="NO_DATA frames must not include measurements",
                    violations=["NO_DATA frames must not include measurements"],
                    classification=ValidationClassification.INVALID,
                )
            classification = ValidationClassification.NO_DATA
        else:
            range_reason = self._validate_ranges(frame)
            if range_reason is not None:
                return ValidationResult(
                    frame=frame,
                    is_valid=False,
                    reason=range_reason,
                    violations=[range_reason],
                    classification=ValidationClassification.INVALID,
                )
            classification = self._classify_measurements(frame)

        monotonic_reason = self._validate_monotonicity(frame)
        if monotonic_reason is not None:
            return ValidationResult(
                frame=frame,
                is_valid=False,
                reason=monotonic_reason,
                violations=[monotonic_reason],
                classification=ValidationClassification.INVALID,
            )

        skew_reason = self._validate_timestamp_skew(frame)
        if skew_reason is not None:
            return ValidationResult(
                frame=frame,
                is_valid=False,
                reason=skew_reason,
                violations=[skew_reason],
                classification=ValidationClassification.INVALID,
            )

        return ValidationResult(
            frame=frame,
            is_valid=classification in {ValidationClassification.VALID, ValidationClassification.ANOMALOUS},
            reason=None,
            violations=[],
            classification=classification,
        )

    def _build_frame(self, raw_frame: Dict[str, Any]) -> tuple[Optional[TelemetryFrame], Optional[tuple[str, ContractValidation]]]:
        required = ["frame_id", "timestamp_utc", "status", "quality_code"]
        missing = [f for f in required if f not in raw_frame]
        if missing:
            return None, (f"Missing required fields: {','.join(missing)}", ContractValidation.REJECTED_SCHEMA)

        try:
            frame_id = str(raw_frame["frame_id"])
            timestamp = int(raw_frame["timestamp_utc"])
            status = Status(str(raw_frame["status"]))
            quality_code = QualityCode(str(raw_frame["quality_code"]))
        except (ValueError, KeyError, TypeError) as exc:
            return None, (f"Schema violation: {exc}", ContractValidation.REJECTED_SCHEMA)

        try:
            temperature = self._optional_float(raw_frame.get("temperature_c"))
            vibration = self._optional_float(raw_frame.get("vibration_mm_s"))
            cycle_count = self._optional_int(raw_frame.get("cycle_count"))
        except ValueError as exc:
            return None, (str(exc), ContractValidation.REJECTED_SCHEMA)

        if quality_code != QualityCode.NO_DATA:
            if temperature is None or vibration is None or cycle_count is None:
                return None, ("Missing measurement fields for non-NO_DATA frame", ContractValidation.REJECTED_SCHEMA)

        notes = raw_frame.get("diagnostic_notes")
        frame = TelemetryFrame(
            frame_id=frame_id,
            timestamp_utc=timestamp,
            temperature_c=temperature,
            vibration_mm_s=vibration,
            cycle_count=cycle_count,
            status=status,
            quality_code=quality_code,
            diagnostic_notes=str(notes) if notes is not None else None,
        )
        return frame, None

    @staticmethod
    def _optional_float(value: Any) -> Optional[float]:
        if value is None:
            return None
        if isinstance(value, (int, float)):
            result = float(value)
            if math.isnan(result) or math.isinf(result):
                raise ValueError("Non-finite numeric value")
            return result
        raise ValueError("Non-numeric measurement field")

    @staticmethod
    def _optional_int(value: Any) -> Optional[int]:
        if value is None:
            return None
        if isinstance(value, int) and not isinstance(value, bool):
            return value
        raise ValueError("Non-integer cycle_count field")

    def _validate_ranges(self, frame: TelemetryFrame) -> Optional[str]:
        assert frame.temperature_c is not None
        assert frame.vibration_mm_s is not None
        assert frame.cycle_count is not None

        if not (TEMPERATURE_RANGE[0] <= frame.temperature_c <= TEMPERATURE_RANGE[1]):
            return "Temperature outside contractual range"
        if not (VIBRATION_RANGE[0] <= frame.vibration_mm_s <= VIBRATION_RANGE[1]):
            return "Vibration outside contractual range"
        if frame.cycle_count < 0 or frame.cycle_count > 1_000_000:
            return "Cycle count outside contractual range"
        return None

    def _classify_measurements(self, frame: TelemetryFrame) -> ValidationClassification:
        assert frame.temperature_c is not None
        assert frame.vibration_mm_s is not None

        if frame.temperature_c > TEMP_MAJOR_THRESHOLD or frame.vibration_mm_s > VIB_MAJOR_THRESHOLD:
            return ValidationClassification.ANOMALOUS
        if (
            TEMP_MINOR_BAND[0] <= frame.temperature_c <= TEMP_MINOR_BAND[1]
            or VIB_MINOR_BAND[0] <= frame.vibration_mm_s <= VIB_MINOR_BAND[1]
        ):
            return ValidationClassification.ANOMALOUS
        return ValidationClassification.VALID

    def _validate_monotonicity(self, frame: TelemetryFrame) -> Optional[str]:
        if self._last_timestamp is not None and frame.timestamp_utc < self._last_timestamp:
            return "Timestamp regression detected"

        if frame.quality_code != QualityCode.NO_DATA:
            assert frame.cycle_count is not None
            if self._last_cycle is not None:
                if frame.cycle_count < self._last_cycle and frame.status != Status.MAINTENANCE:
                    return "Cycle count regression detected"
            self._last_cycle = frame.cycle_count

        self._last_timestamp = frame.timestamp_utc
        if frame.status == Status.MAINTENANCE:
            self._maintenance_active = True
        elif self._maintenance_active:
            self._maintenance_active = False
        return None

    def _validate_timestamp_skew(self, frame: TelemetryFrame) -> Optional[str]:
        skew = self.clock.utc_ms() - frame.timestamp_utc
        if skew > MAX_TIMESTAMP_SKEW_MS:
            return "Frame timestamp stale"
        return None
