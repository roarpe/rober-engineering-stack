"""Test 6: End-to-end CLI test validating exit code, DB rows, and summary.

Also covers: retry/rollback on retryable SQLite errors, duplicate frame_id
IntegrityError, exit codes 0/2/3/4/5, and cli_runs best-effort persistence.
"""

from __future__ import annotations

import json
import sqlite3
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from pilot.cli import main
from pilot.exceptions import PersistenceFatalError, PersistenceRetryableError


class TestCliEndToEnd(unittest.TestCase):
    """Runs CLI with limited frames, asserts exit code 0, verifies DB rows & summary."""

    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self._tmpdir.name) / "cli_test.sqlite")

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_cli_exit_code_zero(self) -> None:
        exit_code = main(["--frames", "5", "--db-path", self.db_path, "--reset-db"])
        self.assertEqual(exit_code, 0)

    def test_cli_persists_frames(self) -> None:
        main(["--frames", "5", "--db-path", self.db_path, "--reset-db"])
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.execute("SELECT COUNT(*) FROM telemetry_frames")
            self.assertEqual(cur.fetchone()[0], 5)
        finally:
            conn.close()

    def test_cli_records_run(self) -> None:
        main(["--frames", "3", "--db-path", self.db_path, "--reset-db"])
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.execute("SELECT COUNT(*) FROM cli_runs")
            self.assertEqual(cur.fetchone()[0], 1)
            cur = conn.execute("SELECT frames_processed, frames_persisted, exit_code FROM cli_runs")
            row = cur.fetchone()
            self.assertEqual(row[0], 3)
            self.assertEqual(row[1], 3)
            self.assertEqual(row[2], 0)
        finally:
            conn.close()

    def test_cli_no_alarms_for_normal_data(self) -> None:
        main(["--frames", "5", "--db-path", self.db_path, "--reset-db"])
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.execute("SELECT COUNT(*) FROM diagnostic_events WHERE event_type = 'ACTIVATE'")
            self.assertEqual(cur.fetchone()[0], 0)
        finally:
            conn.close()

    def test_cli_usage_error_exit_code_2(self) -> None:
        exit_code = main(["--frames", "0", "--db-path", self.db_path, "--reset-db"])
        self.assertEqual(exit_code, 2)

    def test_cli_summary_printed_to_stdout(self) -> None:
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            exit_code = main(["--frames", "3", "--db-path", self.db_path, "--reset-db"])
        self.assertEqual(exit_code, 0)
        output = mock_stdout.getvalue()
        self.assertIn("frames_processed", output)
        self.assertIn("frames_persisted", output)
        self.assertIn("exit_code", output)

    # --- Gap 1: Retry/rollback on retryable SQLite errors ---

    def test_retry_on_database_locked(self) -> None:
        """PersistenceManager retries 'database is locked' once, then succeeds."""
        from pilot.persistence import PersistenceManager
        from pilot.models import TelemetryFrame, Status, QualityCode, ContractValidation
        pm = PersistenceManager(self.db_path)
        pm.ensure_schema()

        real_conn = pm._connection
        call_count = [0]

        class RetryWrapper:
            def execute(self, sql, *args, **kwargs):
                if "INSERT INTO telemetry_frames" in sql and call_count[0] == 0:
                    call_count[0] += 1
                    raise sqlite3.OperationalError("database is locked")
                return real_conn.execute(sql, *args, **kwargs)

            def commit(self):
                real_conn.commit()

            def rollback(self):
                real_conn.rollback()

            @property
            def row_factory(self):
                return real_conn.row_factory

            @row_factory.setter
            def row_factory(self, value):
                real_conn.row_factory = value

        pm._connection = RetryWrapper()

        frame = TelemetryFrame(
            frame_id="retry-001", timestamp_utc=1_000_000,
            temperature_c=60.0, vibration_mm_s=10.0, cycle_count=1,
            status=Status.RUNNING, quality_code=QualityCode.GOOD,
            contract_validation=ContractValidation.PASS,
        )
        pm.record_frame(frame, 1_000_000)

        pm._connection = real_conn
        cur = real_conn.execute("SELECT COUNT(*) FROM telemetry_frames WHERE frame_id = 'retry-001'")
        self.assertEqual(cur.fetchone()[0], 1)
        pm.close()

    # --- Gap 2: Duplicate frame_id IntegrityError ---

    def test_duplicate_frame_id_raises_persistence_fatal(self) -> None:
        """Duplicate frame_id causes IntegrityError → PersistenceFatalError (exit code 4)."""
        from pilot.persistence import PersistenceManager
        from pilot.models import TelemetryFrame, Status, QualityCode, ContractValidation
        pm = PersistenceManager(self.db_path)
        pm.ensure_schema()

        frame = TelemetryFrame(
            frame_id="dup-001", timestamp_utc=1_000_000,
            temperature_c=60.0, vibration_mm_s=10.0, cycle_count=1,
            status=Status.RUNNING, quality_code=QualityCode.GOOD,
            contract_validation=ContractValidation.PASS,
        )
        pm.record_frame(frame, 1_000_000)

        with self.assertRaises(PersistenceFatalError):
            pm.record_frame(frame, 1_000_001)
        pm.close()

    def test_duplicate_frame_id_cli_exit_code_4(self) -> None:
        """CLI returns exit code 4 when PersistenceFatalError occurs."""
        import pilot.cli as cli_module
        import pilot.ingestion as ingestion_module

        # First run to create DB
        main(["--frames", "3", "--db-path", self.db_path, "--reset-db"])

        # Patch record_frame to raise PersistenceFatalError on next run
        original_record_frame = ingestion_module.PersistenceManager.record_frame

        def fail_record_frame(self_pm, frame, ingested_at):
            raise PersistenceFatalError("Simulated IntegrityError")

        with patch.object(ingestion_module.PersistenceManager, "record_frame", fail_record_frame):
            exit_code = main(["--frames", "3", "--db-path", self.db_path])
        self.assertEqual(exit_code, 4)

    # --- Gap 3: Exit code 0 (success) ---

    def test_exit_code_zero_on_success(self) -> None:
        """Exit code 0 when all frames processed and persisted."""
        exit_code = main(["--frames", "5", "--db-path", self.db_path, "--reset-db"])
        self.assertEqual(exit_code, 0)

    # --- Gap 4: Exit code 2 (usage error) ---

    def test_exit_code_2_on_usage_error(self) -> None:
        """Exit code 2 for invalid CLI arguments."""
        exit_code = main(["--frames", "0", "--db-path", self.db_path, "--reset-db"])
        self.assertEqual(exit_code, 2)

    def test_exit_code_2_on_missing_frames_arg(self) -> None:
        """Exit code 2 when --frames is negative."""
        exit_code = main(["--frames", "-1", "--db-path", self.db_path, "--reset-db"])
        self.assertEqual(exit_code, 2)

    # --- Gap 5: Exit code 3 (run-level validation failure) ---

    def test_exit_code_3_when_all_frames_rejected(self) -> None:
        """Exit code 3 when frames_processed > 0 but frames_persisted == 0."""
        import pilot.telemetry_source as ts_module

        original_next = ts_module.TelemetrySource.next_frame

        def bad_frame(self_src):
            frame = original_next(self_src)
            frame["temperature_c"] = 999.0  # Out of range
            return frame

        with patch.object(ts_module.TelemetrySource, "next_frame", bad_frame):
            exit_code = main(["--frames", "3", "--db-path", self.db_path, "--reset-db"])
        self.assertEqual(exit_code, 3)

    # --- Gap 14: cli_runs best-effort persistence ---

    def test_cli_run_recorded_on_success(self) -> None:
        """cli_runs table records the run with correct counters and exit_code."""
        main(["--frames", "5", "--db-path", self.db_path, "--reset-db"])
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.execute("SELECT frames_processed, frames_persisted, exit_code, summary_json FROM cli_runs")
            row = cur.fetchone()
            self.assertEqual(row[0], 5)
            self.assertEqual(row[1], 5)
            self.assertEqual(row[2], 0)
            summary = json.loads(row[3])
            self.assertEqual(summary["frames_processed"], 5)
            self.assertEqual(summary["exit_code"], 0)
        finally:
            conn.close()

    def test_cli_run_recorded_on_validation_failure(self) -> None:
        """cli_runs is recorded even when exit code is 3 (best-effort)."""
        import pilot.telemetry_source as ts_module

        original_next = ts_module.TelemetrySource.next_frame

        def bad_frame(self_src):
            frame = original_next(self_src)
            frame["temperature_c"] = 999.0
            return frame

        with patch.object(ts_module.TelemetrySource, "next_frame", bad_frame):
            exit_code = main(["--frames", "3", "--db-path", self.db_path, "--reset-db"])
        self.assertEqual(exit_code, 3)

        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.execute("SELECT exit_code, frames_processed, frames_persisted FROM cli_runs")
            row = cur.fetchone()
            self.assertEqual(row[0], 3)
            self.assertEqual(row[1], 3)
            self.assertEqual(row[2], 0)
        finally:
            conn.close()

    def test_cli_run_not_recorded_on_persistence_fatal(self) -> None:
        """cli_runs is NOT recorded when PersistenceFatalError occurs (exit code 4)."""
        import pilot.ingestion as ingestion_module

        with patch.object(ingestion_module.PersistenceManager, "record_frame",
                          side_effect=PersistenceFatalError("Simulated fatal")):
            exit_code = main(["--frames", "3", "--db-path", self.db_path, "--reset-db"])
        self.assertEqual(exit_code, 4)

        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.execute("SELECT COUNT(*) FROM cli_runs")
            self.assertEqual(cur.fetchone()[0], 0)
        finally:
            conn.close()

    # --- Gap 5 (remaining): Exit code 5 — unexpected internal error ---

    def test_exit_code_5_on_unexpected_internal_error(self) -> None:
        """An unexpected exception (not UsageError/ValidationError/Persistence*) 
        reaches the general except boundary and main() returns exit code 5.
        Resources are closed via the finally cleanup."""
        import pilot.ingestion as ingestion_module

        close_called = []

        original_close = ingestion_module.IngestionService.close

        def tracking_close(self_ing):
            close_called.append(True)
            original_close(self_ing)

        with patch.object(ingestion_module.IngestionService, "process_frame",
                          side_effect=RuntimeError("Simulated internal crash")), \
             patch.object(ingestion_module.IngestionService, "close", tracking_close):
            exit_code = main(["--frames", "3", "--db-path", self.db_path, "--reset-db"])

        self.assertEqual(exit_code, 5)
        self.assertTrue(close_called, "ingestion.close() must be called via finally cleanup")


if __name__ == "__main__":
    unittest.main()
