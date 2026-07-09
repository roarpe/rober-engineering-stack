"""Core data models for the telemetry ingestion pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class Status(str, Enum):
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    FAULT = "FAULT"
    MAINTENANCE = "MAINTENANCE"


class QualityCode(str, Enum):
    GOOD = "GOOD"
    BAD_DATA = "BAD_DATA"
    NO_DATA = "NO_DATA"


class ContractValidation(str, Enum):
    PASS = "PASS"
    REJECTED_SCHEMA = "REJECTED_SCHEMA"
    REJECTED_RANGE = "REJECTED_RANGE"
    REJECTED_MONOTONICITY = "REJECTED_MONOTONICITY"


class ValidationClassification(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    ANOMALOUS = "ANOMALOUS"
    NO_DATA = "NO_DATA"


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    INFO = "INFO"


class AlarmCode(str, Enum):
    INPUT_OUT_OF_RANGE = "INPUT_OUT_OF_RANGE"
    COUNTER_REGRESSION = "COUNTER_REGRESSION"
    TIMESTAMP_REGRESSION = "TIMESTAMP_REGRESSION"
    THERMAL_OVER_LIMIT = "THERMAL_OVER_LIMIT"
    VIBRATION_OVER_LIMIT = "VIBRATION_OVER_LIMIT"
    COMMUNICATION_WARNING = "COMMUNICATION_WARNING"
    COMMUNICATION_LOSS = "COMMUNICATION_LOSS"
    QUALITY_BAD_DATA = "QUALITY_BAD_DATA"
    QUALITY_NO_DATA = "QUALITY_NO_DATA"


class EventType(str, Enum):
    ACTIVATE = "ACTIVATE"
    CLEAR = "CLEAR"
    INFO = "INFO"


@dataclass(slots=True)
class TelemetryFrame:
    frame_id: str
    timestamp_utc: int
    temperature_c: Optional[float]
    vibration_mm_s: Optional[float]
    cycle_count: Optional[int]
    status: Status
    quality_code: QualityCode
    diagnostic_notes: Optional[str] = None
    contract_validation: ContractValidation = ContractValidation.PASS


@dataclass(slots=True)
class ValidationResult:
    frame: Optional[TelemetryFrame]
    is_valid: bool
    reason: Optional[str]
    violations: List[str]
    classification: ValidationClassification

    @property
    def is_ingestable(self) -> bool:
        return self.classification in {
            ValidationClassification.VALID,
            ValidationClassification.ANOMALOUS,
        }

    @property
    def is_no_data(self) -> bool:
        return self.classification == ValidationClassification.NO_DATA


@dataclass(slots=True)
class EnrichedFrame:
    frame: TelemetryFrame
    ingested_at: int
    contract_validation: ContractValidation
    persistence_id: int


@dataclass(slots=True)
class Alarm:
    code: AlarmCode
    severity: Severity
    activated_at: int
    cleared_at: Optional[int] = None
    first_out: bool = False
    details: Dict[str, Any] = field(default_factory=dict)
    recovery_frames: int = 0


@dataclass(slots=True)
class DiagnosticEvent:
    event_type: EventType
    alarm: Alarm
    frame_id: Optional[str]
    occurred_at: int
    context: Dict[str, Any]


@dataclass(slots=True)
class DiagnosticState:
    active_alarms: Dict[AlarmCode, Alarm] = field(default_factory=dict)
    first_out_code: Optional[AlarmCode] = None
    heartbeat_miss_count: int = 0
    frames_since_recovery: int = 0


@dataclass(slots=True)
class WatchdogSnapshot:
    missed_heartbeats: int
    communication_recovery_frames: int
    measurement_recovery_frames: int


@dataclass(slots=True)
class CliCounters:
    frames_processed: int = 0
    frames_persisted: int = 0
    frames_rejected_schema: int = 0
    frames_rejected_range: int = 0
    frames_rejected_monotonicity: int = 0
    no_data_count: int = 0
    anomalous_count: int = 0


@dataclass(slots=True)
class CliSummary:
    frames_processed: int
    frames_persisted: int
    frames_rejected_schema: int
    frames_rejected_range: int
    frames_rejected_monotonicity: int
    no_data_count: int
    active_alarms: List[Dict[str, Any]]
    exit_code: int


def build_summary(
    counters: CliCounters,
    active_alarms: Dict[AlarmCode, Alarm],
    exit_code: int,
) -> CliSummary:
    return CliSummary(
        frames_processed=counters.frames_processed,
        frames_persisted=counters.frames_persisted,
        frames_rejected_schema=counters.frames_rejected_schema,
        frames_rejected_range=counters.frames_rejected_range,
        frames_rejected_monotonicity=counters.frames_rejected_monotonicity,
        no_data_count=counters.no_data_count,
        active_alarms=[
            {
                "code": alarm.code.value,
                "severity": alarm.severity.value,
                "activated_at": alarm.activated_at,
                "cleared_at": alarm.cleared_at,
                "first_out": alarm.first_out,
            }
            for alarm in active_alarms.values()
            if alarm.cleared_at is None
        ],
        exit_code=exit_code,
    )
