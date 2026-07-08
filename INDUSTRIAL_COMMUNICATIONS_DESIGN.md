# INDUSTRIAL_COMMUNICATIONS_DESIGN.md

Industrial Automation Engineer — Skill `industrial-communications-design`

## 1. Metadata & Preconditions

- **Project:** Industrial Machine Telemetry Ingestion & Diagnostics Pipeline
- **Skill contract:** `skills/industrial-communications-design/SKILL.md`
- **Owner:** Industrial Automation Engineer (producer-side OT domain)
- **Consumers:** Software Engineer (data pipeline implementation), QA & Debug Engineer (verification), Engineering Architect (coherence)
- **Requirements Quality status:** PASS per `REQUIREMENTS_GATE_REPORT.md` (2026-07-08). No Decision Readiness gate required because no blocking decisions were identified.
- **Scope:** Single cross-domain interface between the simulated OT telemetry source and the Python data-ingestion pipeline (Sections 17-18 of `PILOT_PROJECT_PROPOSAL.md`). No physical PLC, fieldbus or hardware exists in this pilot; design remains proportional and purely software-simulated.

### 1.1 Design Decisions & Assumptions

- **2 s frame cadence (±200 ms jitter):** Chosen so diagnostics can observe state changes without generating excessive simulated data. Because cadence is a constant in configuration, Software Engineer can change it later without architectural impact, keeping the decision reversible.
- **Single in-process transport:** The interface is modeled as an API boundary, not a network link, which is proportional to a pilot without hardware. Should future phases demand fieldbus semantics, this contract can be re-hosted on a transport without rewriting telemetry semantics.
- **Enumerated status model (`IDLE`, `RUNNING`, `FAULT`, `MAINTENANCE`):** Keeps automation states explicit while avoiding a larger mode matrix. Enumerations can be extended compatibly if more modes become necessary.
- **Quality signaling via `quality_code` + diagnostics notes:** Separates producer confidence from consumer validation, giving QA deterministic hooks while remaining optional for production implementations.
- **Two-frame recovery policy:** Any alarm clears only after two consecutive frames confirm the nominal condition, which keeps noise low yet is easy to override later if tighter responsiveness is required.

## 2. Interface Inventory

| ID | Producer | Consumer | Purpose | Ownership |
|---|---|---|---|---|
| ICD-OT-PIPELINE-001 | Simulated OT telemetry generator (Industrial Automation Engineer) | Data-ingestion service inside the pipeline (Software Engineer) | Deliver normalized telemetry frames so that the pipeline can validate, persist and diagnose machine behavior. | Contract owner: Industrial Automation Engineer. Implementation owner: Software Engineer.

## 3. Interface ICD-OT-PIPELINE-001 — Simulated OT → Data Pipeline

### 3.1 Contract Fields (11 mandatory attributes)

- **Producer:** `telemetry_source` module owned by Industrial Automation Engineer. It emits telemetry frames generated deterministically from the simulated machine model.
- **Consumer:** `ingestion` module owned by Software Engineer. It validates, persists and forwards telemetry frames to downstream diagnostics and CLI consumers.
- **Purpose:** Provide a single source of truth for machine state so that downstream modules can compute diagnostics, persistence, and CLI summaries without inventing signal semantics.
- **Data Contract:** Defined in §3.2; includes tag names, types, units, ranges, scaling rules, envelope metadata, and validation outcomes.
- **Ownership:** Industrial Automation Engineer owns the contract definition and versioning; Software Engineer owns consumer implementation and persistence. Changes require mutual review with Engineering Architect if they affect scope.
- **Update Model:** Push-style periodic frames. Producer emits one frame every **2 seconds** (configurable constant) even if values remain unchanged. Consumer must handle occasional jitter (±200 ms) without declaring failure.
- **Timing Expectations:**
  - New frame expected within 2.2 seconds of the previous frame.
  - Missing two consecutive frames (>4.4 seconds) elevates a communications warning that must be surfaced to diagnostics.
  - Frame timestamps must be monotonic (non-decreasing UTC milliseconds). Out-of-order frames are rejected.
- **Failure Behavior:** Detailed in §3.4. Invalid frames (schema, range, timestamp, monotonicity) are rejected with structured log entries; ingestion never crashes. Communication loss is surfaced as a diagnostics event after two missed frames.
- **Recovery Behavior:** On rejection, consumer requests the next scheduled frame (no retries of the invalid payload). Every alarm or warning clears **only after two consecutive frames** satisfy the nominal condition (including communications); counters reset once the second healthy frame is observed.
- **Diagnostics:** Producer sets `status` to reflect machine operating mode; ingestion adds `contract_validation` results. QA verifies via dedicated tests and runtime counters described in §3.5.
- **Verification Method:**
  - Automated test `test_telemetry_source` validates schema, ranges, timing, and monotonicity.
  - Automated test `test_ingestion_invalid` injects malformed frames to ensure rejection without crash.
  - Runtime self-check `telemetry_contract_self_check()` (to be implemented under Software Engineer ownership) periodically validates producer timestamps and frame cadence using the counters specified below.

### 3.2 Data Contract (Tags & Envelope)

| Field | Type | Units / Domain | Valid Range / Values | Resolution | Notes |
|---|---|---|---|---|---|
| `frame_id` | `str` (UUIDv4 text) | n/a | Unique per frame | n/a | Envelope identifier for traceability; generated by producer. |
| `timestamp_utc` | `int` | milliseconds since epoch | Monotonic, within ±1 second of system clock | 1 ms | Required for ordering. Consumer rejects backward timestamps. |
| `temperature_c` | `float` | °C | 0.0 – 120.0 | 0.1 | Represents simulated coolant or casing temperature. Values outside range flagged as MAJOR input fault. |
| `vibration_mm_s` | `float` | mm/s RMS | 0.0 – 50.0 | 0.01 | Derived magnitude of vibration sensor. >40 triggers MAJOR diagnostic; 30–40 triggers MINOR diagnostic. |
| `cycle_count` | `int` | cycles | 0 – 1,000,000 | 1 | Monotonic non-decreasing counter. Resets allowed only on simulated maintenance and must be declared via `status="MAINTENANCE"`. |
| `status` | `str` enum | {`IDLE`, `RUNNING`, `FAULT`, `MAINTENANCE`} | Must match enum; `FAULT` allowed only when paired with diagnostic reason. | n/a | Encodes current machine mode; used to contextualize alarms. |
| `quality_code` | `str` enum | {`GOOD`, `BAD_DATA`, `NO_DATA`} | Defaults to `GOOD`. | n/a | Communicates producer-side confidence. `BAD_DATA` means the producer detected corruption but still reports actual readings; **no clamping is applied**. `NO_DATA` denotes an intentional heartbeat frame where measurement values are `null` and must not be interpreted as zero. |
| `diagnostic_notes` | `str` or `null` | free text | ≤256 UTF-8 chars | n/a | Optional human-readable context for simulated anomalies (used only in test scenarios). |
| `contract_validation` | `str` enum | {`PASS`, `REJECTED_SCHEMA`, `REJECTED_RANGE`, `REJECTED_MONOTONICITY`} | Set by consumer only | n/a | Enables downstream diagnostics to distinguish ingestion issues. |

**Validation rules:**

1. Numeric fields must be finite (no NaN/Inf).
2. Missing required fields -> frame rejection.
3. Units are implied; conversions are not performed by consumer.
4. Producer never clamps values; it either emits the real reading (flagged via `quality_code`) or withholds the field. Consumer relies on the invalid/valid rules below to decide acceptance.
5. `cycle_count` strictly greater than or equal to previous frame unless `status=MAINTENANCE`, in which case it may reset to zero once.

#### Invalid vs. Anomalous Telemetry

- **Invalid telemetry** results from missing fields, wrong data types, NaN/Inf, backwards `timestamp_utc`, or `cycle_count` regression outside maintenance resets. These frames are rejected and never persisted.
- **Valid but anomalous telemetry** respects schema/monotonic rules yet exceeds diagnostic thresholds (e.g., high temperature). Such frames remain ingestible; they simply trigger diagnostics according to `MACHINE_DIAGNOSTICS.md`. This separation ensures that failure analysis distinguishes communication/contract defects from machine-behavior anomalies.

#### `NO_DATA` Semantics

- Frames marked with `quality_code=NO_DATA` are **syntactically valid** and count toward the watchdog cadence even though measurement fields are `null` (which is otherwise forbidden). The only exception to the “no nulls” rule is when every measurement is `null` and `quality_code=NO_DATA`.
- Consumer behavior:
  - Treat the frame as a heartbeat: reset the missed-frame counter and do **not** raise communication alarms.
  - Do not persist telemetry rows with `null` measurements; instead, record an INFO-level diagnostics event so downstream consumers know a heartbeat occurred without data.
  - These frames never trigger threshold-based alarms because there are no numeric values; however, repeated `NO_DATA` frames should be tracked so QA can spot modeling issues.
- Recovery: once two consecutive frames with actual measurements (`quality_code=GOOD` or `BAD_DATA`) arrive on time, the diagnostics subsystem considers the data stream fully recovered.

### 3.3 Synchronization, Timeouts & Watchdogs

- **Heartbeat watchdog:** Consumer maintains `heartbeat_missed_count`. Thresholds:
  - 0–1 misses: informational.
  - 2 consecutive misses: raise `COMMUNICATION_WARNING` diagnostic event.
  - ≥3 misses: escalate to `COMMUNICATION_LOSS` MAJOR alarm (Software Engineer will implement translation per diagnostics spec).
- **Timeouts:** Consumer rejects frames that arrive >5 seconds after `timestamp_utc` indicates they were produced (prevents stale data being ingested later).
- **Clock source:** Both producer and consumer share the same process clock; no NTP or distributed synchronization is required.

### 3.4 Failure & Recovery Behavior Matrix

| Scenario | Producer Action | Consumer Action | Recovery |
|---|---|---|---|
| Schema violation (missing field, wrong type) | Emit frame with `quality_code=BAD_DATA` and set `diagnostic_notes`. | Reject frame, log `REJECTED_SCHEMA`, increment `contract_validation` metric, do not persist. | Wait for next scheduled frame; no retry request issued. |
| Range violation (`temperature_c` or `vibration_mm_s`) | Send raw value with `quality_code=BAD_DATA`; no clamping allowed. | Reject frame, log `REJECTED_RANGE`, surface MINOR diagnostics entry `INPUT_OUT_OF_RANGE`. | Condition clears only after **two** consecutive valid frames fall back inside range. |
| `cycle_count` regression | Emit raw value and set `quality_code=BAD_DATA`. | Reject, log `REJECTED_MONOTONICITY`, raise MAJOR diagnostic `COUNTER_REGRESSION`. | Requires producer fix; alarm clears after two monotonic frames. |
| `timestamp_utc` regression or stale timestamp | Emit raw value and set `quality_code=BAD_DATA`. | Reject, log `REJECTED_MONOTONICITY`, raise MAJOR diagnostic `TIMESTAMP_REGRESSION`. | Requires producer fix; alarm clears after two chronological frames inside timeout window. |
| Communication pause (producer halted) | Stop emitting frames. | After 2 missed frames raise `COMMUNICATION_WARNING`; after 3 raise `COMMUNICATION_LOSS`. | Clears only after **two** on-time frames (which may include `NO_DATA` heartbeats) arrive; consumer then resets miss counter. |
| Process crash inside consumer | n/a | Outside scope of this contract; covered by `industrial-python-engineering`. | n/a |

Recovery expectations in every scenario now mirror the diagnostics artifact: the consumer keeps tracking counters until **two consecutive frames** satisfy the nominal condition, except for communication loss where two healthy frames arriving on time clear the warning/loss states.

### 3.5 Diagnostics & Verification Method

- **Producer diagnostics:**
  - Maintains rolling statistics (min/max for temperature/vibration) for inclusion in `diagnostic_notes` when injecting anomalies.
  - Sets `status` according to simulated machine state machine documented in `MACHINE_DIAGNOSTICS.md`.
- **Consumer diagnostics:**
  - Records per-frame `contract_validation` outcome (default `PASS`).
  - Maintains counters: `frames_received`, `frames_rejected_schema`, `frames_rejected_range`, `frames_rejected_monotonicity`, `heartbeat_missed_count`.
  - Exposes metrics via CLI summary for QA inspection (exact formatting delegated to `industrial-python-engineering`).
- **Verification:**
  1. Unit tests `test_telemetry_source`, `test_ingestion_valid`, `test_ingestion_invalid` (Section 22 of proposal) must exercise each scenario above.
  2. Manual checklist: compare data-contract table to implementation before Implementation Review.
  3. Runtime assertion: consumer asserts enumerated `status`/`quality_code` values and rejects unknown strings.

### 3.6 Versioning & Compatibility

- Initial version: `ICD-OT-PIPELINE-001 v1.0 (2026-07-08)`.
- Backward-incompatible changes (renaming tags, changing units) require updated version suffix and downstream coordination before Implementation Review.
- Optional fields may be added if they default to `null`/`None` and are ignored by older consumers.

### 3.7 Security & Access Control

- Interface operates entirely within a single process for this pilot; no transport security is required.
- Authentication/authorization: **Not Applicable** (no multi-tenant runtime, no external clients). Documented here to avoid implicit assumptions.

### 3.8 Observability & Logging Requirements

- Producer logs anomalies when emitting `quality_code != GOOD` and includes `frame_id`.
- Consumer logs every rejection with: `frame_id`, cause, tag/value that triggered rejection, `status`, `quality_code`.
- Consumer must log heartbeat transitions (normal → warning → loss, and clear events).
- All logs must be structured (key=value) so QA & Debug Engineer can parse them deterministically during Implementation Review.

### 3.9 Handoff Notes

- This artifact, together with `MACHINE_DIAGNOSTICS.md`, forms the complete OT-side contract delivered to the Software Engineer before `INDUSTRIAL_PYTHON_ENGINEERING.md` begins.
- RQF-002 is resolved: Purpose and Ownership are explicitly declared above and restated in the inventory table. Any change to those attributes requires looping back through the Industrial Automation Engineer before implementation.
- RQF-001 remains satisfied: this document now explicitly records the decisions/assumptions made after the Requirements Gate PASS, keeping the execution order unambiguous.
