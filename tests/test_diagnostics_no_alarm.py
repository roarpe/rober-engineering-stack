"""Test 5: Verifies that normal data does not raise alarms (no false positives)."""

from __future__ import annotations

import unittest

from pilot.diagnostics import DiagnosticsEngine
from pilot.models import (
    AlarmCode,
    EventType,
    QualityCode,
    Status,
    TelemetryFrame,
    ValidationClassification,
    ValidationResult,
    WatchdogSnapshot,
)


def make_normal_result(cycle: int = 1, timestamp: int = 1_000_000) -> ValidationResult:
    frame = TelemetryFrame(
        frame_id=f"normal-{cycle:04d}",
        timestamp_utc=timestamp,
        temperature_c=60.0,
        vibration_mm_s=10.0,
        cycle_count=cycle,
        status=Status.RUNNING,
        quality_code=QualityCode.GOOD,
    )
    return ValidationResult(
        frame=frame,
        is_valid=True,
        reason=None,
        violations=[],
        classification=ValidationClassification.VALID,
    )


def make_normal_snapshot() -> WatchdogSnapshot:
    return WatchdogSnapshot(
        missed_heartbeats=0,
        communication_recovery_frames=1,
        measurement_recovery_frames=1,
    )


class TestDiagnosticsNoAlarm(unittest.TestCase):
    """Ensures normal data does not raise alarms."""

    def setUp(self) -> None:
        self.engine = DiagnosticsEngine()

    def test_single_normal_frame_no_alarms(self) -> None:
        events = self.engine.evaluate(make_normal_result(1), make_normal_snapshot())
        self.assertEqual(len(events), 0)

    def test_multiple_normal_frames_no_alarms(self) -> None:
        for i in range(1, 10):
            events = self.engine.evaluate(make_normal_result(i), make_normal_snapshot())
            self.assertEqual(len(events), 0,
                             f"Unexpected alarm on frame {i}: {[e.alarm.code.value for e in events]}")

    def test_no_active_alarms_after_normal_run(self) -> None:
        for i in range(1, 6):
            self.engine.evaluate(make_normal_result(i), make_normal_snapshot())
        active = {code: alarm for code, alarm in self.engine.active_alarms.items() if alarm.cleared_at is None}
        self.assertEqual(len(active), 0)

    def test_no_first_out_after_normal_run(self) -> None:
        for i in range(1, 6):
            self.engine.evaluate(make_normal_result(i), make_normal_snapshot())
        self.assertIsNone(self.engine.first_out_code)

    def test_normal_data_at_boundary_no_alarm(self) -> None:
        frame = TelemetryFrame(
            frame_id="boundary-001",
            timestamp_utc=1_000_000,
            temperature_c=89.9,
            vibration_mm_s=29.9,
            cycle_count=1,
            status=Status.RUNNING,
            quality_code=QualityCode.GOOD,
        )
        result = ValidationResult(
            frame=frame,
            is_valid=True,
            reason=None,
            violations=[],
            classification=ValidationClassification.VALID,
        )
        events = self.engine.evaluate(result, make_normal_snapshot())
        self.assertEqual(len(events), 0)


if __name__ == "__main__":
    unittest.main()
