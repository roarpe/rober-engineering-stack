"""Deterministic telemetry source that simulates OT frames."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from .models import QualityCode, Status
from .utils.clock import Clock, SystemClock


@dataclass
class TelemetryProfile:
    base_temperature: float = 60.0
    base_vibration: float = 10.0
    noise_step: float = 0.5


class TelemetrySource:
    """Generates deterministic telemetry frames for the pilot."""

    def __init__(
        self,
        clock: Optional[Clock] = None,
        cadence_seconds: float = 2.0,
        profile: Optional[TelemetryProfile] = None,
    ) -> None:
        self._clock = clock or SystemClock()
        self._cadence_ms = int(cadence_seconds * 1000)
        self._profile = profile or TelemetryProfile()
        self._cycle_count = 0
        self._last_timestamp: Optional[int] = None

    def _next_timestamp(self) -> int:
        if self._last_timestamp is None:
            self._last_timestamp = self._clock.utc_ms()
        else:
            self._last_timestamp += self._cadence_ms
        return self._last_timestamp

    def _next_temperature(self) -> float:
        return self._profile.base_temperature + (self._cycle_count % 5) * self._profile.noise_step

    def _next_vibration(self) -> float:
        return self._profile.base_vibration + ((self._cycle_count % 3) * self._profile.noise_step)

    def next_frame(self) -> dict:
        self._cycle_count += 1
        timestamp = self._next_timestamp()
        return {
            "frame_id": str(uuid.uuid4()),
            "timestamp_utc": timestamp,
            "temperature_c": self._next_temperature(),
            "vibration_mm_s": self._next_vibration(),
            "cycle_count": self._cycle_count,
            "status": Status.RUNNING.value,
            "quality_code": QualityCode.GOOD.value,
            "diagnostic_notes": None,
        }

    @staticmethod
    def build_no_data_frame(frame_id: Optional[str] = None, timestamp_utc: Optional[int] = None) -> dict:
        return {
            "frame_id": frame_id or str(uuid.uuid4()),
            "timestamp_utc": timestamp_utc or 0,
            "temperature_c": None,
            "vibration_mm_s": None,
            "cycle_count": None,
            "status": Status.RUNNING.value,
            "quality_code": QualityCode.NO_DATA.value,
            "diagnostic_notes": "heartbeat",
        }
