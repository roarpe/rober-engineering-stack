# MACHINE_DIAGNOSTICS.md

Industrial Automation Engineer — Skill `machine-diagnostics`

## 1. Metadata & Preconditions

- **Project:** Industrial Machine Telemetry Ingestion & Diagnostics Pipeline
- **Skill contract:** `skills/machine-diagnostics/SKILL.md`
- **Owner:** Industrial Automation Engineer
- **Participants:** Software Engineer (implements logic), QA & Debug Engineer (verification), Engineering Architect (coherence)
- **Requirements Quality status:** PASS confirmed (2026-07-08).
- **Decision Readiness:** Not required; no blocking alternatives identified in `REQUIREMENTS_GATE_REPORT.md`.
- **Scope:** Diagnostics for a single simulated machine producing telemetry via interface ICD-OT-PIPELINE-001. No physical hardware, operator consoles, HMIs, or maintenance crews exist; such elements are marked **Not Applicable (N/A)** with justification.

### 1.1 Design Decisions & Assumptions

- **Two-frame confirmation for alarm recovery:** Chosen to suppress flicker in a simulation without real noise, while still ensuring a deterministic window that QA can exercise. Because the window length is purely a parameter, it can be tightened later without reworking diagnostic taxonomy.
- **Severity model limited to MAJOR/MINOR/INFO:** Proportional to a pilot with no safety exposure. Introducing CRITICAL would demand safety processes not in scope; leaving it unused keeps the model reversible.
- **First-out tracking retained even without operators:** Provides evidence for QA and future analytics to pinpoint root causes, replacing the usual operator acknowledgement workflow with automated logging (see §8 and §15). If future phases add human actors, the same field can feed an HMI without changes.
- **`quality_code` semantics honored exactly:** `BAD_DATA` indicates corrupted-but-present values, `NO_DATA` is a heartbeat placeholder containing `null` measurement fields (never treated as zeros). This keeps the distinction between invalid telemetry and valid anomalies explicit across artifacts.

## 2. Diagnostic Objectives

1. Detect invalid or missing telemetry frames before they corrupt persistence or analytics.
2. Identify machine-state anomalies driven by `temperature_c`, `vibration_mm_s`, and `cycle_count` trends.
3. Surface communication issues between the simulated OT source and the ingestion pipeline.
4. Provide deterministic severity grading (MAJOR vs MINOR) that Software Engineer and QA can implement and verify via automated tests.
5. Supply enough structured context for CLI summaries and future logs without requiring human operators.

## 3. System Boundaries

- **In scope:** Simulated OT generator, ingestion/persistence service, diagnostics evaluation, CLI summary, SQLite storage.
- **Out of scope:** Physical machine hardware, plant network, PLC firmware, HMI displays, external notification systems, safety-rated behavior.

## 4. Failure Domains & Ownership

| Domain | Description | Owner |
|---|---|---|
| Telemetry quality | Schema/range/monotonicity violations | Industrial Automation Engineer defines limits; Software Engineer enforces. |
| Machine process | Thermal and vibration anomalies derived from telemetry | Industrial Automation Engineer defines thresholds; Software Engineer implements evaluation.| 
| Communication link | Missing frames, heartbeat degradation | Industrial Automation Engineer defines detection; Software Engineer implements counters per ICD watchdog rules. |
| Data persistence | SQLite storage errors | **Not covered** by this skill (delegated to `industrial-python-engineering`). |
| Operator/HMI interactions | **Not Applicable** (no human interface). |

## 5. Taxonomy of Faults

1. **INPUT_OUT_OF_RANGE** — Telemetry within schema but outside specified ranges.
2. **COUNTER_REGRESSION** — `cycle_count` decreases unexpectedly outside maintenance window.
3. **TIMESTAMP_REGRESSION** — `timestamp_utc` goes backwards or arrives stale beyond timeout.
4. **THERMAL_OVER_LIMIT** — `temperature_c` exceeds safe thresholds.
5. **VIBRATION_OVER_LIMIT** — `vibration_mm_s` exceeds acceptable vibration levels.
6. **COMMUNICATION_WARNING / COMMUNICATION_LOSS** — Missing heartbeats as defined in communications contract.
7. **QUALITY_BAD_DATA** — Producer flagged `quality_code=BAD_DATA` with actual readings.
8. **QUALITY_NO_DATA** — Producer emitted placeholders with `quality_code=NO_DATA`; measurements are `null` and interpreted as loss-of-signal, not zero.

## 6. Severity Model

| Severity | Definition | Application |
|---|---|---|
| CRITICAL | Immediate risk; system cannot continue. | Not used in this pilot (no safety context). |
| MAJOR | Requires immediate software attention; halts diagnostics chain but pipeline keeps running. | COMMUNICATION_LOSS, COUNTER_REGRESSION, **TIMESTAMP_REGRESSION**, THERMAL_OVER_LIMIT above MAJOR threshold, VIBRATION_OVER_LIMIT above MAJOR threshold. |
| MINOR | Logged and surfaced but does not block subsequent processing. | INPUT_OUT_OF_RANGE, QUALITY_BAD_DATA, COMMUNICATION_WARNING, THERMAL/VIBRATION MINOR bands. |
| INFO | Context only. | QUALITY_NO_DATA (when expected), heuristics or maintenance resets. |

Numeric thresholds:
- **Temperature bands:**
  - MINOR: 90.0–100.0 °C inclusive.
  - MAJOR: >100.0 °C.
- **Vibration bands:**
  - MINOR: 30.0–40.0 mm/s inclusive.
  - MAJOR: >40.0 mm/s.
- **Cycle counter regression:** any decrease outside a declared maintenance reset is MAJOR.
- **Communication:** 2 missed frames → MINOR (warning); ≥3 → MAJOR (loss). Recovery in all cases requires **two consecutive on-time frames**.

## 7. Alarm & Event Lifecycle

1. **Create:** Diagnostics engine sets alarm when condition transitions from false to true.
2. **Active:** Alarm remains active while condition persists (e.g., successive frames still high).
3. **Acknowledge:** **Not Applicable** (no human operator). Instead, system logs the active condition.
4. **Reset/Clear:** Automatically cleared when the triggering signal returns to normal for two consecutive frames.
5. **Archive:** Persist alarm history with timestamps and severity for CLI summary/testing. Implemented by Software Engineer as part of persistence requirements.

## 8. First-Out Strategy

- Maintain `first_out_alarm` for each cycle. The first MAJOR alarm raised after `status` transitions from `RUNNING` to `FAULT` (or communication loss) is latched until system returns to `IDLE` or `RUNNING` without active alarms. This ensures proportional root-cause traceability even without human acknowledgements: QA can compare first-out to logged telemetry to confirm diagnostics correctness without additional tooling.

## 9. Context Capture Requirements

For every alarm activation the system must capture the following **data elements** (schema left to `INDUSTRIAL_PYTHON_ENGINEERING.md`):
- `alarm_code`, `severity`, `frame_id`
- `activated_at`, `cleared_at`
- Raw telemetry values (`temperature_c`, `vibration_mm_s`, `cycle_count`, `status`, `quality_code` or `null` for `NO_DATA`).
- `contract_validation` result from ingestion.
- Derived metrics: heartbeat miss count, threshold that was exceeded, boolean `first_out_alarm`.
Implementation owns the storage structure (e.g., SQLite columns) but must persist at least these fields for traceability.

## 10. Logging, Metrics & Traces

- Persist alarm lifecycle events using the data elements listed in §9; storage medium/schema is decided later by `INDUSTRIAL_PYTHON_ENGINEERING.md`.
- Maintain cumulative counters exposed through CLI summary: number of MAJOR/MINOR alarms, current heartbeat status, last rejected frame cause.
- Structured logs (key=value) for each alarm create/clear event to aid QA verification.

## 11. Diagnostics Contracts by Subsystem

| Subsystem | Diagnostic Output | Consumer |
|---|---|---|
| Simulated OT generator | `status`, `quality_code`, `diagnostic_notes` embedded in telemetry frames | Diagnostics engine uses to contextualize issues; no extra channel required. |
| Ingestion pipeline | `contract_validation` outcome, rejection counters, heartbeat metrics | Diagnostics engine consumes to generate INPUT/COMMUNICATION alarms. |
| Diagnostics engine | Alarm objects, lifecycle state, first-out metadata | CLI & tests read to present results. |
| Operator/HMI | **Not Applicable** — there is no operator interface. |

## 12. Recovery Model

| Role | Actions |
|---|---|
| Operator | **Not Applicable** (no operators). |
| Maintenance | **Not Applicable** (no physical system). |
| Engineering | Investigate telemetry generator or ingestion logic depending on alarm code; rerun CLI after fixes to confirm clearance. |

Recovery is fully automated: alarms clear only after **two consecutive frames** meet nominal conditions (matching the communications contract). Engineering intervention is documented in repo issues or follow-up tasks (outside scope of this skill).

## 13. Operator Guide (N/A)

- **Status:** Not Applicable — no operator exists. Documented to satisfy template.
- **Justification:** Pilot runs entirely inside development environment without human-machine interface.

## 14. Maintenance Guide (N/A)

- **Status:** Not Applicable — there is no physical maintenance crew.
- **Justification:** All corrective actions occur in software design/implementation.

## 15. Escalation to Engineering

- Triggered when MAJOR alarms persist for more than 5 consecutive frames or repeat within a single CLI run.
- Engineering must review logs, verify contract adherence, and adjust thresholds or simulation behavior if alarms reveal modeling issues.

## 16. Recovery Verification

- After an alarm clears, diagnostics engine writes a `recovery_event` entry (in-memory or SQLite) noting the condition return to normal along with final readings.
- Automated test `test_diagnostics_thresholds` must assert that a MAJOR alarm clears when telemetry falls below MINOR band for two frames.

## 17. Risks of Diagnostic Strategy

| ID | Risk | Mitigation |
|---|---|---|
| DR-01 | Simulated telemetry may not cover edge combinations (e.g., simultaneous temperature and vibration spikes). | Include deterministic test vectors for combined faults so QA can verify multi-alarm behavior. |
| DR-02 | Communication-loss alarms could trigger due to long-running unit tests pausing execution. | Tests should mock time or emit frames faster to avoid false positives; document in `INDUSTRIAL_PYTHON_ENGINEERING.md`. |
| DR-03 | Absence of human acknowledgements could hide first-out data. | Persist first-out metadata per Section 8; CLI must display it explicitly. |

## 18. Decisions & Open Items

- **Thresholds chosen** per Section 6 based on proportional sample ranges; can be revisited after empirical test data.
- **Open item:** None blocking. Any future change to thresholds requires updating this artifact and re-running Implementation Review.

## 19. Diagnostics vs Debugging Distinction

- This artifact specifies the proactive design: signals, thresholds, alarms, lifecycle, and automated recovery/verification.
- Actual debugging of anomalies (investigating logs, reproducing bugs) remains the responsibility of QA & Debug Engineer following `systematic-debugging` and occurs after implementation.

## 20. Handoff Notes

- Outputs required by Software Engineer:
  - Threshold table (Section 6)
  - Alarm lifecycle & first-out behavior (Sections 7–8)
  - Context capture schema (Section 9)
  - Logging & persistence expectations (Section 10)
  - Recovery automation rules (Sections 12 & 16)
- QA & Debug Engineer will use Sections 6–10 to craft tests verifying severity transitions, first-out capture, and communication-loss handling.
- This artifact, combined with `INDUSTRIAL_COMMUNICATIONS_DESIGN.md`, satisfies RQF-001 by documenting the post-gate order: both skills now complete and ready for Software Engineer consumption.
