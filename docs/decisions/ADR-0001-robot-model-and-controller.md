# ADR-0001: Robot Model and Controller Selection

## Status

ACCEPTED — 2026-07-10

## Context

The project requires a KUKA robot platform for industrial pick-and-place cycle
validation. The robot model and controller determine available KRL features,
safety integration options, compatible simulation/verification tools, and motion
capabilities. This decision blocks D002 (simulation environment), D003 (safety
architecture), and indirectly affects D006 (authorization interface), D010 (safe
state definition).

The Decision Readiness Gate (ROBOT_DR_GATE_REPORT.md) classified D001 as
BLOCKING with HIGH risk and difficult reversibility. The Project Owner is the
decision owner.

## Decision

**Robot model**: KUKA KR 6 R900 sixx
**Controller generation**: KR C4
**KSS version**: KSS 8.3

The project shall target standard KRL development for the KR C4 controller.

No optional KUKA technology packages shall be assumed unless explicitly
authorized by a later engineering decision.

The robot model, controller generation, and KSS version are now considered
resolved project constraints.

## Alternatives Considered

| Option | Description | Rejected because |
|---|---|---|
| KR C4 with KSS 8.x | Mature platform, well-documented KRL, broad tool support | — (SELECTED) |
| KR C5 with KSS 8.x/9.x | Newer platform, updated safety integration | Not selected by Project Owner |
| Sunrise controller | Java-based programming paradigm with KRL fallback | Different programming model; not selected by Project Owner |
| Other | Non-standard or unspecified platform | Not applicable |

## Consequences

- **KRL development**: Targets KSS 8.3 KRL syntax and features. Code must be
  compatible with KR C4 / KSS 8.3.
- **Simulation**: D002 resolution is now constrained to tools compatible with
  KR C4 / KSS 8.3 (e.g., KUKA Sim Pro, Office Lite for KSS 8.x).
- **Safety**: D003 resolution is now constrained to safety features available
  on KR C4 with KSS 8.3.
- **Technology packages**: No optional packages assumed. If motion features
  require a technology package (e.g., KUKA ConveyorTech, KUKA PalletTech),
  a later engineering decision must explicitly authorize its use.
- **Robot capabilities**: KR 6 R900 sixx has 6 kg payload and 900 mm reach.
  The part (0.5 kg, 100x60x40 mm per D004) is well within these limits.

## Evidence

- Project Owner decision: 2026-07-10
- DR Gate classification: BLOCKING, HIGH risk, difficult reversibility
- Resolution method: user decision
- Decision recorded in: PROJECT_DISCOVERY.md section 13 (D001 status updated
  to RESOLVED)
- Validation log: VALIDATION_LOG.md (VL-075)

## References

- PROJECT_DISCOVERY.md section 13 (D001)
- ROBOT_DR_GATE_REPORT.md (DR Gate FAIL, D001 classification)
- gates/decision-readiness/GATE.md (Evidence Required: ADR as resolution evidence)
- docs/decisions/README.md (ADR creation criteria: hard to reverse, real
  alternatives, future agent could reopen)
