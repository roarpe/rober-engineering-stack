# Gate 4 -- Final Verification

## Name

Final Verification Gate

## Purpose

Impedir claims de completitud sin evidencia fresca. Verificar que cada
requisito aplicable, criterio de aceptacion, test, finding critico y documento
requerido tiene evidencia obtenida o revalidada durante la ejecucion actual.
Reportar riesgos residuales antes de cerrar.

## Trigger

- Antes de cerrar tarea/proyecto.
- Antes de entregar artefactos finales.
- Antes de afirmar "terminado", "funciona", "tests pasan" o equivalente.

## When Not To Use

- Nunca se omite antes de declarar completitud.
- Para microtareas conversacionales sin artefacto, basta una verificacion
  proporcional (no requiere artefacto formal, pero si evidencia).

## Owner

QA & Debug Engineer

## Participants

- Engineering Architect (aprueba entrega).
- Technical Documentation Engineer (verifica documentos actualizados).
- Especialista de dominio si hay verificaciones industriales especificas.

## Required Inputs

- Requisitos y criterios de aceptacion.
- Plan y tasks.
- Resultados de tests/verificaciones.
- Review findings (salida de Implementation Review Gate).
- Documentacion requerida.
- Riesgos pendientes.

## Procedure

1. Listar todos los claims importantes del trabajo (que se afirma que esta
   hecho o funciona).
2. Para cada claim, registrar:
   - Claim (afirmacion de completitud).
   - Required Evidence (evidencia necesaria para respaldar el claim).
   - Evidence Source (de donde se obtiene: test, comando, inspeccion,
     simulacion, review result, comparacion contra criterio).
   - Timestamp/Execution Context (cuando se obtuvo, si aplica).
   - Result (resultado de la evidencia).
   - PASS/FAIL (estado del claim).
3. Comprobar requisitos aplicables cubiertos.
4. Comprobar criterios de aceptacion con evidencia.
5. Comprobar tests/checks ejecutados recientemente.
6. Comprobar findings criticos del Implementation Review resueltos.
7. Comprobar documentacion requerida actualizada.
8. Identificar y registrar riesgos residuales.
9. Producir el artefacto de salida con la decision final.

### Fresh Evidence

Fresh evidence significa: evidencia obtenida o revalidada durante la
ejecucion actual o despues del ultimo cambio relevante que pueda afectar al
resultado. La evidencia historica sin revalidacion no cuenta como fresh
evidence.

Tipos validos de evidencia:

- Tests ejecutados.
- Comandos ejecutados con resultado observable.
- Checks automatizados.
- Inspecciones manuales documentadas.
- Simulaciones.
- Review results.
- Comparacion contra criterios de aceptacion.

## Required Outputs

Artefacto: `FINAL_VERIFICATION_REPORT.md`

Contenido obligatorio:

- Tabla de claims con evidencia fresca por claim.
- Lista de criterios de aceptacion con estado PASS/FAIL.
- Resultados de tests/checks ejecutados.
- Estado de findings criticos del Implementation Review.
- Documentacion verificada.
- Riesgos residuales identificados.
- Decision final: PASS o FAIL.

## PASS Criteria

- Cada criterio de aceptacion tiene evidencia fresca.
- Tests/checks relevantes fueron ejecutados o revalidados recientemente.
- Reviews criticas estan resueltas.
- Documentacion minima esta actualizada.
- Riesgos residuales estan identificados y documentados.

## FAIL Criteria

- Hay claims sin evidencia.
- Tests no ejecutados o incompletos.
- Se confia unicamente en resultados historicos sin revalidar.
- Riesgos criticos pendientes sin documentar.
- Documentacion o criterios de aceptacion faltan.
- Se acepta "deberia funcionar" sin verificacion.

## Corrective Actions

- Ejecutar verificaciones faltantes (owner: QA & Debug Engineer).
- Corregir fallos detectados (owner: asignado por finding/claim).
- Documentar limitaciones o riesgos residuales (owner: Technical Documentation
  Engineer).
- Reabrir Implementation Review o debugging si procede (owner: QA & Debug
  Engineer).

## Evidence Required

- `FINAL_VERIFICATION_REPORT.md` con tabla de claims y evidencia.
- Resultados de tests/checks con timestamp o contexto de ejecucion.
- Evidencia de que findings criticos fueron resueltos.
- Documentacion de riesgos residuales.

## Handoff

- **PASS** -> entrega/cierre.
- **FAIL** -> implementacion, debugging, review o documentacion segun causa.
