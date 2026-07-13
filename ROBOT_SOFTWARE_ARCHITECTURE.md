# ROBOT_SOFTWARE_ARCHITECTURE.md

ROBER ENGINEERING STACK -- Robot Software Architecture
Project: Industrial Robot Software Validation -- 6-axis pick-and-place (KUKA KRL)
Date: 2026-07-10
Owner: Engineering Architect (coordinator), Robotics Engineer (primary author)
Module: robotics
Preceding gates: RQ Gate V2 PASS, DR Gate V2 PASS
Platform: KUKA KR 6 R900 sixx, KR C4, KSS 8.3 (ADR-0001)
Verification: KUKA.Sim + OfficeLite, no physical hardware (D002)

---

## 1. Pre-Execution Verification

| Field | Value |
|---|---|
| HEAD | 43aef84 |
| main | 43aef84 |
| origin/main | 43aef84 |
| Working tree | 10 untracked files (all authorized project artefacts) |
| RQ Gate V2 verdict | PASS (12/12 acceptance criteria approved) |
| DR Gate V2 verdict | PASS (8/8 blocking decisions resolved with evidence) |
| ADRs applicable | ADR-0001, ADR-0002, ADR-0003 |

### Authorized project boundary

| In scope | Out of scope |
|---|---|
| KRL application software for pick-and-place cycle | Safety-rated functions (D003, ADR-0002) |
| Application-level state machine | PLC, vision, conveyor, database, backend |
| Gripper control via digital I/O | Physical robot motion execution (simulation only per D002) |
| Application-level diagnostics | Controller fault recovery, collision recovery, E-stop handling |
| Application-level recovery (bounded retries) | Maintenance mode, manual mode, teaching |
| Authorization handshake | HMI, external protocols |
| SAFE_IDLE state and RECOVERY_RESET | Production deployment |

---

## 2. Proportional KRL Decomposition

### Design principle

The user constraint requires modular separation of six functional responsibilities:
(1) production sequence, (2) motion logic, (3) gripper control, (4) interface handling,
(5) diagnostics, (6) recovery behavior. The architecture instruction explicitly states:
"Do not assume six physical modules merely because six functional responsibilities
were identified."

### Decomposition analysis

| Functional responsibility | Separate file? | Rationale |
|---|---|---|
| Production sequence | No — integrated into main program | The 12-step cycle is the main program's primary purpose. |
| Motion logic | No — integrated into main program | Motion commands (PTP, LIN) are sequential within cycle steps. No complex motion planning in scope. |
| Gripper control | **Yes** | Distinct I/O (2 DO, 3 DI), verification logic, retry execution. Has internal state (retry counters). |
| Interface handling | No — integrated into main program | CYCLE_REQUEST/CYCLE_COMPLETE/RECOVERY_RESET tightly coupled to state machine. |
| Diagnostics | **Yes** | Cross-cutting (R08). Preserved across states. Distinct data ownership. |
| Recovery behavior | **Yes** | D009 requires explicit modular separation. Owns SAFE_IDLE exit, RECOVERY_RESET. |

### Result: 4 KRL program files

| # | File | Responsibility | Owns |
|---|---|---|---|
| 1 | `main.src` / `main.dat` | State machine, cycle orchestration, motion, interface handling | Application state, CYCLE_REQUEST consumption, CYCLE_COMPLETE, SAFE_IDLE entry |
| 2 | `gripper.src` / `gripper.dat` | Gripper actuation, verification, retry counters | Gripper I/O, grip/release verification, retry state |
| 3 | `diag.src` / `diag.dat` | Diagnostic data recording, preservation, clearing | Diagnostic data structure |
| 4 | `recovery.src` / `recovery.dat` | Recovery coordination, SAFE_IDLE exit, RECOVERY_RESET | Recovery state, RECOVERY_RESET processing |

### Functional responsibility coverage

| Required responsibility | Covered by |
|---|---|
| Production sequence | `main.src` — 12-step cycle in main loop |
| Motion logic | `main.src` — PTP/LIN commands inline in cycle steps |
| Gripper control | `gripper.src` — actuation + verification + retry |
| Interface handling | `main.src` — CYCLE_REQUEST/CYCLE_COMPLETE/RECOVERY_RESET in state machine |
| Diagnostics | `diag.src` — recording, preservation, clearing |
| Recovery behavior | `recovery.src` — retry coordination, SAFE_IDLE, RECOVERY_RESET |

**All 6 functional responsibilities have explicit ownership. 4 files is proportional.**

---

## 3. Application State Model

### States

| State | Owner | Description | Motion? | Gripper? |
|---|---|---|---|---|
| `IDLE` | `main.src` | Waiting for CYCLE_REQUEST | No | No |
| `CONDITION_CHECK` | `main.src` | Evaluating D005 operating conditions | No | No |
| `CYCLE_ACTIVE` | `main.src` | Executing 12-step pick-and-place cycle | Yes | Yes |
| `RECOVERY_RETRY` | `recovery.src` | Executing automatic retry (gripping or release) | Limited | Yes |
| `SAFE_IDLE` | `recovery.src` | Application-level safe state. No auto-leave. | No | No |
| `RECOVERY_RESET_PROC` | `recovery.src` | Processing RECOVERY_RESET signal | No | No |

### State transition diagram

```
                    CYCLE_REQUEST active + conditions met
  IDLE ──────────────────────────────────► CONDITION_CHECK
   ▲                                         │
   │                                         │ conditions OK
   │                                         ▼
   │                                    CYCLE_ACTIVE ◄──────────┐
   │                                         │                  │
   │                                         │ gripping fail    │ retry < max
   │                                         ▼                  │
   │                                    RECOVERY_RETRY ──────────┘
   │                                         │
   │                                         │ retry fail OR
   │                                         │ invalid internal state
   │                                         ▼
   │                                    SAFE_IDLE
   │                                         │
   │                                         │ RECOVERY_RESET valid
   │                                         ▼
   │                                   RECOVERY_RESET_PROC
   │                                         │
   │                                         │ reset complete
   │                                         ▼
   └─────────────────────────────────────── IDLE
```

### State transition rules

| From | To | Trigger | Guard conditions |
|---|---|---|---|
| `IDLE` | `CONDITION_CHECK` | CYCLE_REQUEST active | Request not consumed, no fault, no recovery, not in SAFE_IDLE |
| `CONDITION_CHECK` | `CYCLE_ACTIVE` | All D005 conditions satisfied | Request marked consumed on transition |
| `CONDITION_CHECK` | `IDLE` | Any D005 condition not satisfied | Request not consumed, diagnostic on failed condition |
| `CYCLE_ACTIVE` | `RECOVERY_RETRY` | Gripping failure detected | Grip retry count < 1 |
| `CYCLE_ACTIVE` | `RECOVERY_RETRY` | Release failure detected | Release retry count < 1 |
| `CYCLE_ACTIVE` | `IDLE` | Cycle completed successfully | CYCLE_COMPLETE set, wait for request clear, rearm |
| `CYCLE_ACTIVE` | `SAFE_IDLE` | Invalid internal cycle state | No auto-recovery, request remains consumed |
| `RECOVERY_RETRY` | `CYCLE_ACTIVE` | Retry successful | Cycle continues with same consumed request |
| `RECOVERY_RETRY` | `SAFE_IDLE` | Retry failed | No CYCLE_COMPLETE, request remains consumed |
| `SAFE_IDLE` | `RECOVERY_RESET_PROC` | RECOVERY_RESET active | No recovery active, no motion, no gripper, CYCLE_REQUEST inactive |
| `RECOVERY_RESET_PROC` | `IDLE` | Reset complete | Fault cleared, recovery cleared, request rearmed, diagnostics archived |

### Critical state invariants

- **SAFE_IDLE**: No motion. No gripper actuation. Diagnostics preserved. No new cycle. No auto-leave.
- **RECOVERY_RESET_PROC**: No motion. No gripper. No auto-start cycle. No bypass of D005/D006/safety.
- **CYCLE_ACTIVE**: Exactly one consumed request. At most 1 grip retry + 1 release retry per cycle.
- **IDLE**: No consumed request. No active fault. No recovery state. Diagnostics cleared.

---

## 4. Cycle-Request Consumption and Rearming Model (D006)

### Signal ownership

| Signal | Direction | Owner | Purpose |
|---|---|---|---|
| `CYCLE_REQUEST` | Input (external -> robot) | `main.src` | Cycle authorization request |
| `CYCLE_COMPLETE` | Output (robot -> external) | `main.src` | Cycle completion notification |
| `RECOVERY_RESET` | Input (external -> robot) | `recovery.src` | Request to leave SAFE_IDLE |

### Consumption model

```
State: IDLE
  CYCLE_REQUEST = FALSE -> stay IDLE, wait
  CYCLE_REQUEST = TRUE  -> check conditions
    Conditions OK    -> consume request (request_consumed = TRUE)
                        -> transition to CYCLE_ACTIVE
    Conditions fail  -> do NOT consume -> return to IDLE
                        -> record diagnostic on failed condition

State: CYCLE_ACTIVE
  request_consumed = TRUE
  CYCLE_REQUEST still TRUE -> no additional cycle (anti-duplication)
  CYCLE_REQUEST goes FALSE -> cycle continues (abnormal per D006)
  Cycle completes successfully:
    -> Set CYCLE_COMPLETE = TRUE
    -> Wait for CYCLE_REQUEST = FALSE
    -> Rearm: request_consumed = FALSE
    -> Clear CYCLE_COMPLETE = FALSE
    -> Return to IDLE
  Cycle fails (enters SAFE_IDLE):
    -> CYCLE_COMPLETE stays FALSE
    -> request_consumed stays TRUE
    -> Must leave SAFE_IDLE via RECOVERY_RESET
    -> RECOVERY_RESET rearms request_consumed = FALSE

State: SAFE_IDLE
  request_consumed = TRUE (from failed cycle)
  CYCLE_REQUEST must be FALSE before RECOVERY_RESET accepted
  RECOVERY_RESET processing:
    -> Clear fault, clear recovery state
    -> Rearm: request_consumed = FALSE
    -> Return to IDLE
    -> New cycle requires new CYCLE_REQUEST
```

### Anti-duplication mechanism

The `request_consumed` boolean flag in `main.dat` is the primary anti-duplication
mechanism:

1. One CYCLE_REQUEST edge = at most one cycle.
2. Continuously active CYCLE_REQUEST never causes repeated cycles.
3. Request must be cleared (CYCLE_REQUEST = FALSE) and rearmed before new cycle.
4. Failed cycle keeps request consumed — no auto-retry at cycle level.

---

## 5. Recovery Architecture (D009)

### Recovery ownership

| Behavior | Owner | File |
|---|---|---|
| Retry counter management | `gripper.src` | `gripper.dat` (counters) |
| Retry execution (gripping) | `gripper.src` | open, verify, regrip sequence |
| Retry execution (release) | `gripper.src` | re-open, verify sequence |
| SAFE_IDLE entry decision | `main.src` | on failure detection |
| SAFE_IDLE state management | `recovery.src` | state, exit logic |
| RECOVERY_RESET processing | `recovery.src` | guard check, reset, rearm |

### Gripping failure retry (max 1 per cycle)

```
Trigger: Step 6 (verify grip) fails
Guard: grip_retry_count < 1
Sequence:
  1. Record diagnostic (step, failure type, retry attempt)
  2. Set gripper OPEN (DO)
  3. Verify GRIPPER_OPEN active (DI)
  4. Set gripper CLOSE (DO)
  5. Verify GRIPPER_CLOSED AND PART_PRESENT active (DI)
  6. Success: grip_retry_count++, resume cycle
  7. Fail: grip_retry_count++, transition to SAFE_IDLE
```

### Release failure retry (max 1 per cycle)

```
Trigger: Step 10 (verify release) fails
Guard: release_retry_count < 1
Sequence:
  1. Record diagnostic (step, failure type, retry attempt)
  2. Set gripper OPEN (DO) — re-open
  3. Verify GRIPPER_OPEN active AND PART_PRESENT inactive (DI)
  4. Success: release_retry_count++, cycle completes, CYCLE_COMPLETE per D006
  5. Fail: release_retry_count++, transition to SAFE_IDLE
Note: NO robot motion during release retry (D009 constraint)
```

### Invalid pre-cycle conditions

```
Trigger: Any D005 condition not satisfied during CONDITION_CHECK
Action: Do NOT consume CYCLE_REQUEST, record diagnostic, return to IDLE
No SAFE_IDLE entry (unless independent failure detected)
```

### Invalid internal cycle state

```
Trigger: Unexpected state detected during CYCLE_ACTIVE
Action: No auto-recovery, no motion, no gripper, record diagnostic,
        cycle terminates unsuccessfully, no CYCLE_COMPLETE,
        request_consumed stays TRUE, transition to SAFE_IDLE
```

### SAFE_IDLE exit via RECOVERY_RESET

```
Guard conditions (all must be true):
  - No recovery active
  - No automatic motion in progress
  - No gripper actuation in progress
  - D005 conditions evaluated
  - Previous CYCLE_REQUEST is inactive (FALSE)

Processing:
  1. Clear application-level fault flag
  2. Clear recovery state
  3. Rearm request consumption (request_consumed = FALSE)
  4. Return to IDLE
  5. Acknowledge/archive diagnostics

RECOVERY_RESET shall NOT:
  - Auto-start a cycle
  - Auto-execute motion
  - Auto-actuate gripper
  - Bypass D005/D006/safety
```

### Retry counter reset

- `grip_retry_count` and `release_retry_count` reset to 0 at:
  - Cycle start (CONDITION_CHECK -> CYCLE_ACTIVE transition)
  - RECOVERY_RESET processing (RECOVERY_RESET_PROC -> IDLE transition)

---

## 6. KRL Program Structure

### 6.1 File: `main.src` / `main.dat`

**Owner**: Robotics Engineer
**Role**: Main program — state machine, cycle orchestration, motion, interface handling

#### `main.dat` declarations

```krl
; Application state
DECL INT app_state
DECL BOOL request_consumed
DECL BOOL cycle_complete_signal

; Signal declarations (functional identifiers)
DECL IN CYCLE_REQUEST
DECL OUT CYCLE_COMPLETE
DECL IN RECOVERY_RESET

; Position declarations (values during implementation/teaching)
DECL E6POS pick_approach
DECL E6POS pick_position
DECL E6POS place_approach
DECL E6POS place_position
DECL E6POS safe_wait_position
```

#### `main.src` structure

```krl
DEF main()
  INIT()
  LOOP
    SWITCH app_state
      CASE #IDLE
        IF CYCLE_REQUEST AND NOT request_consumed THEN
          app_state = #CONDITION_CHECK
        ENDIF
      CASE #CONDITION_CHECK
        IF check_conditions() THEN
          request_consumed = TRUE
          grip_retry_count = 0
          release_retry_count = 0
          app_state = #CYCLE_ACTIVE
        ELSE
          app_state = #IDLE
        ENDIF
      CASE #CYCLE_ACTIVE
        execute_cycle()
      CASE #SAFE_IDLE
        recovery.handle_safe_idle()
      CASE #RECOVERY_RESET_PROC
        recovery.handle_recovery_reset()
    ENDSWITCH
  ENDLOOP
END
```

#### `main.src` subroutines

| Routine | Purpose |
|---|---|
| `INIT()` | Initialize state, signals, positions |
| `check_conditions()` | Evaluate 8 D005 conditions, record diagnostic on failure |
| `execute_cycle()` | Execute 12-step cycle with motion and gripper calls |
| `set_cycle_complete()` | Set CYCLE_COMPLETE, wait for request clear, rearm |
| `enter_safe_idle()` | Transition to SAFE_IDLE, preserve diagnostics |

### 6.2 File: `gripper.src` / `gripper.dat`

**Owner**: Robotics Engineer
**Role**: Gripper actuation, verification, retry execution

#### `gripper.dat` declarations

```krl
DECL OUT GRIPPER_OPEN_CMD
DECL OUT GRIPPER_CLOSE_CMD
DECL IN GRIPPER_OPEN_FB
DECL IN GRIPPER_CLOSED_FB
DECL IN PART_PRESENT_FB
DECL INT grip_retry_count
DECL INT release_retry_count
```

#### `gripper.src` routines

| Routine | Purpose |
|---|---|
| `close_gripper()` | Set CLOSE output, deactivate OPEN |
| `open_gripper()` | Set OPEN output, deactivate CLOSE |
| `verify_grip()` | Returns TRUE if GRIPPER_CLOSED_FB AND PART_PRESENT_FB |
| `verify_release()` | Returns TRUE if GRIPPER_OPEN_FB AND NOT PART_PRESENT_FB |
| `execute_grip_retry()` | Open, verify open, close, verify grip. Max 1 per cycle. |
| `execute_release_retry()` | Re-open, verify release. No motion. Max 1 per cycle. |

### 6.3 File: `diag.src` / `diag.dat`

**Owner**: Robotics Engineer
**Role**: Diagnostic data recording, preservation, clearing

#### `diag.dat` declarations

```krl
DECL INT diag_step
DECL INT diag_failure_type
DECL INT diag_retry_attempt
DECL BOOL diag_requires_intervention
DECL BOOL diag_recovery_available
DECL BOOL diag_active
```

#### `diag.src` routines

| Routine | Purpose |
|---|---|
| `record(step, failure_type, retry_attempt, ...)` | Record diagnostic data |
| `preserve()` | Mark diagnostic as active — not cleared on state transition |
| `clear()` | Clear diagnostic — called only during RECOVERY_RESET |
| `is_active()` | Returns TRUE if diagnostic record is active |

### 6.4 File: `recovery.src` / `recovery.dat`

**Owner**: Robotics Engineer
**Role**: Recovery coordination, SAFE_IDLE management, RECOVERY_RESET processing

#### `recovery.dat` declarations

```krl
DECL BOOL recovery_active
DECL BOOL safe_idle_entered
DECL BOOL recovery_reset_requested
```

#### `recovery.src` routines

| Routine | Purpose |
|---|---|
| `handle_safe_idle()` | Wait for RECOVERY_RESET, verify guards, transition to reset |
| `handle_recovery_reset()` | Clear fault, clear recovery, rearm request, return to IDLE |
| `enter_safe_idle(failure_type)` | Called by main on unrecoverable failure |

---

## 7. Interface and Signal Ownership Model

### Signal ownership matrix

| Signal | Direction | Owner file | Writer | Notes |
|---|---|---|---|---|
| `CYCLE_REQUEST` | Input | `main.src` | External | Authorization request |
| `CYCLE_COMPLETE` | Output | `main.src` | `main.src` | Completion notification |
| `RECOVERY_RESET` | Input | `recovery.src` | External | SAFE_IDLE exit request |
| `GRIPPER_OPEN_CMD` | Output | `gripper.src` | `gripper.src` | Gripper open command |
| `GRIPPER_CLOSE_CMD` | Output | `gripper.src` | `gripper.src` | Gripper close command |
| `GRIPPER_OPEN_FB` | Input | `gripper.src` | Gripper | Gripper open feedback |
| `GRIPPER_CLOSED_FB` | Input | `gripper.src` | Gripper | Gripper closed feedback |
| `PART_PRESENT_FB` | Input | `gripper.src` | Gripper | Part present feedback |

### Allowed dependencies

```
main.src ──────► gripper.src    (calls gripper routines)
main.src ──────► diag.src       (records diagnostics)
main.src ──────► recovery.src   (calls enter_safe_idle)
gripper.src ───► diag.src       (records retry diagnostics)
recovery.src ──► diag.src       (clears diagnostics on reset)
recovery.src ──► main.dat       (rearms request_consumed, sets app_state)

NOT allowed (no circular dependencies):
gripper.src ──► main.src
gripper.src ──► recovery.src
diag.src ────► main.src
diag.src ────► gripper.src
diag.src ────► recovery.src
recovery.src ► gripper.src
```

**Dependency direction**: `main.src` -> `gripper.src`, `diag.src`, `recovery.src`.
`gripper.src` -> `diag.src`. `recovery.src` -> `diag.src`. No circular dependencies.

---

## 8. Motion and Gripper Interaction

### Motion prevention during SAFE_IDLE and RECOVERY_RESET

| State | Motion allowed? | Enforcement |
|---|---|---|
| `SAFE_IDLE` | No | State machine does not enter CYCLE_ACTIVE. No motion command in handle_safe_idle(). |
| `RECOVERY_RESET_PROC` | No | No motion command in handle_recovery_reset(). |
| `RECOVERY_RETRY` (release) | No | execute_release_retry() contains no motion commands. |
| `RECOVERY_RETRY` (gripping) | No | execute_grip_retry() contains gripper commands only. No robot motion. |

### Gripper command separation from verification

| Action | Command routine | Verification routine |
|---|---|---|
| Close gripper | `close_gripper()` sets GRIPPER_CLOSE_CMD | `verify_grip()` reads GRIPPER_CLOSED_FB + PART_PRESENT_FB |
| Open gripper | `open_gripper()` sets GRIPPER_OPEN_CMD | `verify_release()` reads GRIPPER_OPEN_FB + PART_PRESENT_FB |

Commands and verification are separate routines. This ensures:
1. Verification can fail without re-actuating the gripper.
2. Retry logic can re-issue commands based on verification results.
3. Command and verification can be tested independently.

---

## 9. Diagnostics Strategy -- D008 Resolution

### D008 resolution

| Field | Value |
|---|---|
| Question | Que diagnosticos se requieren, en que formato y para que audiencia? |
| Resolution | Application-level diagnostics via KRL variables in `diag.src`/`diag.dat`. No external HMI, database, or logging protocol. Diagnostic data stored in KRL variables. R08 acceptance criterion defines minimum content: (a) step/state, (b) failure type, (c) intervention required, (d) recovery available. Diagnostics preserved across state transitions, cleared only during RECOVERY_RESET. Accessible via KRL variable inspection in OfficeLite/simulation. |
| Evidence | Architecture defines diag.src/diag.dat with explicit data structure. R08 acceptance criterion already approved. D005, D009, D010 resolutions all reference diagnostic recording. Sufficient evidence exists to resolve D008 during architecture per its reactivation condition. |
| ADR required | No -- LOW-MEDIUM risk, reversible, framework allows documented engineering decision. |
| Status | **RESOLVED** -- 2026-07-10 (Architecture phase) |
| Validation log | VL-115 |

### Diagnostic data structure

| Field | Type | R08 mapping |
|---|---|---|
| `diag_step` | INT | (a) paso o estado actual |
| `diag_failure_type` | INT | (b) tipo de fallo detectado |
| `diag_retry_attempt` | INT | Retry attempt context |
| `diag_requires_intervention` | BOOL | (c) si se requiere intervencion |
| `diag_recovery_available` | BOOL | (d) si la recuperacion esta disponible |
| `diag_active` | BOOL | Diagnostic record status |

### Failure type codes

| Code | Failure | Recovery? | Intervention? |
|---|---|---|---|
| 1 | Gripping failure | Yes (1 auto retry) | If retry fails: yes |
| 2 | Release failure | Yes (1 auto retry) | If retry fails: yes |
| 3 | Authorization invalid | No | No |
| 4 | Operating condition not satisfied | No | No |
| 5 | Invalid internal cycle state | No (SAFE_IDLE) | Yes |
| 6 | Gripping retry failure | No (SAFE_IDLE) | Yes |
| 7 | Release retry failure | No (SAFE_IDLE) | Yes |

### Diagnostic lifecycle

```
1. Failure detected -> diag.record() called by detecting component
2. diag_active = TRUE -> diagnostic preserved
3. State transitions occur -> diagnostic NOT cleared
4. SAFE_IDLE entered -> diagnostic remains active and accessible
5. RECOVERY_RESET processed -> diag.clear() -> diag_active = FALSE
6. Return to IDLE -> diagnostic cleared
```

---

## 10. Safety Boundary Preservation (D003, ADR-0002)

| Domain | Responsibility | Owner | KRL involvement |
|---|---|---|---|
| Safety-rated functions | E-stop, protective stop, safe monitoring | Controller/safety system | None — KRL shall not implement, emulate, or replace |
| External safety architecture | Safety PLC, safety I/O, SafeOperation | External systems | None — outside project scope |
| Application-level behavior | State machine, cycle, gripper, diagnostics, recovery | KRL application | Full ownership |

### Architecture enforcement

1. No safety-rated KRL commands in architecture (no BRAKE, RESUME, SAFETY).
2. SAFE_IDLE is not safety-rated (ADR-0003). No safety-rated command on entry.
3. No auto-recovery from safety events. Recovery handles application-level failures only.
4. RECOVERY_RESET explicitly does not bypass safety.

---

## 11. Simulation and Verification Limitations (D002)

| Evidence type | Tool | Available? | Limitations |
|---|---|---|---|
| KRL execution | OfficeLite (KSS 8.3) | Yes | Software-level only — no physical motion |
| Robot-cell simulation | KUKA.Sim | Yes | 3D simulation — validates motion paths, not I/O timing |
| Physical hardware | None | No | Cannot verify physical gripping, part presence, I/O behavior |

### Architecture accommodations

1. All external signals must be simulatable via variable override in OfficeLite.
2. Architecture uses functional signal names, not physical I/O addresses.
3. KUKA.Sim validates motion paths; OfficeLite validates KRL execution logic.
4. Verification limitations to report in Final Verification: physical gripping force, pneumatic response time, sensor debounce/timing, physical part presence detection.

---

## 12. Requirements and Decision-to-Architecture Traceability

### Requirement-to-architecture mapping

| Req | Acceptance criterion | Architecture component | Verification approach |
|---|---|---|---|
| R01 | Execute 12-step cycle | `main.src` execute_cycle() | OfficeLite: execute cycle, verify all 12 steps |
| R02 | No cycle without authorization | `main.src` IDLE state, CYCLE_REQUEST check | OfficeLite: verify no transition without CYCLE_REQUEST |
| R03 | Approach positions | `main.src` motion commands | KUKA.Sim: verify approach positions before pick and place |
| R04 | Gripper via digital signals | `gripper.src` close/open_gripper() | OfficeLite: verify DO activation on steps 5 and 9 |
| R05 | Verify grip | `gripper.src` verify_grip() | OfficeLite: verify no step 7 without grip confirmation |
| R06 | Verify release | `gripper.src` verify_release() | OfficeLite: verify no step 11 without release confirmation |
| R07 | Detect 5 failure types | `main.src`, `gripper.src`, `recovery.src` | OfficeLite: simulate each failure, verify detection |
| R08 | Useful diagnostics | `diag.src` record(), data structure | OfficeLite: trigger failures, verify diag fields populated |
| R09 | Support recovery | `recovery.src`, `gripper.src` retry routines | OfficeLite: simulate failure, verify retry sequence |
| R10 | Prevent duplicate cycle | `main.src` request_consumed flag | OfficeLite: hold CYCLE_REQUEST, verify single cycle |
| R11 | Return to safe state | `recovery.src` enter_safe_idle(), SAFE_IDLE | OfficeLite: trigger failure, verify SAFE_IDLE entry |
| R12 | Modular architecture | 4 KRL files with explicit ownership | Inspection: verify file structure, ownership, interfaces |

### Decision-to-architecture mapping

| Decision | Resolution | Architecture impact | Evidence |
|---|---|---|---|
| D001 | KR 6 R900 sixx, KR C4, KSS 8.3 | KRL syntax targets KSS 8.3; PTP/LIN motion; no optional packages | ADR-0001 |
| D002 | KUKA.Sim + OfficeLite, no hardware | Signal simulation required; verification limitations documented | VL-081 |
| D003 | Safety-rated out of scope | No safety-rated KRL commands; SAFE_IDLE not safety-rated | ADR-0002 |
| D004 | Pneumatic gripper, 2 DO + 3 DI | `gripper.src` signal definitions; verification logic | VL-076 |
| D005 | 8 operating conditions | `main.src` check_conditions() | VL-088 |
| D006 | CYCLE_REQUEST/CYCLE_COMPLETE handshake | `main.src` consumption/rearming model | VL-095 |
| D008 | KRL variable diagnostics (resolved here) | `diag.src`/`diag.dat` data structure | VL-115 |
| D009 | Limited auto-retry, SAFE_IDLE, RECOVERY_RESET | `recovery.src` + `gripper.src` retry | VL-101 |
| D010 | SAFE_IDLE application-level state | State model; entry/exit conditions | ADR-0003 |

---

## 13. Implementation Plan

### Implementation order

| Phase | Component | Tasks | Verification |
|---|---|---|---|
| 1 | `main.dat` | Declare shared variables, signals, positions | Compilation check |
| 2 | `diag.src` / `diag.dat` | Implement data structure, record, preserve, clear, is_active | Unit: record, verify fields, clear |
| 3 | `gripper.src` / `gripper.dat` | Implement open/close, verify_grip/release, retry routines | Unit: simulate I/O, verify commands and verification |
| 4 | `recovery.src` / `recovery.dat` | Implement handle_safe_idle, handle_recovery_reset, enter_safe_idle | Unit: simulate RECOVERY_RESET, verify guard conditions |
| 5 | `main.src` | Implement INIT, check_conditions, execute_cycle, state machine | Integration: full cycle execution in OfficeLite |
| 6 | Integration | Connect all 4 files, verify state transitions, signal flow | OfficeLite: full state machine test |
| 7 | Failure scenarios | Simulate gripping failure, release failure, invalid state | OfficeLite: verify retry, SAFE_IDLE, RECOVERY_RESET |
| 8 | Anti-duplication | Hold CYCLE_REQUEST active, verify single cycle | OfficeLite: verify request_consumed behavior |

### Implementation constraints

- No production KRL code during architecture phase (this is planning only)
- Signal names are functional identifiers; final I/O mapping during implementation
- Position values require teaching or simulation setup (not architecture)
- Timeout values for gripper verification require implementation tuning
- All code must target KSS 8.3 syntax (ADR-0001)

---

## 14. Architecture Evaluation

### Proportionality assessment

| Criterion | Assessment |
|---|---|
| Minimum decomposition | 4 files — not 6. Production sequence, motion, and interface handling integrated into main program. Gripper, diagnostics, and recovery separated. |
| Complexity proportional | Single-cycle pick-and-place with bounded retry. No multi-cell coordination, no vision, no PLC. 4 files is proportional. |
| Coupling | main.src depends on 3 subprograms. Subprograms depend only on diag.src. No circular dependencies. Coupling is unidirectional and minimal. |
| Duplication | No duplicated responsibilities. Each routine has single owner. Diagnostic recording centralized in diag.src. |
| Scope creep | No architecture on unverified assumptions. No framework modifications. No KRL-specific skill created. No unplanned improvements. D008 resolved within authorized scope (architecture phase, reactivation condition met). |

### Required Architecture Questions -- Answers

| Question | Answer |
|---|---|
| Minimum proportional KRL decomposition? | 4 files: main.src, gripper.src, diag.src, recovery.src. 6 functional responsibilities mapped to 4 files. |
| Which component owns the application state machine? | `main.src` — owns app_state variable and all state transitions except SAFE_IDLE/RECOVERY_RESET_PROC internal logic. |
| Which component owns CYCLE_REQUEST consumption and rearming? | `main.src` — owns request_consumed flag. RECOVERY_RESET rearming delegated to `recovery.src` which writes to main.dat. |
| Which component owns CYCLE_COMPLETE? | `main.src` — set on successful cycle completion, cleared after rearming. |
| Which component owns SAFE_IDLE entry and exit transitions? | Entry: `main.src` calls `recovery.enter_safe_idle()`. Exit: `recovery.src` processes RECOVERY_RESET and transitions to IDLE. |
| Which component owns retry counters and retry execution? | `gripper.src` owns counters and execution. `main.src` resets counters at cycle start. |
| How are gripper commands separated from gripper verification? | Separate routines: close_gripper()/open_gripper() issue commands. verify_grip()/verify_release() read feedback only. |
| How are motion commands prevented during SAFE_IDLE and RECOVERY_RESET? | State machine does not enter CYCLE_ACTIVE from SAFE_IDLE or RECOVERY_RESET_PROC. No motion commands in handle_safe_idle() or handle_recovery_reset(). |
| How are diagnostics represented, preserved, and cleared? | KRL variables in diag.dat. Preserved via diag_active flag. Cleared only by diag.clear() during RECOVERY_RESET. |
| How does the architecture prevent repeated cycles from continuously active CYCLE_REQUEST? | request_consumed flag: set TRUE on cycle start, cleared only after CYCLE_REQUEST goes FALSE and cycle completes. One request = one cycle. |
| How does an unsuccessful cycle terminate without reporting CYCLE_COMPLETE? | CYCLE_COMPLETE stays FALSE on any failure path. Only set TRUE in set_cycle_complete() after successful cycle completion. |
| How will each acceptance criterion be verified later? | See section 12 traceability table. OfficeLite for logic, KUKA.Sim for motion, inspection for structure. |
| Does absence of KRL-specific framework skill create an architecture problem? | No. Existing framework contracts (ARCHITECTURE.md, robotics-cell-integration, gate contracts, AGENTS.md) provided sufficient guidance. robotics-cell-integration was consulted for integration contract patterns. The Engineering Architect and Robotics Engineer agent contracts define robot software architecture responsibility. No KRL-specific skill was needed. See section 15. |

---

## 15. Framework Skill Evaluation

### Question: Does the absence of a KRL-specific framework skill create an actual architecture problem?

**Answer: No.**

### Evidence

1. **ARCHITECTURE.md section 6.3 (robotics module)**: Activates for robot industrial
   projects. Skills under demand include `robotics-cell-integration`. No KRL-specific
   skill listed, but module activation is correct.

2. **robotics-cell-integration SKILL.md**: Provides integration contract guidance.
   Steps 16-17 distinguish "robot internal behavior" ownership. While its required
   outputs focus on integration contracts (PLC-robot handshake, cell states), the
   ownership distinction and state/transition methodology informed this architecture.

3. **Robotics Engineer agent (ARCHITECTURE.md section 9.3)**: Mission includes "robot
   cell architecture, estado robotico, senales, recuperacion." The agent contract
   covers robot software architecture responsibility without requiring a dedicated
   KRL skill.

4. **Engineering Architect (section 9.1)**: Coordinates architecture, selects
   modules/agents/skills. The architect can produce architecture artefacts using
   framework principles (proportionality, ownership, modularity) without a
   vendor-specific skill.

5. **AGENTS.md Global Core**: "Prefer simple, robust, maintainable solutions."
   "Select tools, agents, skills, and checks proportionally." The architecture was
   produced using these principles. A KRL-specific skill would add context cost
   without changing the architectural output for a project of this size.

6. **plc-software-architecture failure mode**: "Vendor lock-in innecesario." The
   framework is intentionally vendor-neutral. A KRL-specific skill would introduce
   vendor lock-in, contradicting this principle.

### Conclusion

The absence of a KRL-specific skill is **not a framework gap** for this project. The
existing framework contracts (ARCHITECTURE.md, agent contracts, module contracts,
gate contracts, AGENTS.md principles) provided sufficient guidance. The
UNDETERMINED observation (VL-023/031/047/054/064/073) can be reclassified:

**Classification**: Framework observation -- **RESOLVED (for this project)**. The
existing framework is sufficient for KRL robot software architecture at this project
complexity level. A KRL-specific skill may be beneficial for larger, more complex
KRL projects but is not needed here. No framework modification recommended.

---

## 16. Remaining Open Items

### Open decisions

| Decision | Status | Notes |
|---|---|---|
| D008 | **RESOLVED** (this architecture) | Diagnostics strategy defined. VL-115. |

**All 10 project decisions (D001-D010) are now resolved.**

### Remaining UNKNOWN items (not blocking architecture)

| ID | Item | Latest phase | Notes |
|---|---|---|---|
| U004 | Disponibilidad requerida | Architecture/Implementation | Not needed for architecture. Defer. |
| U005 | Mantenimiento | Architecture/Implementation | Not needed for architecture. Defer. |
| U006 | Plazos | Planificacion | No deadlines specified. |
| U007 | Entorno de despliegue | Architecture/Implementation | No deployment in scope (D002). |
| U013 | Formato de diagnosticos | ~~Arquitectura~~ — RESOLVED (D008) | KRL variables. |
| U014b | Posiciones -- valores fisicos | Implementacion | Requires teaching/simulation setup. |
| U015 | Ciclo tiempo / rendimiento | Architecture/Implementation | No performance requirement specified. |

### Remaining ambiguities (not blocking architecture)

7 of 9 ambiguities remain pending, linked to derivable decisions. None block
architecture. They will be addressed during implementation or flagged in Final
Verification if relevant.

### Framework observations

| Observation | Status | Notes |
|---|---|---|
| No KRL-specific skill | **RESOLVED (for this project)** | Section 15. Existing framework sufficient. |
| Output filename collision | UNDETERMINED | Framework observation, not a defect. |
| No corrective action output spec | UNDETERMINED | Framework observation. |
| No re-execution versioning spec | UNDETERMINED | Framework observation. |

### Residual risks

| Risk | Impact | Mitigation |
|---|---|---|
| No physical hardware (D002) | Cannot verify physical gripping, I/O timing | Document in Final Verification. Simulation evidence only. |
| Gripper I/O timing unknown | Timeout values not defined | Implementation tuning required. Architecture defines structure, not timing. |
| Position values not defined | Motion targets unknown | Teaching/simulation setup during implementation. Architecture defines positions by name. |
| KRL language features limited | No classes, namespaces | Architecture uses file-based modularity and naming conventions. |

---

## 17. Handoff

This `ROBOT_SOFTWARE_ARCHITECTURE.md` is delivered for external review.

**Next authorized action**: KRL implementation (after external review and
authorization).

Per framework contracts:
1. Implementation Review Gate will review KRL code against this architecture.
2. Final Verification Gate will verify acceptance criteria with fresh evidence.
3. D008 is resolved — no blocking decisions remain.

**Stop condition**: Architecture and planning artifacts complete. Stopping for
external review. No KRL implementation. No Implementation Review. No Final
Verification. No commit. No push.
