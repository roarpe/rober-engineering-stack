# Gate 2 -- Decision Readiness

## Name

Decision Readiness Gate

## Purpose

Determinar si las decisiones tecnicas bloqueantes estan resueltas con
evidencia. Evitar disenar arquitectura sobre suposiciones no verificadas.
Distinguir decisiones bloqueantes de deferibles y registrar dependencias entre
ellas. Tener un plan de resolucion (owner y Resolution Method) no es suficiente
para PASS; el plan debe ejecutarse y producir evidencia.

## Trigger

- Requirements Quality detecta decisiones abiertas.
- Hay multiples alternativas arquitectonicas viables.
- Existen dependencias entre decisiones.
- La incertidumbre tecnica podria requerir prototipo.

## When Not To Use

- La solucion es obvia, reversible y de bajo riesgo.
- Ya existe ADR aplicable que cubre la decision.
- El trabajo es puramente mecanico.
- No hay decisiones tecnicas abiertas despues de Requirements Quality.

## Owner

Engineering Architect

## Participants

- Software Engineer, Industrial Automation Engineer, Robotics Engineer o QA &
  Debug Engineer segun el tipo de decision.
- Technical Documentation Engineer si se proponen ADRs.

## Required Inputs

- Requisitos validados (salida de Requirements Quality Gate).
- Riesgos identificados.
- Restricciones tecnicas.
- Opciones conocidas.
- Evidencia disponible.
- ADRs existentes si aplican.

## Procedure

1. Recibir la lista de decisiones abiertas desde Requirements Quality.
2. Para cada decision relevante, registrar:
   - Decision ID.
   - Question (pregunta concreta).
   - Context (por que es relevante).
   - Options (alternativas identificadas).
   - Missing Information (datos faltantes para decidir).
   - Dependencies (otras decisiones que afectan o son afectadas).
   - Risk (impacto si la decision es incorrecta).
   - Reversibility (facil/dificil de revertir).
   - Owner (responsable de la resolucion).
   - Resolution Method (como se resolvera).
   - Status (open/resolved/deferred).
3. Clasificar cada decision como blocking o deferrable.
4. Para decisiones blocking, verificar si estan resueltas con evidencia. Si no
   estan resueltas, registrar el plan de resolucion (owner, Resolution Method)
   pero el gate permanece FAIL hasta ejecutar dicho plan y obtener evidencia.
5. Para decisiones deferrables, confirmar que pueden posponerse. Deben tener
   owner, justificacion, riesgo aceptado y condicion explicita de reactivacion.
6. Verificar que las dependencias entre decisiones estan claras.
7. Producir el artefacto de salida con la decision PASS o FAIL.

### Resolution Method

Puede ser uno de:

- `research` -- investigacion dirigida.
- `prototype` -- prototipo desechable para validar viabilidad.
- `user decision` -- decision del usuario.
- `specialist consultation` -- consulta a especialista de dominio.
- `ADR` -- registro formal de decision arquitectonica.
- `defer` -- posponer con justificacion y condicion de reactivacion.

## Required Outputs

Artefacto: `DECISION_MAP.md`

Contenido obligatorio:

- Lista de decisiones con todos los campos del procedimiento.
- Clasificacion blocking/deferrable para cada decision.
- Estado de cada decision: resolved, open (con plan de resolucion) o deferred.
- Dependencias entre decisiones mapeadas.
- Recomendaciones de prototipo, investigacion o ADR cuando aplique.
- Decision: PASS o FAIL.

## PASS Criteria

- Todas las decisiones blocking estan resueltas con evidencia (status:
  resolved). Tener unicamente owner y Resolution Method define un plan, pero no
  es suficiente para PASS.
- Las decisiones deferrable pueden permanecer abiertas (status: deferred) si
  tienen owner, justificacion, riesgo aceptado y condicion explicita de
  reactivacion.
- Las dependencias entre decisiones estan claras.
- No se disenara arquitectura sobre suposiciones criticas no verificadas.

## FAIL Criteria

- Hay decisiones blocking sin resolver (status: open sin evidencia de
  resolucion).
- Hay decisiones blocking con plan de resolucion pero sin ejecutar (owner y
  Resolution Method definidos, pero sin evidencia del resultado).
- Hay decisiones deferrable sin owner, sin justificacion, sin riesgo aceptado o
  sin condicion de reactivacion.
- Se intenta disenar arquitectura sobre suposiciones criticas no verificadas.
- Las dependencias entre decisiones no estan claras.

## Corrective Actions

- Ejecutar el plan de resolucion de decisiones blocking pendientes (owner: el
  asignado en cada decision).
- Ejecutar investigacion dirigida (owner: Engineering Architect o delegado).
- Ejecutar prototipo si hay incertidumbre tecnica (owner: especialista de
  dominio).
- Consultar al usuario para decisiones que requieren input externo.
- Crear ADR cuando se tome una decision relevante.
- Completar metadata de decisiones deferrable incompletas (owner,
  justificacion, riesgo, condicion de reactivacion).
- Owner de cada accion correctiva: el asignado en el campo Owner de cada
  decision.

## Evidence Required

- `DECISION_MAP.md` con todas las decisiones registradas.
- Para decisiones blocking resueltas: evidencia de la resolucion (ADR,
  resultado de prototipo, documento de investigacion, decision del usuario
  documentada).
- Para decisiones deferrable: owner, justificacion, riesgo aceptado y
  condicion de reactivacion documentados.
- Un plan de resolucion sin ejecutar no cuenta como evidencia para PASS.

## Handoff

- **PASS** -> arquitectura/planificacion. Todas las blocking estan resueltas
  con evidencia.
- **FAIL** -> ejecutar planes de resolucion de decisiones blocking, completar
  metadata de deferrable, o consultar especialista segun la causa de fallo.
