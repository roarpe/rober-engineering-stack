# Skill -- industrial-project-verification

## Name

industrial-project-verification

## Purpose

Disenar una estrategia de verificacion industrial transversal que permita
demostrar progresivamente que un sistema cumple sus requisitos y contratos
tecnicos. La skill diseña que debe verificarse, en que nivel, con que metodo,
con que evidencia, cuando, por quien, en que entorno y contra que criterio.

Esta skill NO ejecuta la decision final PASS/FAIL de completitud. El Final
Verification Gate conserva la autoridad exclusiva sobre el PASS/FAIL tecnico
final.

## Activation Triggers

- Proyecto industrial mediano o grande con multiples subsistemas.
- Existen PLC, robot, software, vision, IA o comunicaciones.
- Existen requisitos de integracion o riesgos tecnicos relevantes.
- Existen criterios de aceptacion complejos.
- Existe necesidad de FAT, SAT, commissioning o simulacion.
- Existe necesidad de validacion de recuperacion.
- Existe necesidad de trazabilidad requisito -> evidencia.

## When Not To Use

- La tarea es trivial.
- Final Verification proporcional es suficiente.
- No existe estrategia de verificacion adicional que disenar.
- El proyecto es un experimento desechable sin claims de ingenieria.

## Primary Owner

QA & Debug Engineer

## Participants

- Engineering Architect (coherencia transversal, entry/exit criteria).
- Industrial Automation Engineer (verificacion PLC/automatizacion).
- Robotics Engineer (verificacion robotica).
- Software Engineer (verificacion de software).
- Technical Documentation Engineer (verificacion de documentacion cuando
  aplique).

## Required Inputs

- Requisitos validados (salida de Requirements Quality Gate).
- Decision map resuelto (salida de Decision Readiness Gate, si aplica).
- Arquitecturas de dominio existentes (PLC, robot, software, comunicaciones,
  vision/IA, diagnostico).
- Criterios de aceptacion.
- Contratos de comunicacion e integracion.
- ADRs aplicables.
- Resultados de gates previos.

## Procedure

1. Confirmar precondiciones: RQ PASS y DR PASS (si aplica).
2. Definir objetivos de verificacion.
3. Definir alcance y limites del sistema.
4. Construir requirements traceability: REQUIREMENT -> VERIFICATION METHOD ->
   EXECUTION -> EVIDENCE -> RESULT -> FINAL VERIFICATION CLAIM.
5. Identificar requisitos sin metodo de verificacion.
6. Identificar metodos sin requisito o claim.
7. Definir verification levels proporcionales:
   - Component Level: verificacion de componentes individuales.
   - Subsystem Level: PLC, robot, software, vision/IA, comunicaciones.
   - Integration Level: verificacion de contratos entre subsistemas.
   - System Level: verificacion del comportamiento del sistema completo.
   - Operational Level: FAT, SAT, commissioning, operacion, mantenimiento,
     recuperacion (cuando aplique).
8. Para cada elemento relevante, definir Verification Method Contract:
   - Verification ID.
   - Requirement/Claim.
   - Level.
   - Method.
   - Environment.
   - Preconditions.
   - Required Inputs.
   - Expected Result.
   - Evidence Required.
   - Owner.
   - Reviewer cuando aplique.
   - Entry Criteria.
   - Exit Criteria.
   - Dependencies.
   - Status (planned, ready, blocked, executed, passed, failed, deferred).
9. Definir verification environments (simulacion, emulacion, HIL, SIL,
   laboratorio, produccion).
10. Definir responsabilidades e independence requirements.
11. Definir entry y exit criteria por nivel.
12. Definir execution sequence.
13. Definir Industrial Failure Verification: no verificar unicamente happy
    paths. Considerar cuando aplique:
    - Communication loss.
    - Timeout.
    - Stale data.
    - Invalid data.
    - Unavailable device.
    - Robot fault.
    - PLC fault.
    - Software failure.
    - Vision/AI invalid result.
    - Vision/AI unavailable.
    - Restart.
    - Recovery.
    - Degraded mode.
    - Interrupted sequence.
    - Persistence failure.
    - Resource exhaustion.
14. Definir recovery verification.
15. Definir performance, timing, latency, throughput y reliability cuando
    aplique.
16. Definir diagnostics verification.
17. Definir documentation verification (que documentacion requerida existe,
    esta actualizada, es coherente y es consumible).
18. Definir Evidence Policy:
    - Evidencia requerida por verificacion.
    - Origen.
    - Formato.
    - Owner.
    - Almacenamiento cuando aplique.
    - Trazabilidad.
    - Reproducibilidad.
    - Criterio de aceptacion.
19. No asumir que: test ejecutado significa test valido; log existente
    significa evidencia suficiente; resultado historico significa fresh
    evidence; ausencia de error significa cumplimiento.
20. Definir test data y simulacion.
21. Definir riesgos residuales.
22. Registrar decisiones abiertas.
23. Producir el artefacto de salida.

### Frontera arquitectonica obligatoria

- **Verification Strategy** (esta skill): diseña verification scope, levels,
  methods, environments, evidence requirements, traceability,
  responsibilities, execution sequence, entry/exit criteria.
- **Implementation Review** (Implementation Review Gate): revisa SPEC,
  STANDARDS, findings, severities, corrective actions.
- **Final Verification** (Final Verification Gate): ejecuta evaluacion final
  de claims, comproba fresh evidence, decision tecnica PASS/FAIL.

La skill no duplica ninguno de los dos gates.

### Requirements Traceability

La estrategia debe permitir identificar:

- Requisitos sin metodo de verificacion.
- Metodos sin requisito o claim.
- Evidencia insuficiente.
- Dependencias bloqueantes.
- Riesgos residuales.

## Required Outputs

Artefacto: `INDUSTRIAL_PROJECT_VERIFICATION.md`

Contenido obligatorio:

- Verification objectives.
- Scope y boundaries.
- Verification levels.
- Verification methods (con 15 campos por elemento).
- Verification environments.
- Requirements traceability model.
- Responsibilities e independence requirements.
- Entry criteria.
- Exit criteria.
- Execution sequence.
- Evidence policy.
- Failure verification (happy + fault paths).
- Recovery verification.
- Performance/timing/latency/throughput cuando aplique.
- Diagnostics verification.
- Documentation verification.
- Residual risks.
- Open decisions.

## Consumer

Engineering Architect (coherencia transversal), QA & Debug Engineer (ejecucion
de verificacion), Final Verification Gate (consume evidencia producida).

## Stop Condition

La skill se detiene cuando existe una estrategia de verificacion suficiente
para demostrar progresivamente requisitos y contratos mediante metodos,
responsabilidades y evidencia trazables. No debe continuar hasta ejecutar
todas las verificaciones.

## Gates Interaction

- **Precondicion**: Requirements Quality PASS. Decision Readiness PASS (si
  aplica).
- **Despues de**: la estrategia se entrega a planificacion y ejecucion de
  verificacion. Final Verification Gate consume la evidencia producida.
- **No ejecuta**: la decision PASS/FAIL final. Final Verification Gate
  conserva autoridad exclusiva.
- **No duplica**: Implementation Review Gate (revisa SPEC/STANDARDS/findings)
  ni Final Verification Gate (evalua claims con fresh evidence y decide
  PASS/FAIL).
- **No reemplaza**: ADRs. Las decisiones de verificacion dificiles de
  revertir se proponen como ADR.

## Agent Interaction

- **Activada por**: QA & Debug Engineer (owner).
- **Coordina con**: Engineering Architect (entry/exit criteria, transversal),
  especialistas de dominio (verificacion de su subsistema), Technical
  Documentation Engineer (verificacion de documentacion).
- **Handoff a**: QA & Debug Engineer para ejecucion de verificacion; Final
  Verification Gate para evaluacion final.

## Evidence Required

- `INDUSTRIAL_PROJECT_VERIFICATION.md` con todos los campos obligatorios.
- Verification Method Contract completo por elemento relevante.
- Requirements traceability model con cobertura de requisitos.
- Failure verification incluye fault paths, no solo happy paths.
- Evidence policy definida con origen, formato, owner, trazabilidad y
  reproducibilidad.
- Riesgos residuales identificados.

## Failure Modes

- Ejecutar Final Verification o declarar PASS/FAIL final.
- Duplicar Implementation Review (revisar SPEC/STANDARDS/findings).
- Duplicar Final Verification (evaluar claims con fresh evidence).
- Sustituir testing de dominio (responsabilidad de especialistas).
- Implementar automaticamente tests.
- Ocultar verificaciones fallidas.
- Cambiar requisitos para hacer pasar verificaciones.
- Aceptar evidencia insuficiente.
- Asumir que todos los proyectos necesitan todos los niveles.
- Verificar unicamente happy paths sin fault paths.
- Asumir que test ejecutado significa test valido.
- Asumir que ausencia de error significa cumplimiento.
- No definir independence requirements cuando aplique.

## Escalation Rules

- Conflicto entre verificacion y arquitectura -> Engineering Architect.
- Verificacion de dominio PLC -> Industrial Automation Engineer.
- Verificacion de dominio robot -> Robotics Engineer.
- Verificacion de software -> Software Engineer.
- Verificacion de documentacion -> Technical Documentation Engineer.
- Decision de verificacion dificil de revertir -> proponer ADR.
- Evidencia insuficiente o bloqueada -> escalar a especialista para
  correccion.
- Riesgo que supera verificacion -> escalar al usuario.

## Done Criteria

- `INDUSTRIAL_PROJECT_VERIFICATION.md` completo con todos los campos
  obligatorios.
- Verification Method Contract completo por elemento relevante.
- Requirements traceability model con cobertura identificada.
- Verification levels definidos proporcionalmente.
- Failure verification incluye fault paths.
- Evidence policy definida.
- No duplica Implementation Review ni Final Verification.
- Final Verification Gate conserva autoridad exclusiva sobre PASS/FAIL.
- Riesgos residuales identificados.
- Artefacto entregado a QA & Debug Engineer para ejecucion.
