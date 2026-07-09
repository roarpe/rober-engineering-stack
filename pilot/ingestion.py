"""Ingestion service orchestrating validation, diagnostics, and persistence."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .diagnostics import DiagnosticsEngine
from .exceptions import PersistenceFatalError, PersistenceRetryableError
from .models import (
    CliCounters,
    ContractValidation,
    DiagnosticEvent,
    EnrichedFrame,
    ValidationClassification,
    ValidationResult,
    WatchdogSnapshot,
    build_summary,
)
from .persistence import PersistenceManager
from .utils.clock import Clock, SystemClock
from .validator import Validator
from .watchdog import WatchdogMonitor

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class IngestionService:
    validator: Validator
    diagnostics: DiagnosticsEngine
    persistence: PersistenceManager
    clock: Clock = SystemClock()
    watchdog: WatchdogMonitor = field(default_factory=WatchdogMonitor)
    counters: CliCounters = field(default_factory=CliCounters)
    _started_at_ms: int = 0

    def start(self) -> None:
        self._started_at_ms = self.clock.utc_ms()
        self.persistence.ensure_schema()

    def process_frame(self, frame_payload: Dict[str, object]) -> List[DiagnosticEvent]:
        LOGGER.debug("event=ingestion_start frame_id=%s", frame_payload.get("frame_id"))
        result = self.validator.validate(frame_payload)
        snapshot = self._observe_watchdog(result)
        events = self.diagnostics.evaluate(result, snapshot)
        self._update_counters(result, events)

        if result.is_ingestable and result.frame:
            ingested_at = self.clock.utc_ms()
            persistence_id = self.persistence.record_frame(result.frame, ingested_at)
            enriched = EnrichedFrame(
                frame=result.frame,
                ingested_at=ingested_at,
                contract_validation=result.frame.contract_validation,
                persistence_id=persistence_id,
            )
            LOGGER.info(
                "event=frame_ingested frame_id=%s contract_validation=PASS persistence_id=%d",
                enriched.frame.frame_id,
                enriched.persistence_id,
            )
        elif result.is_no_data and result.frame:
            LOGGER.info("event=no_data_heartbeat frame_id=%s", result.frame.frame_id)
        else:
            LOGGER.warning(
                "event=frame_rejected reason=%s frame_id=%s",
                result.reason,
                frame_payload.get("frame_id"),
            )

        if events:
            self.persistence.record_diagnostic_events(events)
            for event in events:
                if event.event_type.value == "ACTIVATE":
                    LOGGER.warning(
                        "event=alarm_activated code=%s severity=%s first_out=%s frame_id=%s",
                        event.alarm.code.value,
                        event.alarm.severity.value,
                        event.alarm.first_out,
                        event.frame_id,
                    )
                elif event.event_type.value == "CLEAR":
                    LOGGER.info(
                        "event=alarm_cleared code=%s severity=%s frame_id=%s",
                        event.alarm.code.value,
                        event.alarm.severity.value,
                        event.frame_id,
                    )
                elif event.event_type.value == "INFO":
                    LOGGER.info(
                        "event=diagnostic_info code=%s frame_id=%s",
                        event.alarm.code.value,
                        event.frame_id,
                    )

        return events

    def _observe_watchdog(self, result: ValidationResult) -> WatchdogSnapshot:
        timestamp = result.frame.timestamp_utc if result.frame else None
        if timestamp is None:
            LOGGER.debug("event=watchdog_skip reason=no_timestamp")
            return self.watchdog.observe(None, result.classification)

        snapshot = self.watchdog.observe(timestamp, result.classification)
        LOGGER.debug(
            "event=watchdog_update missed=%s comm_recovery=%s meas_recovery=%s",
            snapshot.missed_heartbeats,
            snapshot.communication_recovery_frames,
            snapshot.measurement_recovery_frames,
        )
        return snapshot

    def _update_counters(self, result: ValidationResult, events: List[DiagnosticEvent]) -> None:
        self.counters.frames_processed += 1

        if result.is_ingestable:
            self.counters.frames_persisted += 1
            if result.classification == ValidationClassification.ANOMALOUS:
                self.counters.anomalous_count += 1
        elif result.is_no_data:
            self.counters.no_data_count += 1
        else:
            reason = result.reason or ""
            if "range" in reason.lower() or "temperature" in reason.lower() or "vibration" in reason.lower():
                self.counters.frames_rejected_range += 1
            elif "timestamp" in reason.lower() or "cycle" in reason.lower() or "monotonic" in reason.lower():
                self.counters.frames_rejected_monotonicity += 1
            else:
                self.counters.frames_rejected_schema += 1

    def build_summary(self, exit_code: int):
        return build_summary(
            self.counters,
            self.diagnostics.active_alarms,
            exit_code,
        )

    def finalize(self, exit_code: int) -> None:
        summary = self.build_summary(exit_code)
        try:
            self.persistence.record_cli_run(
                summary,
                self._started_at_ms,
                self.clock.utc_ms(),
            )
        except (PersistenceFatalError, PersistenceRetryableError) as exc:
            LOGGER.error("event=cli_run_persist_failed error=%s", exc)

    def close(self) -> None:
        self.persistence.close()


def build_ingestion_service(db_path: str, clock: Optional[Clock] = None) -> IngestionService:
    clock = clock or SystemClock()
    persistence = PersistenceManager(db_path)
    persistence.ensure_schema()
    validator = Validator(clock=clock)
    diagnostics = DiagnosticsEngine()
    return IngestionService(
        validator=validator,
        diagnostics=diagnostics,
        persistence=persistence,
        clock=clock,
    )
