"""SQLite persistence layer implementing the approved schema."""

from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Iterable, Optional

from .exceptions import PersistenceFatalError, PersistenceRetryableError
from .models import CliSummary, DiagnosticEvent, TelemetryFrame

RETRYABLE_MESSAGES = {"database is locked", "disk I/O error"}
RETRY_WAIT_SECONDS = 0.01

SCHEMA_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS telemetry_frames (
        frame_id TEXT PRIMARY KEY,
        timestamp_utc INTEGER NOT NULL,
        temperature_c REAL NOT NULL,
        vibration_mm_s REAL NOT NULL,
        cycle_count INTEGER NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('IDLE','RUNNING','FAULT','MAINTENANCE')),
        quality_code TEXT NOT NULL CHECK(quality_code IN ('GOOD','BAD_DATA')),
        contract_validation TEXT NOT NULL CHECK(contract_validation IN ('PASS')),
        ingested_at INTEGER NOT NULL,
        diagnostic_notes TEXT
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_frames_timestamp ON telemetry_frames(timestamp_utc)",
    """
    CREATE TABLE IF NOT EXISTS diagnostic_events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL CHECK(event_type IN ('ACTIVATE','CLEAR','INFO')),
        alarm_code TEXT NOT NULL,
        severity TEXT NOT NULL CHECK(severity IN ('CRITICAL','MAJOR','MINOR','INFO')),
        frame_id TEXT,
        occurred_at INTEGER NOT NULL,
        first_out INTEGER NOT NULL CHECK(first_out IN (0,1)),
        details_json TEXT NOT NULL,
        FOREIGN KEY(frame_id) REFERENCES telemetry_frames(frame_id) ON DELETE SET NULL
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_diag_code ON diagnostic_events(alarm_code)",
    """
    CREATE TABLE IF NOT EXISTS cli_runs (
        run_id INTEGER PRIMARY KEY AUTOINCREMENT,
        started_at INTEGER NOT NULL,
        completed_at INTEGER,
        frames_processed INTEGER NOT NULL,
        frames_persisted INTEGER NOT NULL,
        frames_rejected_schema INTEGER NOT NULL,
        frames_rejected_range INTEGER NOT NULL,
        frames_rejected_monotonicity INTEGER NOT NULL,
        no_data_count INTEGER NOT NULL,
        exit_code INTEGER NOT NULL,
        summary_json TEXT NOT NULL
    )
    """,
]

DROP_STATEMENTS = [
    "DROP TABLE IF EXISTS diagnostic_events",
    "DROP TABLE IF EXISTS cli_runs",
    "DROP TABLE IF EXISTS telemetry_frames",
]


class PersistenceManager:
    """Manages SQLite connection, schema, and transactions for the pilot."""

    def __init__(self, db_path: str | Path) -> None:
        self._db_path = str(db_path)
        self._connection: Optional[sqlite3.Connection] = None

    def __enter__(self) -> "PersistenceManager":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def connect(self) -> None:
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path)
            self._connection.execute("PRAGMA foreign_keys=ON")
            self._connection.row_factory = sqlite3.Row

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def ensure_schema(self) -> None:
        self.connect()
        assert self._connection is not None
        for statement in SCHEMA_STATEMENTS:
            self._connection.execute(statement)
        self._connection.commit()

    def reset_schema(self) -> None:
        self.connect()
        assert self._connection is not None
        for statement in DROP_STATEMENTS:
            self._connection.execute(statement)
        self._connection.commit()
        for statement in SCHEMA_STATEMENTS:
            self._connection.execute(statement)
        self._connection.commit()

    def record_frame(self, frame: TelemetryFrame, ingested_at_ms: int) -> int:
        query = (
            "INSERT INTO telemetry_frames "
            "(frame_id, timestamp_utc, temperature_c, vibration_mm_s, cycle_count, "
            "status, quality_code, contract_validation, ingested_at, diagnostic_notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )
        params = (
            frame.frame_id,
            frame.timestamp_utc,
            frame.temperature_c,
            frame.vibration_mm_s,
            frame.cycle_count,
            frame.status.value,
            frame.quality_code.value,
            frame.contract_validation.value,
            ingested_at_ms,
            frame.diagnostic_notes,
        )
        self._execute_with_retry(query, params)
        assert self._connection is not None
        cursor = self._connection.execute(
            "SELECT rowid FROM telemetry_frames WHERE frame_id = ?", (frame.frame_id,)
        )
        row = cursor.fetchone()
        return row[0] if row else 0

    def record_diagnostic_events(self, events: Iterable[DiagnosticEvent]) -> None:
        for event in events:
            query = (
                "INSERT INTO diagnostic_events "
                "(event_type, alarm_code, severity, frame_id, occurred_at, first_out, details_json) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)"
            )
            params = (
                event.event_type.value,
                event.alarm.code.value,
                event.alarm.severity.value,
                event.frame_id,
                event.occurred_at,
                1 if event.alarm.first_out else 0,
                json.dumps(event.context, sort_keys=True, default=str),
            )
            self._execute_with_retry(query, params)

    def record_cli_run(
        self,
        summary: CliSummary,
        started_at_ms: int,
        completed_at_ms: int,
    ) -> None:
        query = (
            "INSERT INTO cli_runs "
            "(started_at, completed_at, frames_processed, frames_persisted, "
            "frames_rejected_schema, frames_rejected_range, frames_rejected_monotonicity, "
            "no_data_count, exit_code, summary_json) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )
        payload = {
            "frames_processed": summary.frames_processed,
            "frames_persisted": summary.frames_persisted,
            "frames_rejected_schema": summary.frames_rejected_schema,
            "frames_rejected_range": summary.frames_rejected_range,
            "frames_rejected_monotonicity": summary.frames_rejected_monotonicity,
            "no_data_count": summary.no_data_count,
            "active_alarms": summary.active_alarms,
            "exit_code": summary.exit_code,
        }
        params = (
            started_at_ms,
            completed_at_ms,
            summary.frames_processed,
            summary.frames_persisted,
            summary.frames_rejected_schema,
            summary.frames_rejected_range,
            summary.frames_rejected_monotonicity,
            summary.no_data_count,
            summary.exit_code,
            json.dumps(payload, sort_keys=True, default=str),
        )
        self._execute_with_retry(query, params)

    def _execute_with_retry(self, query: str, params: tuple) -> None:
        assert self._connection is not None
        attempt = 0
        while True:
            try:
                self._connection.execute("BEGIN")
                self._connection.execute(query, params)
                self._connection.commit()
                return
            except sqlite3.IntegrityError as exc:
                self._connection.rollback()
                raise PersistenceFatalError(str(exc)) from exc
            except sqlite3.OperationalError as exc:
                self._connection.rollback()
                if any(msg in str(exc) for msg in RETRYABLE_MESSAGES) and attempt == 0:
                    attempt += 1
                    time.sleep(RETRY_WAIT_SECONDS)
                    continue
                if attempt > 0:
                    raise PersistenceFatalError(str(exc)) from exc
                raise PersistenceRetryableError(str(exc)) from exc


__all__ = ["PersistenceManager"]
