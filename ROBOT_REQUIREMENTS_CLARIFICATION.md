# ROBOT_REQUIREMENTS_CLARIFICATION.md

ROBER ENGINEERING STACK -- Requirements Clarification Proposal
Project: Industrial Robot Software Validation -- 6-axis pick-and-place (KUKA KRL)
Date: 2026-07-10
Owner: Engineering Architect
Purpose: Address RQ Gate FAIL corrective action -- propose acceptance criteria for external user review
Status: **USER APPROVED 2026-07-10** -- R01-R08, R10, R12 approved; R09 blocked by D009; R11 blocked by D010

---

## 1. Context

The Requirements Quality Gate (ROBOT_RQ_GATE_REPORT.md) returned **FAIL** because
no acceptance criteria exist for any of the 12 project requirements. This
document analyses each requirement against existing project information
(`PROJECT_DISCOVERY.md`, original user requirements) and proposes acceptance
criteria where sufficient information exists.

### Constraints on this pass

- Do not resolve D001-D006, D009 or D010
- Do not invent numeric thresholds, timing values, tolerances, signal names,
  robot models, hardware capabilities or safety requirements
- Do not silently convert assumptions into requirements
- Formulate behavioral criteria that remain valid independently of the final
  KUKA robot model or physical coordinate values where possible

---

## 2. Requirements clarification proposal

### Summary table

| ID | Requirement | Proposed acceptance criterion | Evidence required | Dependency on open decisions | Status |
|---|---|---|---|---|---|
| R01 | Execute automatic pick-and-place cycle | The robot software shall execute the complete 12-step cycle sequence (as defined in PROJECT_DISCOVERY.md section 3) from [Espera autorizacion] through [Reportar completitud de ciclo] and return to [Espera autorizacion], without skipping or reordering steps. | Cycle execution trace showing all 12 steps executed in sequence. | None -- sequence is FACT defined by user. | READY FOR USER APPROVAL |
| R02 | No cycle start without authorization | The robot software shall not transition from the wait-authorization state to the verify-conditions state unless an authorization signal is present. | State machine trace showing no state transition without authorization signal. | D006 (mechanism) -- criterion is behavioral and does not depend on mechanism. | READY FOR USER APPROVAL |
| R03 | Use approach positions | The robot software shall move to an approach position before moving to the pick position (step 3 to step 4), and shall move to an approach position before moving to the place position (step 7 to step 8), as defined in the cycle sequence. | Motion trace showing approach position visited before pick and before place. | None -- approach positions are CONSTRAINT defined by user. Criterion is behavioral, does not depend on physical coordinate values (U014b). | READY FOR USER APPROVAL |
| R04 | Control gripper via digital signals | The robot software shall activate the gripper via digital output signal(s) at step 5 of the cycle sequence and shall deactivate the gripper via digital output signal(s) at step 9 of the cycle sequence. | I/O trace showing digital output activation at step 5 and deactivation at step 9. | D004 (gripper specs) -- criterion is behavioral and does not depend on specific signal names or gripper type. | READY FOR USER APPROVAL |
| R05 | Verify gripping | The robot software shall verify that the gripper has successfully grasped the part before proceeding from step 6 (Verificar agarre) to step 7 (Retirar de pick area). If gripping is not confirmed, the robot shall not proceed to step 7 and shall transition to a failure-handling state. | State machine trace showing no transition to step 7 without grip confirmation; trace showing transition to failure state when grip is not confirmed. | D004 (gripper specs), U010 (feedback signal) -- criterion is behavioral. Verification method depends on D004 but criterion does not. | READY FOR USER APPROVAL |
| R06 | Verify release | The robot software shall verify that the part has been successfully released before proceeding from step 10 (Verificar liberacion) to step 11 (Retornar a posicion segura). If release is not confirmed, the robot shall not proceed to step 11 and shall transition to a failure-handling state. | State machine trace showing no transition to step 11 without release confirmation; trace showing transition to failure state when release is not confirmed. | D004 (gripper specs), U010 (feedback signal) -- criterion is behavioral. Verification method depends on D004 but criterion does not. | READY FOR USER APPROVAL |
| R07 | Detect relevant execution failures | The robot software shall detect the following relevant execution failures: (a) gripping failure, (b) release failure, (c) cycle authorization lost or invalid when evaluated according to the final authorization contract, (d) required operating condition not satisfied before cycle start, (e) invalid or unexpected internal cycle state. Upon detection, the robot shall transition to a diagnostic state instead of continuing the cycle. The following failures are NOT required as project-level software requirements at this stage: robot controller motion faults, collisions, emergency stop activation, safety-system faults, physical position deviation, communication loss with external systems, cycle timeout. These exclusions mean that handling of these failures is outside the current project software scope unless a later engineering decision demonstrates that explicit KRL application-level handling is required. | Failure injection test: inject each of the 5 relevant failures; verify robot enters diagnostic state and does not continue cycle. | D006 (authorization contract) for failure (c). Criterion is otherwise independent of D001-D006, D009, D010. | READY FOR USER APPROVAL (APPROVED 2026-07-10) |
| R08 | Provide useful diagnostics | The robot software shall record and make available diagnostic information when a failure is detected. At minimum, the diagnostic information shall include: (a) the current production sequence step or state, (b) the detected failure type, (c) whether operator or maintenance intervention is required, (d) whether recovery is available according to the final recovery strategy. Diagnostics are intended primarily for maintenance and engineering personnel. No timestamp requirement. No severity-level model required. No external HMI, database, logging system or communication protocol required. The final KRL representation shall be determined during architecture and implementation. | Diagnostic log review: trigger each of the 5 relevant failures; verify diagnostic output contains step/state, failure type, intervention requirement, and recovery availability. | D009 (recovery strategy) for field (d). D008 (diagnostics strategy, deferible). Criterion is otherwise independent of D001-D006, D010. | READY FOR USER APPROVAL (APPROVED 2026-07-10) |
| R09 | Support recovery from failures | Not proposed -- acceptance criterion depends on D009 (Recovery Strategy). The recovery strategy determines what recovery actions are available, when they are triggered, and what success looks like. Without knowing whether recovery is automatic, manual, or hybrid, no behavioral criterion can be formulated that remains valid across all possible recovery strategies. | N/A -- blocked. | D009 (Recovery Strategy) -- BLOCKING. Must be resolved before criterion can be proposed. | BLOCKED BY DECISION |
| R10 | Prevent duplicate cycle execution | The robot software shall not initiate a new cycle while a cycle is in progress. The robot software shall not execute more than one cycle per authorization signal. | State machine trace showing: (a) no overlapping cycle execution; (b) single cycle completion per authorization signal. | D006 (authorization interface) -- criterion is behavioral and does not depend on mechanism. | READY FOR USER APPROVAL |
| R11 | Return to safe state | Not proposed -- acceptance criterion depends on D010 (Safe State Definition). The safe state definition determines what state the robot transitions to, what conditions trigger the transition, and what "safe" means. Without knowing what the safe state is, no behavioral criterion can be formulated. | N/A -- blocked. | D010 (Safe State Definition) -- BLOCKING. Must be resolved before criterion can be proposed. | BLOCKED BY DECISION |
| R12 | Modular architecture | The robot software shall be structured into the six modules specified in the project constraints: (1) production sequence, (2) motion logic, (3) gripper control, (4) interface handling, (5) diagnostics, (6) recovery behavior. Each module shall have explicit ownership and defined interfaces to other modules. | Architecture document review: verify six modules exist, each has ownership assignment, and inter-module interfaces are defined. | None -- module structure is CONSTRAINT defined by user. | READY FOR USER APPROVAL |

---

## 3. Status summary

| Status | Count | Requirements |
|---|---|---|
| READY FOR USER APPROVAL | 10 | R01, R02, R03, R04, R05, R06, R07, R08, R10, R12 |
| REQUIRES USER INPUT | 0 | (All answered) |
| BLOCKED BY DECISION | 2 | R09 (D009), R11 (D010) |

---

## 4. Detailed analysis per requirement

### R01 -- Execute automatic pick-and-place cycle

**Source**: PROJECT_DISCOVERY.md section 3 (FACT -- 12-step sequence defined by user).

**Derivation**: The user defined a 12-step cycle sequence. The acceptance
criterion is directly derivable: the software must execute all 12 steps in
order. This is a behavioral criterion that does not depend on robot model,
physical coordinates, or timing values.

**Why READY FOR USER APPROVAL**: The criterion is fully derivable from existing
FACT information. The user needs only to confirm that "successful cycle
execution" means "all 12 steps completed in order without skipping."

**Verification evidence**: Cycle execution trace showing all 12 steps executed
in sequence. This can be produced in simulation or on hardware.

---

### R02 -- No cycle start without authorization

**Source**: PROJECT_DISCOVERY.md section 8 (CONSTRAINT -- "No iniciar ciclo sin
autorizacion").

**Derivation**: The constraint is explicit. The behavioral criterion is: no
state transition from wait to cycle-start without authorization signal present.
This does not depend on HOW authorization is signaled (D006) -- only that it
must be present.

**Why READY FOR USER APPROVAL**: The criterion is behavioral and model-
independent. D006 determines the mechanism (signal name, source, encoding) but
not the behavioral requirement.

**Verification evidence**: State machine trace showing no transition without
authorization.

---

### R03 -- Use approach positions

**Source**: PROJECT_DISCOVERY.md section 8 (CONSTRAINT -- "Usar posiciones de
aproximacion antes de pick y place").

**Derivation**: The cycle sequence (section 3) defines steps 3 (move to pick
approach) and 7 (move to place approach). The criterion requires that approach
positions are visited before pick and place positions. This is behavioral and
does not depend on physical coordinate values (U014b).

**Why READY FOR USER APPROVAL**: The criterion is fully derivable from the
FACT sequence and the CONSTRAINT. Physical coordinates are not needed.

**Verification evidence**: Motion trace showing approach position visited
before pick and before place.

---

### R04 -- Control gripper via digital signals

**Source**: PROJECT_DISCOVERY.md section 7 (FACT -- "through digital signals")
and section 3 (steps 5 and 9).

**Derivation**: The user specified digital signals as the gripper control
mechanism. The cycle sequence defines when gripper activates (step 5) and
deactivates (step 9). The criterion requires digital output activation at the
correct steps.

**Why READY FOR USER APPROVAL**: The criterion is behavioral. D004 (gripper
specs) determines which specific signals and gripper type, but the criterion
only requires that digital outputs are used at the correct cycle steps.

**Verification evidence**: I/O trace showing digital output activation at step
5 and deactivation at step 9.

---

### R05 -- Verify gripping

**Source**: PROJECT_DISCOVERY.md section 3 (FACT -- step 6: Verificar agarre).

**Derivation**: The cycle sequence includes a verification step after gripping.
The behavioral requirement is: do not proceed to step 7 unless grip is
confirmed. If grip is not confirmed, transition to failure handling. This is
derivable from the sequence structure -- the verification step exists to gate
progression.

**Why READY FOR USER APPROVAL**: The criterion is behavioral. The verification
METHOD (sensor type, signal name) depends on D004 and U010, but the criterion
only requires that the robot does not proceed without confirmation.

**Verification evidence**: State machine trace showing no transition to step 7
without grip confirmation; trace showing failure-state transition when grip is
not confirmed.

---

### R06 -- Verify release

**Source**: PROJECT_DISCOVERY.md section 3 (FACT -- step 10: Verificar
liberacion).

**Derivation**: Same analysis as R05. The cycle sequence includes a
verification step after release. The behavioral requirement is: do not proceed
to step 11 unless release is confirmed.

**Why READY FOR USER APPROVAL**: Same as R05. Behavioral criterion, independent
of verification method.

**Verification evidence**: State machine trace showing no transition to step 11
without release confirmation; trace showing failure-state transition when
release is not confirmed.

---

### R07 -- Detect relevant execution failures

**Source**: PROJECT_DISCOVERY.md section 10 (FACT -- "The robot shall detect
relevant execution failures"; clarified by user 2026-07-10).

**User decision**: The following failures are relevant and must be detected:
1. Gripping failure
2. Release failure
3. Cycle authorization lost or invalid when evaluated according to the final
   authorization contract
4. Required operating condition not satisfied before cycle start
5. Invalid or unexpected internal cycle state

The following failures are NOT required as project-level software requirements:
- Robot controller motion faults
- Collisions
- Emergency stop activation
- Safety-system faults
- Physical position deviation
- Communication loss with external systems
- Cycle timeout

These exclusions mean that handling of these failures is outside the current
project software scope unless a later engineering decision demonstrates that
explicit KRL application-level handling is required.

**Derivation**: The user confirmed the relevant failure set. The criterion is
behavioral: detect the 5 specified failures and transition to diagnostic state.

**Why READY FOR USER APPROVAL (APPROVED)**: User confirmed the failure set and
the behavioral criterion. D006 (authorization contract) is needed for failure
(c) evaluation, but the criterion itself is defined.

**Verification evidence**: Failure injection test for each of the 5 relevant
failures; verify robot enters diagnostic state and does not continue cycle.

---

### R08 -- Provide useful diagnostics

**Source**: PROJECT_DISCOVERY.md section 10 (FACT -- "The robot shall provide
useful diagnostics"; clarified by user 2026-07-10).

**User decision**: Diagnostics shall be intended primarily for maintenance and
engineering personnel. For each project-level execution failure detected, the
diagnostic information shall identify at minimum:
1. The current production sequence step or state
2. The detected failure type
3. Whether operator or maintenance intervention is required
4. Whether recovery is available according to the final recovery strategy

No timestamp requirement. No severity-level model required. No external HMI,
database, logging system or communication protocol required. The final KRL
representation shall be determined during architecture and implementation.

**Derivation**: The user defined what "useful" means: four specific diagnostic
fields, maintenance/engineering audience, no timestamp, no severity, no
external system. The criterion is fully specified.

**Why READY FOR USER APPROVAL (APPROVED)**: User confirmed the diagnostic
content, audience, and constraints. D009 (recovery strategy) is needed for
field (d) but the criterion itself is defined.

**Verification evidence**: Diagnostic log review after failure injection;
verify output contains step/state, failure type, intervention requirement,
and recovery availability.

---

### R09 -- Support recovery from failures

**Source**: PROJECT_DISCOVERY.md section 10 (FACT -- "The robot shall support
recovery from failures when appropriate").

**Derivation**: Not possible. The acceptance criterion depends entirely on D009
(Recovery Strategy). Without knowing:
- Whether recovery is automatic, manual, or hybrid
- What conditions trigger recovery ("when appropriate")
- What recovery actions are available
- What constitutes successful recovery

...no behavioral criterion can be formulated that remains valid across all
possible recovery strategies.

**Why BLOCKED BY DECISION**: D009 (Recovery Strategy) is BLOCKING before
architecture. The criterion cannot be proposed until D009 is resolved.

**Verification evidence**: N/A -- blocked.

---

### R10 -- Prevent duplicate cycle execution

**Source**: PROJECT_DISCOVERY.md section 8 (CONSTRAINT -- "Prevenir ejecucion
duplicada de ciclo").

**Derivation**: The constraint is explicit. Two behavioral requirements are
derivable:
1. No new cycle while a cycle is in progress (no overlapping cycles)
2. No more than one cycle per authorization signal (no double-triggering)

The cycle sequence (section 3) shows [Espera autorizacion] as the loop entry
point -- a new cycle only starts after the previous completes and returns to
wait state.

**Why READY FOR USER APPROVAL**: The criterion is behavioral and model-
independent. D006 (authorization interface) determines the mechanism but not
the behavioral requirement.

**Verification evidence**: State machine trace showing no overlapping cycles
and single cycle per authorization.

---

### R11 -- Return to safe state

**Source**: PROJECT_DISCOVERY.md section 8 (CONSTRAINT -- "Retornar a estado
seguro cuando se requiera") and section 10 (FACT -- "The robot shall return to
a defined safe state when required").

**Derivation**: Not possible. The acceptance criterion depends entirely on D010
(Safe State Definition). Without knowing:
- What the safe state is (position, state-machine state, or both)
- What conditions trigger the transition ("when required")
- What "safe" means in context

...no behavioral criterion can be formulated.

**Why BLOCKED BY DECISION**: D010 (Safe State Definition) is BLOCKING before
architecture. The criterion cannot be proposed until D010 is resolved.

**Verification evidence**: N/A -- blocked.

---

### R12 -- Modular architecture

**Source**: PROJECT_DISCOVERY.md section 8 (CONSTRAINT -- "Arquitectura
modular") and section 2 (FACT -- six modules: production sequence, motion
logic, gripper control, interface handling, diagnostics, recovery behavior).

**Derivation**: The user explicitly required six modules. The criterion
requires that the software is structured into these six modules with explicit
ownership and defined interfaces. This is fully derivable from the constraint.

**Why READY FOR USER APPROVAL**: The criterion is fully derivable from existing
CONSTRAINT and FACT information. No unresolved decision blocks it.

**Verification evidence**: Architecture document review showing six modules,
ownership, and inter-module interfaces.

---

## 5. User answers (received 2026-07-10)

### Q1 -- Relevant failures (R07) -- ANSWERED

**User decision**: The following failures are relevant and must be detected:
1. Gripping failure
2. Release failure
3. Cycle authorization lost or invalid when evaluated according to the final
   authorization contract
4. Required operating condition not satisfied before cycle start
5. Invalid or unexpected internal cycle state

The following are NOT required as project-level software requirements at this
stage: robot controller motion faults, collisions, emergency stop activation,
safety-system faults, physical position deviation, communication loss with
external systems, cycle timeout. These exclusions mean handling is outside
current project software scope unless a later engineering decision demonstrates
explicit KRL application-level handling is required.

### Q2 -- Useful diagnostics (R08) -- ANSWERED

**User decision**: Diagnostics for maintenance and engineering personnel. For
each detected failure: (a) current production sequence step or state, (b)
detected failure type, (c) whether operator or maintenance intervention is
required, (d) whether recovery is available according to the final recovery
strategy. No timestamp. No severity levels. No external HMI, database, logging
system or communication protocol. Final KRL representation determined during
architecture and implementation.

### Q3 -- Confirmation of READY FOR USER APPROVAL criteria (R01-R06, R10, R12) -- APPROVED

**User decision**: All 8 criteria approved as proposed. R07 and R08 clarified
criteria also approved.

---

## 6. Dependencies on unresolved decisions

| Requirement | Open decision | Impact on criterion | Criterion status without resolution |
|---|---|---|---|
| R07 | D006 (authorization contract) | Needed for failure (c) evaluation | APPROVED -- criterion defined, D006 needed for implementation only |
| R08 | D009 (recovery strategy) | Needed for field (d) "recovery available" | APPROVED -- criterion defined, D009 needed for implementation only |
| R09 | D009 (recovery strategy) | Determines recovery behavior, triggers, success criteria | BLOCKED -- no criterion proposed |
| R11 | D010 (safe state definition) | Determines safe state, triggers | BLOCKED -- no criterion proposed |

**Note**: D002-D006 do not directly block acceptance criteria formulation for
R01-R06, R10, R12 because those criteria are behavioral and model-independent.
D002-D006 will block architecture and implementation but not the acceptance
criteria proposed here.

---

## 7. Scope creep prevention

During this clarification pass, the following scope creep risks were
identified and prevented:

1. **Inventing numeric thresholds**: No cycle time, positioning tolerance, or
   timing values were invented. Criteria are behavioral, not quantitative.
2. **Inventing signal names**: No specific digital signal names were proposed.
   Criteria refer to "digital output signal(s)" generically.
3. **Inventing safety requirements**: No safety categories, performance levels,
   or safety functions were proposed. D003 (Safety Architecture) remains
   unresolved.
4. **Converting assumptions to requirements**: The 8 potential failures
   (PROJECT_DISCOVERY.md section 10) remain ASSUMPTIONS. They were not
   converted into requirements. The user must confirm which are relevant.
5. **Resolving blocking decisions**: D001-D006, D009, D010 were not resolved.
   Criteria that depend on these decisions are either marked REQUIRES USER
   INPUT or BLOCKED BY DECISION.

---

## 8. Framework observations

### KRL-specific robot software architecture skill (VL-023/031/047)

**Status**: UNDETERMINED. No change.

This clarification pass did not produce evidence that would change the
classification. The pass operates on requirements, not architecture. The
question remains open for the architecture phase.

### Artefact naming

This pass produces `ROBOT_REQUIREMENTS_CLARIFICATION.md` as a project-specific
artefact. The RQ Gate contract does not specify a standard name for
clarification proposals (corrective action output). This is consistent with
the framework -- corrective actions are not gated artefacts with fixed names.

---

## 9. Proposed next authorized action

After user review and approval of this clarification proposal:

1. **If user approves the 8 READY FOR USER APPROVAL criteria**: Those criteria
   become confirmed acceptance criteria for the project.
2. **If user answers Q1 and Q2**: R07 and R08 criteria can be finalized.
3. **If user confirms or modifies the READY FOR USER APPROVAL criteria**:
   Update the acceptance criteria in the project artefacts.
4. **Re-execute RQ Gate**: With confirmed acceptance criteria for R01-R08, R10,
   R12, the RQ Gate can re-evaluate. R09 and R11 will remain FAIL conditions
   (blocked by D009 and D010), but the RQ Gate may be able to PASS with those
   blocking decisions derived to the DR Gate -- IF the acceptance criteria for
   R09 and R11 can be deferred to the DR Gate resolution.

**Important**: The RQ Gate FAIL was caused by three FAIL criteria:
1. Missing acceptance criteria (all 12 requirements)
2. Blocking decision without information (D007)
3. Objective not verifiable

If 10 of 12 requirements have acceptance criteria (R01-R08, R10, R12), and R09
and R11 are blocked by D009 and D010 (which have sufficient information to
derive to DR Gate), then:
- FAIL criterion 1 (missing acceptance criteria) may be partially resolved
- FAIL criterion 3 (blocking decision without information) may be resolved if
  D009 and D010 are classified as derivable to DR Gate
- FAIL criterion 6 (objective not verifiable) may be partially resolved

The RQ Gate re-execution will determine the final verdict.

**Proposed next authorized action**: User reviews and approves/modifies this
clarification proposal, answers Q1-Q3, then authorizes RQ Gate re-execution.
