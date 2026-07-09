"""Test 3: Verifies that invalid frames are rejected without crashing.

Also covers: cycle_count regression, timestamp regression, stale timestamps,
BAD_DATA semantics, NO_DATA traceability, and diagnostic events for invalid frames.
"""

from __future__ import annotations

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from pilot.diagnostics import DiagnosticsEngine
from pilot.ingestion import IngestionService
from pilot.models import AlarmCode, EventType, Severity, ValidationClassification
from pilot.persistence import PersistenceManager
from pilot.utils.clock import FakeClock
from pilot.validator import Validator, MAX_TIMESTAMP_SKEW_MS
from pilot.watchdog import WatchdogMonitor


class TestIngestionInvalid(unittest.TestCase):
    """Injects schema/range violations; ensures rejections logged without crash."""

    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self._tmpdir.name) / "test_invalid.sqlite")
        self.clock = FakeClock(monotonic_seconds=0.0, utc_millis=1_000_000)
        self.persistence = PersistenceManager(self.db_path)
        self.persistence.ensure_schema()
        self.ingestion = IngestionService(
            validator=Validator(clock=self.clock),
            diagnostics=DiagnosticsEngine(),
            persistence=self.persistence,
            clock=self.clock,
            watchdog=WatchdogMonitor(),
        )
        self.ingestion.start()

    def tearDown(self) -> None:
        self.ingestion.close()
        self._tmpdir.cleanup()

    def _make_valid_frame(self, n: int) -> dict:
        return {
            "frame_id": f"frame-{n:04d}",
            "timestamp_utc": self.clock.utc_ms(),
            "temperature_c": 60.0,
            "vibration_mm_s": 10.0,
            "cycle_count": n,
            "status": "RUNNING",
            "quality_code": "GOOD",
            "diagnostic_notes": None,
        }

    def test_missing_required_field_rejected(self) -> None:
        frame = self._make_valid_frame(1)
        del frame["temperature_c"]
        del frame["vibration_mm_s"]
        del frame["cycle_count"]
        self.ingestion.process_frame(frame)
        self.assertEqual(self.ingestion.counters.frames_rejected_schema, 1)
        self.assertEqual(self.ingestion.counters.frames_persisted, 0)

    def test_temperature_out_of_range_rejected(self) -> None:
        frame = self._make_valid_frame(1)
        frame["temperature_c"] = 200.0
        self.ingestion.process_frame(frame)
        self.assertEqual(self.ingestion.counters.frames_rejected_range, 1)
        self.assertEqual(self.ingestion.counters.frames_persisted, 0)

    def test_vibration_out_of_range_rejected(self) -> None:
        frame = self._make_valid_frame(1)
        frame["vibration_mm_s"] = 99.0
        self.ingestion.process_frame(frame)
        self.assertEqual(self.ingestion.counters.frames_rejected_range, 1)
        self.assertEqual(self.ingestion.counters.frames_persisted, 0)

    def test_invalid_status_enum_rejected(self) -> None:
        frame = self._make_valid_frame(1)
        frame["status"] = "BROKEN"
        self.ingestion.process_frame(frame)
        self.assertEqual(self.ingestion.counters.frames_rejected_schema, 1)
        self.assertEqual(self.ingestion.counters.frames_persisted, 0)

    def test_no_crash_on_mixed_valid_invalid(self) -> None:
        valid = self._make_valid_frame(1)
        self.ingestion.process_frame(valid)

        invalid = self._make_valid_frame(2)
        invalid["temperature_c"] = 500.0
        self.ingestion.process_frame(invalid)

        valid2 = self._make_valid_frame(3)
        self.ingestion.process_frame(valid2)

        self.assertEqual(self.ingestion.counters.frames_processed, 3)
        self.assertEqual(self.ingestion.counters.frames_persisted, 2)
        self.assertEqual(self.ingestion.counters.frames_rejected_range, 1)

    def test_no_telemetry_rows_for_invalid_frames(self) -> None:
        frame = self._make_valid_frame(1)
        frame["temperature_c"] = -50.0
        self.ingestion.process_frame(frame)

        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.execute("SELECT COUNT(*) FROM telemetry_frames")
            self.assertEqual(cur.fetchone()[0], 0)
        finally:
            conn.close()

    def test_no_data_frame_not_persisted(self) -> None:
        frame = {
            "frame_id": "nodata-001",
            "timestamp_utc": self.clock.utc_ms(),
            "temperature_c": None,
            "vibration_mm_s": None,
            "cycle_count": None,
            "status": "RUNNING",
            "quality_code": "NO_DATA",
            "diagnostic_notes": "heartbeat",
        }
        self.ingestion.process_frame(frame)
        self.assertEqual(self.ingestion.counters.no_data_count, 1)
        self.assertEqual(self.ingestion.counters.frames_persisted, 0)

        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.execute("SELECT COUNT(*) FROM telemetry_frames")
            self.assertEqual(cur.fetchone()[0], 0)
        finally:
            conn.close()


    # --- Gap 6: Cycle count regression ---

    def test_cycle_count_regression_rejected(self) -> None:
        f1 = self._make_valid_frame(1)
        self.ingestion.process_frame(f1)
        f2 = self._make_valid_frame(2)
        f2["cycle_count"] = 0
        self.ingestion.process_frame(f2)
        self.assertEqual(self.ingestion.counters.frames_rejected_monotonicity, 1)
        self.assertEqual(self.ingestion.counters.frames_persisted, 1)

    def test_cycle_count_regression_raises_diagnostic(self) -> None:
        f1 = self._make_valid_frame(1)
        self.ingestion.process_frame(f1)
        f2 = self._make_valid_frame(2)
        f2["cycle_count"] = 0
        events = self.ingestion.process_frame(f2)
        activate = [e for e in events if e.event_type == EventType.ACTIVATE]
        self.assertTrue(any(e.alarm.code == AlarmCode.COUNTER_REGRESSION for e in activate))
        reg = [e for e in activate if e.alarm.code == AlarmCode.COUNTER_REGRESSION][0]
        self.assertEqual(reg.alarm.severity, Severity.MAJOR)
        self.assertIsNone(reg.frame_id)
        self.assertEqual(reg.context.get("source_frame_id"), f2["frame_id"])

    # --- Gap 7: Timestamp regression ---

    def test_timestamp_regression_rejected(self) -> None:
        f1 = self._make_valid_frame(1)
        self.ingestion.process_frame(f1)
        f2 = self._make_valid_frame(2)
        f2["timestamp_utc"] = f1["timestamp_utc"] - 1000
        self.ingestion.process_frame(f2)
        self.assertEqual(self.ingestion.counters.frames_rejected_monotonicity, 1)
        self.assertEqual(self.ingestion.counters.frames_persisted, 1)

    def test_timestamp_regression_raises_diagnostic(self) -> None:
        f1 = self._make_valid_frame(1)
        self.ingestion.process_frame(f1)
        f2 = self._make_valid_frame(2)
        f2["timestamp_utc"] = f1["timestamp_utc"] - 1000
        events = self.ingestion.process_frame(f2)
        activate = [e for e in events if e.event_type == EventType.ACTIVATE]
        self.assertTrue(any(e.alarm.code == AlarmCode.TIMESTAMP_REGRESSION for e in activate))
        ts_reg = [e for e in activate if e.alarm.code == AlarmCode.TIMESTAMP_REGRESSION][0]
        self.assertEqual(ts_reg.alarm.severity, Severity.MAJOR)
        self.assertIsNone(ts_reg.frame_id)

    def test_timestamp_regression_separate_from_cycle_regression(self) -> None:
        """Gap 7: timestamp regression and cycle_count regression are separate conditions."""
        f1 = self._make_valid_frame(1)
        self.ingestion.process_frame(f1)
        # Timestamp backwards but cycle_count forwards — should be timestamp regression only
        f2 = self._make_valid_frame(2)
        f2["timestamp_utc"] = f1["timestamp_utc"] - 1000
        events = self.ingestion.process_frame(f2)
        activate = [e for e in events if e.event_type == EventType.ACTIVATE]
        codes = {e.alarm.code for e in activate}
        self.assertIn(AlarmCode.TIMESTAMP_REGRESSION, codes)
        self.assertNotIn(AlarmCode.COUNTER_REGRESSION, codes)

    # --- Gap 8: Stale timestamps ---

    def test_stale_timestamp_rejected(self) -> None:
        frame = self._make_valid_frame(1)
        frame["timestamp_utc"] = self.clock.utc_ms() - MAX_TIMESTAMP_SKEW_MS - 1000
        self.ingestion.process_frame(frame)
        self.assertEqual(self.ingestion.counters.frames_rejected_monotonicity, 1)
        self.assertEqual(self.ingestion.counters.frames_persisted, 0)

    def test_future_timestamp_accepted(self) -> None:
        """Gap 8: future timestamps are NOT rejected — simulator increments by cadence."""
        frame = self._make_valid_frame(1)
        frame["timestamp_utc"] = self.clock.utc_ms() + 10_000
        self.ingestion.process_frame(frame)
        self.assertEqual(self.ingestion.counters.frames_persisted, 1)
        self.assertEqual(self.ingestion.counters.frames_rejected_monotonicity, 0)

    # --- Gap 9: BAD_DATA semantics ---

    def test_bad_data_with_measurements_persisted(self) -> None:
        """BAD_DATA with in-range measurements is persisted and raises QUALITY_BAD_DATA MINOR."""
        frame = self._make_valid_frame(1)
        frame["quality_code"] = "BAD_DATA"
        events = self.ingestion.process_frame(frame)
        self.assertEqual(self.ingestion.counters.frames_persisted, 1)
        activate = [e for e in events if e.event_type == EventType.ACTIVATE]
        self.assertTrue(any(e.alarm.code == AlarmCode.QUALITY_BAD_DATA for e in activate))
        bd = [e for e in activate if e.alarm.code == AlarmCode.QUALITY_BAD_DATA][0]
        self.assertEqual(bd.alarm.severity, Severity.MINOR)

        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.execute("SELECT quality_code FROM telemetry_frames WHERE frame_id = ?", (frame["frame_id"],))
            self.assertEqual(cur.fetchone()[0], "BAD_DATA")
        finally:
            conn.close()

    def test_bad_data_alarm_clears_after_two_good_frames(self) -> None:
        """BAD_DATA alarm clears after two consecutive GOOD frames."""
        bad = self._make_valid_frame(1)
        bad["quality_code"] = "BAD_DATA"
        self.ingestion.process_frame(bad)

        good1 = self._make_valid_frame(2)
        events1 = self.ingestion.process_frame(good1)
        self.assertEqual(len([e for e in events1 if e.event_type == EventType.CLEAR]), 0)

        good2 = self._make_valid_frame(3)
        events2 = self.ingestion.process_frame(good2)
        clears = [e for e in events2 if e.event_type == EventType.CLEAR]
        self.assertTrue(any(e.alarm.code == AlarmCode.QUALITY_BAD_DATA for e in clears))

    def test_range_violation_raises_input_out_of_range(self) -> None:
        """Range violation raises INPUT_OUT_OF_RANGE MINOR diagnostic event."""
        frame = self._make_valid_frame(1)
        frame["temperature_c"] = 200.0
        events = self.ingestion.process_frame(frame)
        activate = [e for e in events if e.event_type == EventType.ACTIVATE]
        self.assertTrue(any(e.alarm.code == AlarmCode.INPUT_OUT_OF_RANGE for e in activate))
        oor = [e for e in activate if e.alarm.code == AlarmCode.INPUT_OUT_OF_RANGE][0]
        self.assertEqual(oor.alarm.severity, Severity.MINOR)
        self.assertIsNone(oor.frame_id)
        self.assertEqual(oor.context.get("source_frame_id"), frame["frame_id"])

    # --- Gap 12: NO_DATA traceability ---

    def test_no_data_traceability(self) -> None:
        """NO_DATA generates INFO event with frame_id=NULL and source_frame_id in details_json."""
        frame = {
            "frame_id": "nodata-trace-001",
            "timestamp_utc": self.clock.utc_ms(),
            "temperature_c": None,
            "vibration_mm_s": None,
            "cycle_count": None,
            "status": "RUNNING",
            "quality_code": "NO_DATA",
            "diagnostic_notes": "heartbeat",
        }
        events = self.ingestion.process_frame(frame)
        info_events = [e for e in events if e.event_type == EventType.INFO]
        self.assertEqual(len(info_events), 1)
        self.assertIsNone(info_events[0].frame_id)
        self.assertEqual(info_events[0].context.get("source_frame_id"), "nodata-trace-001")

        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.execute("SELECT COUNT(*) FROM telemetry_frames")
            self.assertEqual(cur.fetchone()[0], 0)
            cur = conn.execute("SELECT frame_id, alarm_code, event_type, details_json FROM diagnostic_events")
            row = cur.fetchone()
            self.assertIsNone(row[0])
            self.assertEqual(row[1], "QUALITY_NO_DATA")
            self.assertEqual(row[2], "INFO")
            details = json.loads(row[3])
            self.assertEqual(details.get("source_frame_id"), "nodata-trace-001")
        finally:
            conn.close()

    # --- Gap 13: Diagnostic event persistence & lifecycle ---

    def test_diagnostic_events_persisted_for_invalid_frame(self) -> None:
        """Diagnostic events from invalid frames are persisted to SQLite."""
        f1 = self._make_valid_frame(1)
        self.ingestion.process_frame(f1)
        f2 = self._make_valid_frame(2)
        f2["cycle_count"] = 0
        self.ingestion.process_frame(f2)

        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.execute("SELECT COUNT(*) FROM diagnostic_events WHERE alarm_code = 'COUNTER_REGRESSION'")
            self.assertEqual(cur.fetchone()[0], 1)
            cur = conn.execute("SELECT frame_id, event_type, severity FROM diagnostic_events WHERE alarm_code = 'COUNTER_REGRESSION'")
            row = cur.fetchone()
            self.assertIsNone(row[0])
            self.assertEqual(row[1], "ACTIVATE")
            self.assertEqual(row[2], "MAJOR")
        finally:
            conn.close()


if __name__ == "__main__":
    unittest.main()
