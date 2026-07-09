"""Test 2: Verifies that valid frames persist correctly in SQLite."""

from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from pilot.diagnostics import DiagnosticsEngine
from pilot.ingestion import IngestionService
from pilot.models import ValidationClassification
from pilot.persistence import PersistenceManager
from pilot.utils.clock import FakeClock
from pilot.validator import Validator
from pilot.watchdog import WatchdogMonitor


class TestIngestionValid(unittest.TestCase):
    """Confirms valid frames persist and summaries match."""

    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self._tmpdir.name) / "test_valid.sqlite")
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
            "frame_id": f"valid-frame-{n:04d}",
            "timestamp_utc": self.clock.utc_ms(),
            "temperature_c": 60.0,
            "vibration_mm_s": 10.0,
            "cycle_count": n,
            "status": "RUNNING",
            "quality_code": "GOOD",
            "diagnostic_notes": None,
        }

    def test_valid_frames_persisted(self) -> None:
        n = 5
        for i in range(1, n + 1):
            self.ingestion.process_frame(self._make_valid_frame(i))

        self.assertEqual(self.ingestion.counters.frames_processed, n)
        self.assertEqual(self.ingestion.counters.frames_persisted, n)
        self.assertEqual(self.ingestion.counters.frames_rejected_schema, 0)
        self.assertEqual(self.ingestion.counters.frames_rejected_range, 0)
        self.assertEqual(self.ingestion.counters.frames_rejected_monotonicity, 0)
        self.assertEqual(self.ingestion.counters.no_data_count, 0)

        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.execute("SELECT COUNT(*) FROM telemetry_frames")
            self.assertEqual(cur.fetchone()[0], n)
            cur = conn.execute("SELECT frame_id, temperature_c, vibration_mm_s, cycle_count FROM telemetry_frames ORDER BY cycle_count")
            rows = cur.fetchall()
            for i, row in enumerate(rows, 1):
                self.assertEqual(row[0], f"valid-frame-{i:04d}")
                self.assertAlmostEqual(row[1], 60.0)
                self.assertAlmostEqual(row[2], 10.0)
                self.assertEqual(row[3], i)
        finally:
            conn.close()

    def test_no_diagnostic_events_for_normal_data(self) -> None:
        for i in range(1, 4):
            self.ingestion.process_frame(self._make_valid_frame(i))

        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.execute("SELECT COUNT(*) FROM diagnostic_events")
            self.assertEqual(cur.fetchone()[0], 0)
        finally:
            conn.close()

    def test_summary_reflects_counts(self) -> None:
        for i in range(1, 4):
            self.ingestion.process_frame(self._make_valid_frame(i))

        summary = self.ingestion.build_summary(0)
        self.assertEqual(summary.frames_processed, 3)
        self.assertEqual(summary.frames_persisted, 3)
        self.assertEqual(summary.no_data_count, 0)
        self.assertEqual(summary.exit_code, 0)
        self.assertEqual(len(summary.active_alarms), 0)


if __name__ == "__main__":
    unittest.main()
