"""Test 4: Verifies diagnostic threshold behavior and first-out latching.

Also covers: communication recovery, measurement availability recovery,
and diagnostic event lifecycle (activate/clear/persist).
"""

from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from pilot.diagnostics import DiagnosticsEngine
from pilot.ingestion import IngestionService
from pilot.models import (
    Alarm,
    AlarmCode,
    EventType,
    QualityCode,
    Severity,
    Status,
    TelemetryFrame,
    ValidationClassification,
    ValidationResult,
    WatchdogSnapshot,
)
from pilot.persistence import PersistenceManager
from pilot.utils.clock import FakeClock
from pilot.validator import Validator
from pilot.watchdog import WatchdogMonitor


def make_result(
    temp: float = 60.0,
    vibration: float = 10.0,
    cycle: int = 1,
    timestamp: int = 1_000_000,
    status: Status = Status.RUNNING,
    quality: QualityCode = QualityCode.GOOD,
) -> ValidationResult:
    frame = TelemetryFrame(
        frame_id=f"frame-{cycle:04d}",
        timestamp_utc=timestamp,
        temperature_c=temp,
        vibration_mm_s=vibration,
        cycle_count=cycle,
        status=status,
        quality_code=quality,
    )
    if quality == QualityCode.NO_DATA:
        classification = ValidationClassification.NO_DATA
    elif temp > 100.0 or vibration > 40.0 or (90.0 <= temp <= 100.0) or (30.0 <= vibration <= 40.0):
        classification = ValidationClassification.ANOMALOUS
    else:
        classification = ValidationClassification.VALID
    return ValidationResult(
        frame=frame,
        is_valid=classification in {ValidationClassification.VALID, ValidationClassification.ANOMALOUS},
        reason=None,
        violations=[],
        classification=classification,
    )


def make_snapshot(missed=0, comm_recovery=1, meas_recovery=1) -> WatchdogSnapshot:
    return WatchdogSnapshot(
        missed_heartbeats=missed,
        communication_recovery_frames=comm_recovery,
        measurement_recovery_frames=meas_recovery,
    )


class TestDiagnosticsThresholds(unittest.TestCase):
    """Exercises MAJOR/MINOR transitions and first-out latching."""

    def setUp(self) -> None:
        self.engine = DiagnosticsEngine()

    def test_major_temperature_activates_alarm(self) -> None:
        result = make_result(temp=105.0)
        events = self.engine.evaluate(result, make_snapshot())
        activate_events = [e for e in events if e.event_type == EventType.ACTIVATE]
        self.assertEqual(len(activate_events), 1)
        self.assertEqual(activate_events[0].alarm.code, AlarmCode.THERMAL_OVER_LIMIT)
        self.assertEqual(activate_events[0].alarm.severity, Severity.MAJOR)

    def test_minor_temperature_activates_alarm(self) -> None:
        result = make_result(temp=95.0)
        events = self.engine.evaluate(result, make_snapshot())
        activate_events = [e for e in events if e.event_type == EventType.ACTIVATE]
        self.assertEqual(len(activate_events), 1)
        self.assertEqual(activate_events[0].alarm.code, AlarmCode.THERMAL_OVER_LIMIT)
        self.assertEqual(activate_events[0].alarm.severity, Severity.MINOR)

    def test_major_vibration_activates_alarm(self) -> None:
        result = make_result(vibration=45.0)
        events = self.engine.evaluate(result, make_snapshot())
        activate_events = [e for e in events if e.event_type == EventType.ACTIVATE]
        self.assertEqual(len(activate_events), 1)
        self.assertEqual(activate_events[0].alarm.code, AlarmCode.VIBRATION_OVER_LIMIT)
        self.assertEqual(activate_events[0].alarm.severity, Severity.MAJOR)

    def test_minor_vibration_activates_alarm(self) -> None:
        result = make_result(vibration=35.0)
        events = self.engine.evaluate(result, make_snapshot())
        activate_events = [e for e in events if e.event_type == EventType.ACTIVATE]
        self.assertEqual(len(activate_events), 1)
        self.assertEqual(activate_events[0].alarm.code, AlarmCode.VIBRATION_OVER_LIMIT)
        self.assertEqual(activate_events[0].alarm.severity, Severity.MINOR)

    def test_first_out_latched_on_major(self) -> None:
        result = make_result(temp=105.0, vibration=45.0, cycle=1)
        events = self.engine.evaluate(result, make_snapshot())
        major_alarms = [e.alarm for e in events if e.event_type == EventType.ACTIVATE and e.alarm.severity == Severity.MAJOR]
        first_out = [a for a in major_alarms if a.first_out]
        self.assertEqual(len(first_out), 1)
        self.assertEqual(self.engine.first_out_code, first_out[0].code)

    def test_alarm_clears_after_two_nominal_frames(self) -> None:
        self.engine.evaluate(make_result(temp=105.0, cycle=1), make_snapshot(meas_recovery=1))
        clear_events_1 = self.engine.evaluate(make_result(temp=60.0, cycle=2), make_snapshot(meas_recovery=2))
        self.assertEqual(len([e for e in clear_events_1 if e.event_type == EventType.CLEAR]), 0)
        clear_events_2 = self.engine.evaluate(make_result(temp=60.0, cycle=3), make_snapshot(meas_recovery=3))
        clear_events = [e for e in clear_events_2 if e.event_type == EventType.CLEAR]
        self.assertGreaterEqual(len(clear_events), 1)
        self.assertEqual(clear_events[0].alarm.code, AlarmCode.THERMAL_OVER_LIMIT)

    def test_severity_escalation_from_minor_to_major(self) -> None:
        events_minor = self.engine.evaluate(make_result(temp=95.0, cycle=1), make_snapshot())
        self.assertEqual(events_minor[0].alarm.severity, Severity.MINOR)
        events_major = self.engine.evaluate(make_result(temp=105.0, cycle=2), make_snapshot())
        activate_events = [e for e in events_major if e.event_type == EventType.ACTIVATE]
        self.assertEqual(len(activate_events), 1)
        self.assertEqual(activate_events[0].alarm.severity, Severity.MAJOR)

    def test_communication_warning_at_two_missed(self) -> None:
        result = make_result(cycle=1)
        events = self.engine.evaluate(result, make_snapshot(missed=2, comm_recovery=0))
        activate_events = [e for e in events if e.event_type == EventType.ACTIVATE]
        self.assertTrue(any(e.alarm.code == AlarmCode.COMMUNICATION_WARNING for e in activate_events))

    def test_communication_loss_at_three_missed(self) -> None:
        result = make_result(cycle=1)
        events = self.engine.evaluate(result, make_snapshot(missed=3, comm_recovery=0))
        activate_events = [e for e in events if e.event_type == EventType.ACTIVATE]
        self.assertTrue(any(e.alarm.code == AlarmCode.COMMUNICATION_LOSS for e in activate_events))

    # --- Gap 10: Communication recovery ---

    def test_communication_warning_clears_after_two_on_time_frames(self) -> None:
        """COMMUNICATION_WARNING clears after two consecutive on-time frames (comm_recovery >= 2)."""
        self.engine.evaluate(make_result(cycle=1), make_snapshot(missed=2, comm_recovery=0))
        self.assertIn(AlarmCode.COMMUNICATION_WARNING, self.engine.active_alarms)

        events1 = self.engine.evaluate(make_result(cycle=2), make_snapshot(missed=0, comm_recovery=1))
        self.assertEqual(len([e for e in events1 if e.event_type == EventType.CLEAR]), 0)

        events2 = self.engine.evaluate(make_result(cycle=3), make_snapshot(missed=0, comm_recovery=2))
        clears = [e for e in events2 if e.event_type == EventType.CLEAR]
        self.assertTrue(any(e.alarm.code == AlarmCode.COMMUNICATION_WARNING for e in clears))

    def test_no_data_counts_as_communication_heartbeat(self) -> None:
        """NO_DATA frames count toward communication recovery."""
        self.engine.evaluate(make_result(cycle=1), make_snapshot(missed=2, comm_recovery=0))
        self.assertIn(AlarmCode.COMMUNICATION_WARNING, self.engine.active_alarms)

        # Two NO_DATA frames with comm_recovery incrementing
        nd_frame = TelemetryFrame(
            frame_id="nd-001", timestamp_utc=1_000_002, temperature_c=None,
            vibration_mm_s=None, cycle_count=None, status=Status.RUNNING,
            quality_code=QualityCode.NO_DATA,
        )
        nd_result = ValidationResult(
            frame=nd_frame, is_valid=False, reason=None, violations=[],
            classification=ValidationClassification.NO_DATA,
        )
        events1 = self.engine.evaluate(nd_result, make_snapshot(missed=0, comm_recovery=1))
        events2 = self.engine.evaluate(nd_result, make_snapshot(missed=0, comm_recovery=2))
        clears = [e for e in events2 if e.event_type == EventType.CLEAR]
        self.assertTrue(any(e.alarm.code == AlarmCode.COMMUNICATION_WARNING for e in clears))

    # --- Gap 11: Measurement availability recovery ---

    def test_measurement_recovery_independent_of_communication(self) -> None:
        """Measurement recovery frames increment independently of communication recovery."""
        self.engine.evaluate(make_result(cycle=1), make_snapshot(missed=0, comm_recovery=1, meas_recovery=1))
        # Verify that measurement_recovery_frames tracks separately
        # by having comm_recovery=0 but meas_recovery=2 and checking QUALITY_NO_DATA clears
        nd_alarm = Alarm(code=AlarmCode.QUALITY_NO_DATA, severity=Severity.INFO, activated_at=1_000_000)
        self.engine.active_alarms[AlarmCode.QUALITY_NO_DATA] = nd_alarm
        events = self.engine.evaluate(make_result(cycle=2), make_snapshot(missed=0, comm_recovery=0, meas_recovery=2))
        clears = [e for e in events if e.event_type == EventType.CLEAR]
        self.assertTrue(any(e.alarm.code == AlarmCode.QUALITY_NO_DATA for e in clears))

    def test_thermal_alarm_requires_measurement_frames_to_clear(self) -> None:
        """Thermal alarm does NOT clear when measurement_recovery_frames is 0 (e.g. only NO_DATA)."""
        self.engine.evaluate(make_result(temp=105.0, cycle=1), make_snapshot(meas_recovery=1))
        self.assertIn(AlarmCode.THERMAL_OVER_LIMIT, self.engine.active_alarms)

        # Feed two NO_DATA frames — should not clear thermal alarm
        nd_frame = TelemetryFrame(
            frame_id="nd-001", timestamp_utc=1_000_002, temperature_c=None,
            vibration_mm_s=None, cycle_count=None, status=Status.RUNNING,
            quality_code=QualityCode.NO_DATA,
        )
        nd_result = ValidationResult(
            frame=nd_frame, is_valid=False, reason=None, violations=[],
            classification=ValidationClassification.NO_DATA,
        )
        self.engine.evaluate(nd_result, make_snapshot(missed=0, comm_recovery=1, meas_recovery=0))
        self.assertIn(AlarmCode.THERMAL_OVER_LIMIT, self.engine.active_alarms)
        self.assertIsNone(self.engine.active_alarms[AlarmCode.THERMAL_OVER_LIMIT].cleared_at)

    # --- Gap 13: Diagnostic lifecycle persistence ---

    def test_diagnostic_lifecycle_persisted_to_sqlite(self) -> None:
        """Full lifecycle: activate → clear is persisted to diagnostic_events table."""
        tmpdir = tempfile.TemporaryDirectory()
        try:
            db_path = str(Path(tmpdir.name) / "diag_lifecycle.sqlite")
            clock = FakeClock(monotonic_seconds=0.0, utc_millis=1_000_000)
            persistence = PersistenceManager(db_path)
            persistence.ensure_schema()
            ingestion = IngestionService(
                validator=Validator(clock=clock),
                diagnostics=DiagnosticsEngine(),
                persistence=persistence,
                clock=clock,
                watchdog=WatchdogMonitor(),
            )
            ingestion.start()

            # Activate thermal alarm
            hot = {
                "frame_id": "hot-001", "timestamp_utc": clock.utc_ms(),
                "temperature_c": 105.0, "vibration_mm_s": 10.0, "cycle_count": 1,
                "status": "RUNNING", "quality_code": "GOOD", "diagnostic_notes": None,
            }
            ingestion.process_frame(hot)

            # Two nominal frames to clear
            for i in range(2, 4):
                cool = {
                    "frame_id": f"cool-{i:04d}", "timestamp_utc": clock.utc_ms(),
                    "temperature_c": 60.0, "vibration_mm_s": 10.0, "cycle_count": i,
                    "status": "RUNNING", "quality_code": "GOOD", "diagnostic_notes": None,
                }
                ingestion.process_frame(cool)

            conn = sqlite3.connect(db_path)
            try:
                cur = conn.execute("SELECT event_type, alarm_code, severity FROM diagnostic_events ORDER BY event_id")
                rows = cur.fetchall()
                activate_rows = [r for r in rows if r[0] == "ACTIVATE"]
                clear_rows = [r for r in rows if r[0] == "CLEAR"]
                self.assertGreaterEqual(len(activate_rows), 1)
                self.assertEqual(activate_rows[0][1], "THERMAL_OVER_LIMIT")
                self.assertEqual(activate_rows[0][2], "MAJOR")
                self.assertGreaterEqual(len(clear_rows), 1)
                self.assertEqual(clear_rows[0][1], "THERMAL_OVER_LIMIT")
            finally:
                conn.close()
            ingestion.close()
        finally:
            tmpdir.cleanup()


if __name__ == "__main__":
    unittest.main()
