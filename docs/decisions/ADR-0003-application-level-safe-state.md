# ADR-0003: Application-Level Safe State Definition (SAFE_IDLE)

## Status

ACCEPTED — 2026-07-10

## Context

The project requires a defined application-level safe state for the KRL state
machine. The Decision Readiness Gate (ROBOT_DR_GATE_REPORT.md) classified D010
as BLOCKING with HIGH risk and difficult reversibility. The safe state is a
key state-machine element required before architecture can proceed.

D003 (ADR-0002) established that safety-rated functions are outside project
scope and that application-level states must not be described as safety-rated.
D010 must define an application-level safe state that preserves this boundary.

The Project Owner is the decision owner, with Robotics Engineer and Safety
Specialist consultation. The Robotics Engineer confirms the definition is
sufficient to establish a state-machine target without prematurely defining
motion implementation. The Safety Specialist confirms the distinction between
SAFE_IDLE and safety-rated states preserves the D003 safety boundary.

This decision affects D009 (recovery strategy — entry into SAFE_IDLE occurs
when no immediate automatic recovery is authorized) and the future state
machine architecture.

## Decision

The application-level safe state shall be represented by the application state:

**`SAFE_IDLE`**

### Definition

`SAFE_IDLE` is a defined KRL application condition. It shall not mean or imply
a safety-rated robot state.

### Conditions in SAFE_IDLE

- No automatic production cycle is active
- No new automatic cycle may start
- No recovery sequence is active
- No automatic motion command is initiated
- No gripper actuation command is initiated
- The application preserves available diagnostic information about the event
  that caused entry into `SAFE_IDLE`
- Explicit authorization shall be required before leaving `SAFE_IDLE` according
  to the final recovery and authorization contracts

### Entry conditions

Entry into `SAFE_IDLE` shall occur when application-level logic determines that
normal cycle execution cannot continue and no immediate automatic recovery
action is authorized by the final D009 recovery strategy.

### SAFE_IDLE shall NOT

- Be described as a safety-rated state
- Replace emergency stop behavior
- Replace protective stop behavior
- Replace controller safety functions
- Replace external safety architecture
- Guarantee that the robot is physically located at a specific coordinate or
  pose

### Physical position separation

Physical robot position and application state shall remain separate concepts.
A physical waiting, home, or recovery position may be defined later during
robot software architecture if required for deterministic motion behavior.
Entry into `SAFE_IDLE` shall not automatically command movement to such a
position.

## Alternatives Considered

| Option | Description | Rejected because |
|---|---|---|
| SAFE_IDLE with automatic motion to home | Return to home position on safe state entry | Rejected — would prematurely define motion implementation; physical position and application state must remain separate |
| SAFE_IDLE as safety-rated state | Treat safe state as equivalent to safety-rated state | Rejected — violates D003 boundary; KRL application shall not claim safety-rated responsibility |
| Multiple safe states (e.g., SAFE_IDLE, SAFE_ERROR, SAFE_RECOVERY) | Differentiate safe states by cause | Not selected — single SAFE_IDLE with preserved diagnostics is sufficient for validation project; complexity not warranted |
| No explicit safe state | Rely on controller safety only | Rejected — application state machine requires a defined safe state target |
| SAFE_IDLE (SELECTED) | Single application-level safe state, no motion, no safety-rated claims, diagnostics preserved, authorization required to leave | Selected — proportional to validation project scope, preserves D003 boundary, sufficient for state machine |

## Consequences

- **State machine**: `SAFE_IDLE` is a primary state-machine target. The
  architecture must define transitions into and out of `SAFE_IDLE`.
- **D009 (recovery)**: Entry into `SAFE_IDLE` occurs when no immediate
  automatic recovery is authorized. D009 must define what recovery actions
  are automatic vs. what requires `SAFE_IDLE` entry. Leaving `SAFE_IDLE`
  requires explicit authorization per the final D009/D006 contracts.
- **D006 (authorization)**: Authorization is required to leave `SAFE_IDLE`.
  D006 must define the authorization interface that governs this transition.
- **D005 (operating conditions)**: D005 defines cycle-start conditions. The
  relationship between `SAFE_IDLE` and cycle start is: a cycle cannot start
  from `SAFE_IDLE` without authorization.
- **Motion**: No automatic motion command is initiated in `SAFE_IDLE`. A
  physical home/recovery position may be defined during architecture but is
  not automatically commanded.
- **Diagnostics**: The application must preserve diagnostic information about
  the event causing `SAFE_IDLE` entry. This supports D008 (diagnostics
  strategy).
- **Safety boundary**: `SAFE_IDLE` is explicitly NOT a safety-rated state.
  This preserves the D003 (ADR-0002) safety boundary.

## Evidence

- Project Owner decision: 2026-07-10
- Robotics Engineer consultation: confirms definition sufficient for
  state-machine target without prematurely defining motion implementation
- Safety Specialist consultation: confirms distinction between SAFE_IDLE and
  safety-rated states preserves D003 safety boundary
- DR Gate classification: BLOCKING, HIGH risk, difficult reversibility
- Resolution method: user decision + specialist consultation
- Decision recorded in: PROJECT_DISCOVERY.md section 13 (D010 status updated
  to RESOLVED)
- Validation log: VALIDATION_LOG.md (VL-090)

## References

- PROJECT_DISCOVERY.md section 13 (D010)
- ROBOT_DR_GATE_REPORT.md (DR Gate FAIL, D010 classification)
- gates/decision-readiness/GATE.md (Evidence Required: ADR as resolution evidence)
- docs/decisions/README.md (ADR creation criteria: hard to reverse, real
  alternatives, future agent could reopen)
- ADR-0001 (robot model and controller — KR C4 selected)
- ADR-0002 (safety architecture boundary — safety-rated functions outside scope)
