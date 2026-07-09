"""Diagnostics engine implementing the approved taxonomy and lifecycle."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .models import (
    Alarm,
    AlarmCode,
    DiagnosticEvent,
    EventType,
    QualityCode,
    Severity,
    Status,
    TelemetryFrame,
    ValidationClassification,
    ValidationResult,
    WatchdogSnapshot,
)

THERMAL_MINOR = (90.0, 100.0)
THERMAL_MAJOR = 100.0
VIBRATION_MINOR = (30.0, 40.0)
VIBRATION_MAJOR = 40.0
RECOVERY_FRAMES_REQUIRED = 2


@dataclass(slots=True)
class DiagnosticsEngine:
    active_alarms: Dict[AlarmCode, Alarm] = field(default_factory=dict)
    first_out_code: Optional[AlarmCode] = None
    _prev_status: Optional[Status] = None

    def evaluate(
        self,
        result: ValidationResult,
        snapshot: WatchdogSnapshot,
    ) -> List[DiagnosticEvent]:
        events: List[DiagnosticEvent] = []
        frame = result.frame
        timestamp_ms = frame.timestamp_utc if frame else 0

        if result.classification == ValidationClassification.NO_DATA and frame:
            events.append(self._info_event(AlarmCode.QUALITY_NO_DATA, "NO_DATA heartbeat received", frame))
            self._prev_status = frame.status
            events.extend(self._process_watchdog(snapshot, timestamp_ms, frame))
            return events

        if result.classification == ValidationClassification.INVALID:
            if frame:
                events.extend(self._process_invalid(result, frame))
            return events

        if frame:
            events.extend(self._process_measurements(frame, snapshot))
            events.extend(self._process_quality(frame))
            events.extend(self._try_clear_alarm(AlarmCode.COUNTER_REGRESSION, frame, snapshot))
            events.extend(self._try_clear_alarm(AlarmCode.TIMESTAMP_REGRESSION, frame, snapshot))
            events.extend(self._try_clear_alarm(AlarmCode.INPUT_OUT_OF_RANGE, frame, snapshot))
            self._prev_status = frame.status

        events.extend(self._process_watchdog(snapshot, timestamp_ms, frame))
        return events

    def _process_measurements(self, frame: TelemetryFrame, snapshot: WatchdogSnapshot) -> List[DiagnosticEvent]:
        events: List[DiagnosticEvent] = []
        if frame.temperature_c is not None:
            events.extend(self._evaluate_threshold(
                AlarmCode.THERMAL_OVER_LIMIT,
                frame.temperature_c,
                THERMAL_MINOR,
                THERMAL_MAJOR,
                frame,
                snapshot,
                "High temperature",
                "Temperature approaching limit",
            ))
        if frame.vibration_mm_s is not None:
            events.extend(self._evaluate_threshold(
                AlarmCode.VIBRATION_OVER_LIMIT,
                frame.vibration_mm_s,
                VIBRATION_MINOR,
                VIBRATION_MAJOR,
                frame,
                snapshot,
                "High vibration",
                "Vibration approaching limit",
            ))
        return events

    def _evaluate_threshold(
        self,
        code: AlarmCode,
        value: float,
        minor_band: tuple[float, float],
        major_threshold: float,
        frame: TelemetryFrame,
        snapshot: WatchdogSnapshot,
        major_desc: str,
        minor_desc: str,
    ) -> List[DiagnosticEvent]:
        events: List[DiagnosticEvent] = []
        if value > major_threshold:
            events.extend(self._activate_alarm(code, Severity.MAJOR, frame, major_desc))
        elif minor_band[0] <= value <= minor_band[1]:
            events.extend(self._activate_alarm(code, Severity.MINOR, frame, minor_desc))
        else:
            events.extend(self._try_clear_alarm(code, frame, snapshot))
        return events

    def _process_quality(self, frame: TelemetryFrame) -> List[DiagnosticEvent]:
        events: List[DiagnosticEvent] = []
        if frame.quality_code == QualityCode.BAD_DATA:
            events.extend(self._activate_alarm(AlarmCode.QUALITY_BAD_DATA, Severity.MINOR, frame, "Producer flagged BAD_DATA"))
        else:
            alarm = self.active_alarms.get(AlarmCode.QUALITY_BAD_DATA)
            if alarm and alarm.cleared_at is None:
                alarm.recovery_frames += 1
                if alarm.recovery_frames >= RECOVERY_FRAMES_REQUIRED:
                    events.extend(self._clear_alarm(AlarmCode.QUALITY_BAD_DATA, frame))
        return events

    def _process_invalid(self, result: ValidationResult, frame: TelemetryFrame) -> List[DiagnosticEvent]:
        events: List[DiagnosticEvent] = []
        reason = result.reason or ""

        if "Cycle count regression" in reason:
            events.extend(self._activate_alarm(
                AlarmCode.COUNTER_REGRESSION, Severity.MAJOR, frame, reason,
            ))
        elif "Timestamp regression" in reason:
            events.extend(self._activate_alarm(
                AlarmCode.TIMESTAMP_REGRESSION, Severity.MAJOR, frame, reason,
            ))
        elif "stale" in reason.lower():
            events.extend(self._activate_alarm(
                AlarmCode.TIMESTAMP_REGRESSION, Severity.MAJOR, frame, reason,
            ))
        elif "outside contractual range" in reason:
            events.extend(self._activate_alarm(
                AlarmCode.INPUT_OUT_OF_RANGE, Severity.MINOR, frame, reason,
            ))

        for event in events:
            event.frame_id = None
            event.context["source_frame_id"] = frame.frame_id

        return events

    def _process_watchdog(
        self,
        snapshot: WatchdogSnapshot,
        timestamp_ms: int,
        frame: Optional[TelemetryFrame],
    ) -> List[DiagnosticEvent]:
        events: List[DiagnosticEvent] = []

        if snapshot.missed_heartbeats >= 3:
            events.extend(self._activate_alarm(
                AlarmCode.COMMUNICATION_LOSS, Severity.MAJOR, frame, "Communication loss: >=3 missed heartbeats", timestamp_ms
            ))
        elif snapshot.missed_heartbeats == 2:
            events.extend(self._activate_alarm(
                AlarmCode.COMMUNICATION_WARNING, Severity.MINOR, frame, "Communication warning: 2 missed heartbeats", timestamp_ms
            ))
        else:
            if snapshot.communication_recovery_frames >= RECOVERY_FRAMES_REQUIRED:
                events.extend(self._clear_alarm(AlarmCode.COMMUNICATION_WARNING, frame))
                events.extend(self._clear_alarm(AlarmCode.COMMUNICATION_LOSS, frame))

        if snapshot.measurement_recovery_frames >= RECOVERY_FRAMES_REQUIRED:
            events.extend(self._clear_alarm(AlarmCode.QUALITY_NO_DATA, frame))

        return events

    def _activate_alarm(
        self,
        code: AlarmCode,
        severity: Severity,
        frame: Optional[TelemetryFrame],
        description: str,
        timestamp_ms: Optional[int] = None,
    ) -> List[DiagnosticEvent]:
        ts = timestamp_ms if timestamp_ms is not None else (frame.timestamp_utc if frame else 0)
        alarm = self.active_alarms.get(code)

        if alarm is None or alarm.cleared_at is not None:
            alarm = Alarm(
                code=code,
                severity=severity,
                activated_at=ts,
                details=self._capture_context(frame, description),
            )
            self.active_alarms[code] = alarm

            if severity == Severity.MAJOR and self.first_out_code is None:
                alarm.first_out = True
                self.first_out_code = code

            return [DiagnosticEvent(
                event_type=EventType.ACTIVATE,
                alarm=alarm,
                frame_id=frame.frame_id if frame else None,
                occurred_at=ts,
                context=alarm.details,
            )]

        if alarm.severity != severity:
            alarm.severity = severity
            alarm.details = self._capture_context(frame, description)
            if severity == Severity.MAJOR and self.first_out_code is None:
                alarm.first_out = True
                self.first_out_code = code

            return [DiagnosticEvent(
                event_type=EventType.ACTIVATE,
                alarm=alarm,
                frame_id=frame.frame_id if frame else None,
                occurred_at=ts,
                context=alarm.details,
            )]

        alarm.recovery_frames = 0
        return []

    def _try_clear_alarm(
        self,
        code: AlarmCode,
        frame: TelemetryFrame,
        snapshot: WatchdogSnapshot,
    ) -> List[DiagnosticEvent]:
        alarm = self.active_alarms.get(code)
        if alarm is None or alarm.cleared_at is not None:
            return []

        alarm.recovery_frames += 1
        if alarm.recovery_frames < RECOVERY_FRAMES_REQUIRED:
            return []

        return self._clear_alarm(code, frame)

    def _clear_alarm(self, code: AlarmCode, frame: Optional[TelemetryFrame]) -> List[DiagnosticEvent]:
        alarm = self.active_alarms.get(code)
        if alarm is None or alarm.cleared_at is not None:
            return []

        alarm.cleared_at = frame.timestamp_utc if frame else 0
        alarm.recovery_frames = 0

        if all(a.cleared_at is not None for a in self.active_alarms.values()):
            self.first_out_code = None

        return [DiagnosticEvent(
            event_type=EventType.CLEAR,
            alarm=alarm,
            frame_id=frame.frame_id if frame else None,
            occurred_at=alarm.cleared_at,
            context=self._capture_context(frame, "Alarm cleared"),
        )]

    def _info_event(
        self,
        code: AlarmCode,
        description: str,
        frame: TelemetryFrame,
    ) -> DiagnosticEvent:
        alarm = Alarm(
            code=code,
            severity=Severity.INFO,
            activated_at=frame.timestamp_utc,
            details=self._capture_context(frame, description),
        )
        context = alarm.details.copy()
        context["source_frame_id"] = frame.frame_id
        return DiagnosticEvent(
            event_type=EventType.INFO,
            alarm=alarm,
            frame_id=None,
            occurred_at=frame.timestamp_utc,
            context=context,
        )

    @staticmethod
    def _capture_context(frame: Optional[TelemetryFrame], description: str) -> Dict[str, object]:
        if frame is None:
            return {"description": description}
        return {
            "description": description,
            "temperature_c": frame.temperature_c,
            "vibration_mm_s": frame.vibration_mm_s,
            "cycle_count": frame.cycle_count,
            "status": frame.status.value,
            "quality_code": frame.quality_code.value,
            "frame_id": frame.frame_id,
            "timestamp_utc": frame.timestamp_utc,
        }
