# ADR-0002: Safety Architecture Boundary for Application-Level KRL Software

## Status

ACCEPTED — 2026-07-10

## Context

This is a software validation and framework stress-test project, not a
production robot-cell deployment. No physical robot hardware is available. No
real safety system is being commissioned.

The Decision Readiness Gate (ROBOT_DR_GATE_REPORT.md) classified D003 as
BLOCKING with HIGH risk and difficult reversibility. The decision determines
the boundary between safety-rated robot/controller functions and
application-level KRL state and error handling.

The Project Owner is the decision owner, with Safety Specialist consultation.
The Safety Specialist role confirms that this scope boundary is sufficient for
software architecture and framework validation because no physical installation
or safety commissioning is included.

This decision affects D005 (operating conditions may include safety signals),
D009 (recovery must not be described as safety-rated), and D010 (safe state
must distinguish application-level from safety-rated).

## Decision

Safety-rated functions are outside the implementation scope of this project.

The KRL application software shall not implement, emulate, replace, or claim
responsibility for safety-rated functions.

The project shall maintain an explicit boundary between:

- safety-rated robot/controller functions;
- external safety architecture;
- application-level KRL state and error handling.

### Safety-rated functions owned by robot controller and external safety system

- Emergency stop behavior
- Protective stop behavior
- Safety-rated motion monitoring
- Safety I/O configuration
- Safety PLC implementation
- SafeOperation configuration

All of the above are outside project scope.

### Application-level functions within project scope

The KRL application may:

- detect application-level operating conditions;
- enter defined application states;
- stop or inhibit the production sequence according to normal application logic;
- expose diagnostic information;
- require explicit authorization before restarting production.

The KRL application shall not:

- bypass controller safety behavior;
- automatically recover from safety-rated stops;
- automatically restart production following a safety event;
- claim that an application-level safe state is equivalent to a safety-rated
  state.

### Recovery boundary

Application-level recovery shall never be described as a safety-rated function.

## Alternatives Considered

| Option | Description | Rejected because |
|---|---|---|
| Safety integrated in KUKA controller (SafeOperation) | Use KR C4 safety features within project | Out of scope — no physical hardware, no safety commissioning |
| External safety controller (safety PLC) | Integrate with external safety system | Out of scope — no PLC, no physical installation |
| Include safety-rated functions in KRL application | Implement safety logic in application software | Rejected — KRL application shall not implement, emulate, or replace safety-rated functions |
| No dedicated safety architecture (E-stop only) | Rely only on standard E-stop | Not applicable — safety-rated functions are owned by controller, not by application |
| Explicit boundary (SELECTED) | Application-level only; safety-rated owned by controller/external | Selected — proportional to validation project scope |

## Consequences

- **Application scope**: The KRL software handles application-level states,
  errors, and recovery only. Safety-rated functions are explicitly excluded.
- **D005 (operating conditions)**: Operating conditions are application-level
  only. Safety signals (e.g., safety OK) are not part of the application
  verification logic — they are owned by the controller/external safety system.
- **D009 (recovery strategy)**: Recovery is application-level only. Recovery
  from safety-rated stops is not in scope. Application-level recovery shall
  never be described as a safety-rated function.
- **D010 (safe state)**: The "safe state" in D010 refers to an application-level
  safe state (e.g., IDLE, ERROR_WAIT), not a safety-rated state. The
  application-level safe state is not equivalent to a safety-rated state.
- **Verification**: Requirements that cannot be fully verified without physical
  hardware or safety commissioning must be reported with appropriate verification
  limitations.
- **Future deployment**: Any future deployment on physical equipment shall
  require independent safety engineering according to applicable machinery and
  robotics requirements.

## Important Limitations

This decision does NOT constitute:

- A safety assessment
- A risk assessment
- A CE conformity assessment
- A production safety design

This decision is valid only for this software validation and framework
stress-test project. Any future deployment on physical equipment requires
independent safety engineering.

## Evidence

- Project Owner decision: 2026-07-10
- Safety Specialist consultation: confirmed scope boundary sufficient for
  software validation project
- DR Gate classification: BLOCKING, HIGH risk, difficult reversibility
- Resolution method: user decision + specialist consultation
- Decision recorded in: PROJECT_DISCOVERY.md section 13 (D003 status updated
  to RESOLVED)
- Validation log: VALIDATION_LOG.md (VL-082)

## References

- PROJECT_DISCOVERY.md section 13 (D003)
- ROBOT_DR_GATE_REPORT.md (DR Gate FAIL, D003 classification)
- gates/decision-readiness/GATE.md (Evidence Required: ADR as resolution evidence)
- docs/decisions/README.md (ADR creation criteria: hard to reverse, real
  alternatives, future agent could reopen)
- ADR-0001 (robot model and controller — KR C4 selected, safety features
  available but out of scope)
