# Gate 2 -- Decision Readiness

## Name

Decision Readiness Gate

## Purpose

Determinar si las decisiones tecnicas bloqueantes estan resueltas o tienen un
mecanismo claro de resolucion. Evitar disenar arquitectura sobre suposiciones no
verificadas. Distinguir decisiones bloqueantes de deferibles y registrar
dependencias entre ellas.

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
4. Para decisiones blocking, verificar si tienen informacion suficiente o plan
   de resolucion.
5. Para decisiones deferrables, confirmar que pueden posponerse sin riesgo
   arquitectonico.
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
- Dependencias entre decisiones mapeadas.
- Recomendaciones de prototipo, investigacion o ADR cuando aplique.
- Decision: PASS o FAIL.

## PASS Criteria

- Las decisiones bloqueantes estan resueltas o tienen plan de resolucion con
  owner y metodo definidos.
- Se sabe que decisiones pueden diferirse y por que.
- Las dependencias entre decisiones estan claras.
- No se disenara arquitectura sobre suposiciones criticas no verificadas.

## FAIL Criteria

- Hay decisiones bloqueantes sin owner.
- Faltan datos necesarios para decisiones bloqueantes.
- Se intenta disenar arquitectura sobre suposiciones criticas no verificadas.
- Las dependencias entre decisiones no estan claras.

## Corrective Actions

- Ejecutar investigacion dirigida (owner: Engineering Architect o delegado).
- Ejecutar prototipo si hay incertidumbre tecnica (owner: especialista de
  dominio).
- Consultar al usuario para decisiones que requieren input externo.
- Crear ADR cuando se tome una decision relevante.
- Owner de cada accion correctiva: el asignado en el campo Owner de cada
  decision.

## Evidence Required

- `DECISION_MAP.md` con todas las decisiones registradas.
- Para decisiones resueltas: evidencia de la resolucion (ADR, resultado de
  prototipo, documento de investigacion, decision del usuario documentada).
- Para decisiones con plan de resolucion: owner, metodo y condicion de
  resolucion definidos.

## Handoff

- **PASS** -> arquitectura/planificacion.
- **FAIL** -> investigacion, prototipo, consulta o especialista segun la
  causa de fallo.
