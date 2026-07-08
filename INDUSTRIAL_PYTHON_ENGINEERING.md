# INDUSTRIAL_PYTHON_ENGINEERING.md

Software Engineer — Skill `industrial-python-engineering`

## 1. Metadata & Preconditions

- **Project:** Industrial Machine Telemetry Ingestion & Diagnostics Pipeline
- **Skill contract:** `skills/industrial-python-engineering/SKILL.md`
- **Owner:** Software Engineer (data-engineering module)
- **Inputs consumed:** `PILOT_PROJECT_PROPOSAL.md`, `REQUIREMENTS_GATE_REPORT.md`, `INDUSTRIAL_COMMUNICATIONS_DESIGN.md`, `MACHINE_DIAGNOSTICS.md`, `AGENTS.md`, `ARCHITECTURE.md`, `modules/data-engineering/MODULE.md`.
- **Requirements Quality:** PASS confirmed (`REQUIREMENTS_GATE_REPORT.md`).
- **Upstream artifacts:** `INDUSTRIAL_COMMUNICATIONS_DESIGN.md` and `MACHINE_DIAGNOSTICS.md` committed (HEAD `2e3ac25`).
- **Skill trigger:** Active `data-engineering` module with Python pipeline and CLI (Section 21 of the proposal).
- **Scope:** Define the Python engineering design only. No code, tests, or database files are produced in this phase.

## 2. Objective & Scope

Provide a complete, proportional Python engineering design that enables later implementation of the telemetry ingestion and diagnostics pipeline while resolving RQF-003 (CLI exit/error handling) and RQF-004 (SQLite schema, lifecycle, cleanup). The design must:

1. Consume the authoritative OT/data interface contract (`INDUSTRIAL_COMMUNICATIONS_DESIGN.md`).
2. Consume the diagnostics strategy (`MACHINE_DIAGNOSTICS.md`).
3. Specify architecture, module boundaries, data models, validation flow, persistence, logging, error handling, CLI behavior, and testing approach.
4. Remain stdlib-only (Python 3.14.4) and proportional to the pilot.

## 3. Constraints & Environment

| Constraint | Source | Impact |
|---|---|---|
| Windows host, Python 3.14.4 stdlib only | `ENVIRONMENT_AUDIT.md`, proposal §5 | No external deps; rely on `argparse`, `sqlite3`, `logging`, `time/datetime`, `uuid`, `json`, `tempfile`, `unittest`. |
| No hardware / PLC | Proposal §6 | Telemetry source fully simulated; no external IO beyond SQLite file. |
| `data-engineering` module owns pipeline & CLI | Proposal §8-9 | Software Engineer designs ingestion/diagnostics CLI without activating `software-development`. |
| Contracts upstream frozen | ICD & Diagnostics artifacts | Implementation must honor tag names, enums, thresholds, watchdog/recovery policy (two consecutive frames). |

## 4. Architecture Overview

Synchronous, single-process pipeline with clear module boundaries:

```
+----------------------+      +--------------------+      +------------------+
| telemetry_source     | ---> | validator          | ---> | ingestion_service |
| (producer shim)      |      | (schema+semantics) |      | (persist + enrich)|
+----------------------+      +--------------------+      +------------------+
                                             |                        |
                                             v                        v
                                     +--------------+        +------------------+
                                     | diagnostics  |<------>| persistence_layer |
                                     | engine       |        | (SQLite manager)  |
                                     +--------------+                |
                                             ^                        v
                                             |                +------------------+
                                             +----------------| cli_runner       |
                                                              +------------------+
```

- Control flow is linear per frame; no concurrency required.
- CLI orchestrates lifecycle: spin up components, process N frames, flush summaries, exit with defined codes.
- Diagnostics engine consumes validator outcomes + telemetry + persistence snapshots to raise/clear alarms per `MACHINE_DIAGNOSTICS.md`.

## 5. Component Responsibilities & Dependencies

| Component | Responsibility | Depends On | Notes |
|---|---|---|---|
| `telemetry_source` | Produce deterministic frames that satisfy ICD cadence/fields (or intentionally violate for tests). | None (simulator). | Generates `quality_code`, `status`, `frame_id`, etc. |
| `validator` | Enforce schema, type, enum, timestamp, monotonicity, and range rules. Classifies frames as invalid vs. valid-but-anomalous; handles `NO_DATA`. | ICD contract. | Emits `ValidationResult` objects. |
| `ingestion_service` | Apply validator decisions, persist valid telemetry, record rejections, feed diagnostics. | Validator, persistence layer, diagnostics engine. | Never crashes on invalid frames. |
| `diagnostics_engine` | Implement taxonomy, thresholds, lifecycle (two-frame recovery, first-out, communication warnings/loss). | Diagnostics contract, ingestion service, telemetry metadata. | Emits `DiagnosticEvent` structures and maintains state machine. |
| `persistence_layer` | Own SQLite connection, migrations, transactions, cleanup. | `sqlite3`. | Provides DAO-style helpers (`record_frame`, `record_alarm_event`, `record_cli_run`). |
| `cli_runner` | Parse args, configure logging, coordinate pipeline, surface exit codes, print summaries. | All modules. | Entry point `python -m pilot.cli`. |

Dependencies are acyclic: CLI → (source, validator, ingestion, diagnostics, persistence). Diagnostics/persistence do not call CLI.

## 6. Data Models

Use `dataclasses` for structured records; summarized below:

| Model | Fields | Purpose |
|---|---|---|
| `TelemetryFrame` | `frame_id:str`, `timestamp_utc:int`, `temperature_c:Optional[float]`, `vibration_mm_s:Optional[float]`, `cycle_count:Optional[int]`, `status:Status`, `quality_code:QualityCode`, `diagnostic_notes:Optional[str]` | Mirrors ICD payload. Measurement fields become `Optional` solely to represent `NO_DATA`; validator enforces non-null for all other frames. |
| `ValidationResult` | `frame:TelemetryFrame`, `is_valid:bool`, `reason:Optional[str]`, `violations:list[str]`, `classification:Literal["INVALID","VALID","ANOMALOUS","NO_DATA"]` | Output of validator: `VALID` means contract-compliant and within operational band; `ANOMALOUS` means contract-compliant but requires diagnostics attention; `INVALID` violates contract; `NO_DATA` is the heartbeat exception. |
| `EnrichedFrame` | `frame:TelemetryFrame`, `ingested_at:int`, `contract_validation:ContractValidation`, `persistence_id:int` | Data persisted to SQLite + passed to diagnostics. |
| `DiagnosticState` | `active_alarms:dict[str, Alarm]`, `first_out_code:Optional[str]`, `heartbeat_miss_count:int`, `frames_since_recovery:int` | In-memory context for diagnostics engine. |
| `Alarm` | `code:str`, `severity:Severity`, `activated_at:int`, `cleared_at:Optional[int]`, `first_out:bool`, `details:dict` | Represents lifecycle per `MACHINE_DIAGNOSTICS.md`. |
| `DiagnosticEvent` | `event_type:Literal["ACTIVATE","CLEAR","INFO"]`, `alarm:Alarm`, `frame_id:str`, `context:dict` | Persisted/logged record of alarm transitions (including `NO_DATA` INFO entries). |
| `CliSummary` | `frames_processed:int`, `frames_persisted:int`, `frames_rejected_schema:int`, `frames_rejected_range:int`, `frames_rejected_monotonicity:int`, `no_data_count:int`, `active_alarms:list[Alarm]`, `exit_code:int` | Final output rendered by CLI. |

Enums mirror upstream contracts: `Status`, `QualityCode`, `ContractValidation`, `Severity`, `AlarmCode` (`INPUT_OUT_OF_RANGE`, `COUNTER_REGRESSION`, `TIMESTAMP_REGRESSION`, `THERMAL_OVER_LIMIT`, `VIBRATION_OVER_LIMIT`, `COMMUNICATION_WARNING`, `COMMUNICATION_LOSS`, `QUALITY_BAD_DATA`, `QUALITY_NO_DATA`).

## 7. Validation Pipeline

Validation is deterministic and ordered to maintain transparency:

1. **Schema existence:** Ensure required keys exist (except measurement fields when `quality_code=NO_DATA`). Missing required key → `INVALID:REJECTED_SCHEMA`.
2. **Type enforcement:** Convert numeric fields to float/int; reject NaN/Inf. Wrong type → `INVALID:REJECTED_SCHEMA`.
3. **Enum enforcement:** Validate `status` and `quality_code` against ICD enumerations.
4. **Timestamp checks:** Confirm integer milliseconds, monotonic vs. previous accepted frame, and current wall-clock freshness (≤5 seconds drift). Backwards or stale → `INVALID:TIMESTAMP_REGRESSION`.
5. **Cycle count logic:** Non-decreasing except immediately after `status=MAINTENANCE`, where a single reset to zero is permitted. Violations → `INVALID:COUNTER_REGRESSION`.
6. **Measurement handling:**
   - If `quality_code=NO_DATA`, measurement fields **must** be `null`; classification becomes `NO_DATA`, heartbeat counters reset, and frame is syntactically valid but ineligible for persistence.
   - Otherwise all numeric fields must be present; missing measurement → `INVALID:REJECTED_SCHEMA`.
7. **Contract range vs. diagnostic thresholds:**
   - Contractual ranges (temperature 0–120 °C, vibration 0–50 mm/s) define the **valid** operating window. Values outside these hard limits violate the interface and become `INVALID:REJECTED_RANGE` (discarded, logged, not persisted).
   - Diagnostic thresholds (e.g., MAJOR >100 °C) operate **within** the valid range. Frames inside the contract but crossing diagnostic limits are classified `ANOMALOUS` and remain valid for ingestion/persistence to drive alarms.
8. **Contract validation label:**
   - Invalid frames → `contract_validation=REJECTED_*` with cause stored.
   - Valid frames → `contract_validation=PASS`.

The validator returns `ValidationResult`; ingestion service persists only frames with `classification in {"VALID","ANOMALOUS"}` and `contract_validation=PASS`. `NO_DATA` frames skip persistence but generate INFO diagnostics events. Invalid frames never enter SQLite.

## 8. Diagnostics Integration Design

Diagnostics engine is a pure-Python state machine informed by `MACHINE_DIAGNOSTICS.md`:

- **Fault taxonomy & thresholds** are implemented verbatim: temperature (MINOR 90–100 °C, MAJOR >100 °C), vibration (MINOR 30–40 mm/s, MAJOR >40 mm/s), counter/timestamp regressions (MAJOR), `COMMUNICATION_WARNING/LOSS` (2 and 3 missed frames), `QUALITY_BAD_DATA` (MINOR), `QUALITY_NO_DATA` (INFO heartbeat), `INPUT_OUT_OF_RANGE` (MINOR), etc.
- **Activation:** Each incoming `EnrichedFrame` updates counters and may raise alarms. `NO_DATA` frames are handled as heartbeat-only events.
- **Communication watchdog ownership:** The validator timestamps every observation and updates a dedicated `WatchdogMonitor` (owned by the ingestion service) that tracks cadence, missed frames, and the recovery timer. Diagnostics engine consumes signals from this monitor rather than running its own timers, ensuring single ownership of temporal state.
- **Known-state recovery:**
  - *Communication recovery* occurs after the watchdog observes two consecutive frames (which may be `NO_DATA`) arriving within cadence; this clears `COMMUNICATION_WARNING/LOSS` alarms.
  - *Measurement availability recovery* occurs after two consecutive frames containing real measurements (`quality_code` in {`GOOD`,`BAD_DATA`}); only then can temperature/vibration-related alarms clear. The diagnostics engine separately tracks these two counters to honor both contracts.
- **Active state & first-out:** `Alarm` objects keep `first_out` flag; first MAJOR alarm after `status` transitions to `FAULT` or following a healthy run is latched and reported.
- **Automatic clear:** Alarm-specific recovery rules apply (e.g., thermal/vibration alarms clear after two measurement frames below MINOR threshold; counter/timestamp regressions clear after two monotonic frames). Heartbeat alarms depend solely on the communication recovery counter described above.
- **Context capture:** Every alarm activation/clear event stores `frame_id`, `timestamp_utc`, raw telemetry, `contract_validation`, `heartbeat_miss_count`, threshold details, and `first_out` flag before writing to SQLite/logging.

## 9. SQLite Persistence Design (RQF-004)

### 9.1 Schema Overview

| Table | Purpose |
|---|---|
| `telemetry_frames` | Persist valid telemetry frames (excluding `NO_DATA`). |
| `diagnostic_events` | Store alarm lifecycle & informational diagnostics (including `NO_DATA`). |
| `cli_runs` | Capture per-run summaries (frames processed, counts, exit code) for traceability. |

### 9.2 Table Definitions

```sql
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
);
CREATE INDEX IF NOT EXISTS idx_frames_timestamp ON telemetry_frames(timestamp_utc);

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
);
CREATE INDEX IF NOT EXISTS idx_diag_code ON diagnostic_events(alarm_code);

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
);
```

### 9.3 Constraints & Index Justification

- `telemetry_frames.frame_id` is the UUID provided by the producer; primary key prevents duplicates across runs.
- Only `GOOD`/`BAD_DATA` frames enter the table; `NO_DATA` is excluded per contract.
- Index on `timestamp_utc` supports chronological queries and diagnostics lookups.
- `diagnostic_events` references `telemetry_frames` when available; INFO events for `NO_DATA` intentionally store `frame_id=NULL` (per schema) while retaining full context— including the original `frame.frame_id` as `source_frame_id`—inside `details_json`, preserving traceability without violating FK constraints.

### 9.4 Connection, Transactions & Ownership

- `persistence_layer` exposes a context manager `with db_manager(db_path) as conn:` that enables `PRAGMA foreign_keys=ON`. WAL mode is **not** required for this single-process pilot and therefore omitted to keep configuration simple.
- Each CLI run:
  1. Opens one connection for the entire run.
  2. Applies schema migrations (idempotent `CREATE TABLE IF NOT EXISTS`).
  3. Uses implicit transactions (`sqlite3` autocommit). For each persistence call the code executes `BEGIN`/`COMMIT` via `conn.execute("BEGIN")` … `conn.commit()`. If an `sqlite3.OperationalError` whose message matches `"database is locked"` or `"disk I/O error"` occurs, the ingestion service immediately issues `conn.rollback()`, waits briefly, and retries the transaction exactly once. Any other `OperationalError`, or a second failure of the same statement, is treated as fatal immediately.
  4. Integrity errors (`sqlite3.IntegrityError`)—including duplicate `frame_id` attempts—indicate contract violations. They trigger a rollback, raise `PersistenceFatalError`, and end the run with exit code 4. Duplicate frames are therefore handled consistently and never silently ignored.
- Connections close gracefully during CLI shutdown, even on exceptions (context manager or `try/finally`).

### 9.5 Behavior Between Executions

- Default DB path: `./var/pilot.sqlite` (created lazily). Data persists between CLI runs to inspect historical behavior.
- CLI options:
  - `--db-path PATH` to override location (e.g., for tests).
  - `--reset-db` to drop all tables before run (implemented as `DROP TABLE IF EXISTS ...` + recreate).
- Frame IDs remain unique globally; reuse across runs is prevented by the primary key constraint, and any attempt to insert a duplicate immediately raises `PersistenceFatalError` (exit code 4) per §9.4.

### 9.6 Test Isolation & Cleanup (also see §10)

- Unit tests use temporary directories or in-memory URIs (`sqlite3.connect('file:memdb1?mode=memory&cache=shared', uri=True)`), running schema migrations per test.
- CLI end-to-end tests pass `--db-path <tempfile>` and `--reset-db` to start clean; tear down removes the temporary file, ensuring no leakage between tests.

## 10. Test Isolation & Strategy

- **Temporary databases:** Each test case receives its own path via `tempfile.TemporaryDirectory`; CLI parameterization ensures no shared state.
- **Schema setup:** Tests call `db_manager.ensure_schema()` before inserting fixtures to avoid reliance on migration side effects.
- **Watchdog timing:** Clock abstraction remains to simulate cadence deterministically in tests. Production uses the real `time.monotonic()`; there is no alternate heartbeat timeout argument, preventing multiple sources of truth.
- **Two-frame recovery:** Tests feed sequences demonstrating alarm activation and clearance after exactly two nominal frames.
- **`NO_DATA` handling:** Dedicated tests confirm such frames increment heartbeat, do not persist telemetry rows, yet produce INFO diagnostics events.
- **Six tests from proposal:**
  - `test_telemetry_source`: Validates generator respects ICD contract.
  - `test_ingestion_valid`: Confirms valid frames persist & summaries match.
  - `test_ingestion_invalid`: Injects schema/range violations; ensures rejections logged without crashing.
  - `test_diagnostics_thresholds`: Exercises MAJOR/MINOR transitions and first-out latching.
  - `test_diagnostics_no_alarm`: Ensures normal data does not raise alarms.
  - `test_cli_end_to_end`: Runs CLI with limited frames, asserts exit code 0, verifies DB rows & summary.

## 11. CLI Design (RQF-003 Closure)

### 11.1 Arguments

| Argument | Default | Description |
|---|---|---|
| `--frames N` | `100` | Number of frames to simulate per run; must be ≥1. |
| `--db-path PATH` | `./var/pilot.sqlite` | SQLite file location. |
| `--reset-db` | `False` | If set, drop/recreate schema before processing. |
| `--log-level LEVEL` | `INFO` | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |

### 11.2 Execution Flow

1. Parse args; invalid inputs (e.g., negative frames) raise `UsageError` → exit code 2.
2. Configure logging (`logging.basicConfig`, structured format `timestamp level name key=value ...`).
3. Initialize DB (optionally reset).
4. Initialize diagnostics state, counters, telemetry source, validator.
5. Loop `N` frames:
   - Generate frame.
   - Validate and classify.
   - Update watchdog monitor (which tracks cadence and measurement availability).
   - For `VALID` frames: persist + feed diagnostics.
   - For `ANOMALOUS` frames: persist, flag severity inputs to diagnostics.
   - For invalid frames: log rejection, update counters, continue.
   - For `NO_DATA`: log INFO, emit diagnostic event, skip persistence while still updating the watchdog’s communication counter.
6. After loop, diagnostics rely on the actual frames observed; **no synthetic frames are generated**. Any alarms still active remain so until future CLI runs process additional frames.
7. Persist `cli_runs` summary row.
8. Render textual summary to stdout (counts, active alarms, DB path) and exit with appropriate code.

### 11.3 Exit Codes

| Code | Meaning | Conditions |
|---|---|---|
| `0` | Success | Pipeline executed, DB updated, summary printed (even if some frames invalid/anomalous). |
| `2` | Usage error | Argument parsing/validation failures. |
| `3` | Validation failure at run level | The run processed at least one frame but **zero** frames reached the "valid or anomalous" state (e.g., systemic configuration error causes every frame to violate the ICD). This indicates misconfiguration rather than a transient ingestion failure. |
| `4` | Persistence error | SQLite connection/constraint error that prevents commits after retry. |
| `5` | Unexpected internal error | Unhandled exception; CLI logs stack trace and exits. |

Per RQF-003, individual frame rejections do **not** cause non-zero exit codes unless they lead to the run-level failure scenarios above.

## 12. Error Handling Strategy

- **Custom exceptions:**
  - `UsageError` → CLI exit 2.
  - `ValidationError` (non-fatal) → logged, counted, frame skipped.
  - `PersistenceRetryableError` (e.g., transient `OperationalError`) → ingestion retries once; if the second attempt fails, escalates to `PersistenceFatalError` and exits 4.
  - `PersistenceFatalError` (`IntegrityError`, repeated operational failure) → exit 4 without further retries and without guaranteeing that `cli_runs` was recorded.
  - `PipelineInternalError` → logged as ERROR, exit 5.
- **Logging vs. stdout:** CLI prints human-friendly summary on stdout; errors/warnings go to stderr via logging module.
- **Transaction control:** Validation errors do not open transactions. Persistence errors roll back only the affected frame; CLI may continue unless DB becomes unusable.

## 13. Logging & Observability

- Use stdlib `logging` configured once by CLI.
- Format: `%(asctime)s level=%(levelname)s logger=%(name)s event=%(message)s key=value...` to keep structured `key=value` pairs.
- Mandatory events:
  - Frame ingestion success (`event=frame_ingested frame_id=... contract_validation=PASS`).
  - Frame rejection with cause (`event=frame_rejected reason=REJECTED_SCHEMA`).
  - Heartbeat warning/loss transitions and clearances.
  - Alarm activation/clear with severity + first_out flag.
  - CLI start/end plus exit code.
- Logging levels: `INFO` for nominal operations; `WARNING` for frame rejections/heartbeat warnings; `ERROR` for persistence/internal failures. When a fatal persistence error occurs before the CLI can write `cli_runs`, the log explicitly states that the summary could not be recorded, acknowledging that `cli_runs` entries are best-effort rather than guaranteed.

## 14. Configuration & Dependencies

- **Configuration sources:** CLI args overriding defaults; optional env var `PILOT_DB_PATH` if `--db-path` omitted (CLI precedence: arg > env > default). Secrets are not required.
- **Dependencies (stdlib):** `argparse`, `dataclasses`, `enum`, `logging`, `time`, `datetime`, `uuid`, `json`, `sqlite3`, `tempfile`, `pathlib`, `typing`, `unittest`. No third-party modules.

## 15. Implementation Plan

1. **Skeleton package (`pilot/`)** with modules: `telemetry_source.py`, `validator.py`, `ingestion.py`, `diagnostics.py`, `persistence.py`, `cli.py`, `utils/clock.py`.
2. **Implement data models and enums** (shared `models.py`).
3. **Validator & tests** (`test_telemetry_source`, `test_ingestion_invalid`).
4. **Persistence layer** (schema creation, transactions) + `test_ingestion_valid`.
5. **Diagnostics engine** (state machine, first-out) + `test_diagnostics_thresholds` & `test_diagnostics_no_alarm`.
6. **CLI orchestration** tying everything together, including logging & exit codes + `test_cli_end_to_end`.
7. **Test utilities** (fake clock, temp DB) to support isolation.
8. **Documentation updates** only if required; then Implementation Review will verify adherence.

## 16. Risks & Decision Readiness

- **SQLite path collisions:** Mitigated by `--reset-db` and per-run `cli_runs` metadata. Reversible.
- **Clock abstraction complexity:** Chosen minimal injection; reversible.
- **No blocking decisions** remain; all open items have clear owners and reversible mitigation. Decision Readiness Gate not required.

---

This document provides the authoritative Python engineering design for Phase 11B implementation. All subsequent development and QA activities must adhere to these conventions, contracts, and exit criteria.
