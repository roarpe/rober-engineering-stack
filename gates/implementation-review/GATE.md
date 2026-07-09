# Gate 3 -- Implementation Review

## Name

Implementation Review Gate

## Purpose

Revisar la implementacion en dos ejes separados: SPEC (requisitos, criterios de
aceptacion, alcance, comportamiento esperado) y STANDARDS (arquitectura, ADRs,
convenciones, mantenibilidad, testabilidad, documentacion aplicable). Clasificar
findings por severidad. Impedir que desviaciones arquitectonicas importantes
pasen sin ADR.

## Trigger

- Fin de una tarea mediana/grande.
- Antes de merge/PR.
- Antes de declarar completa una implementacion.
- Tras cambios en PLC/robot/API/comunicaciones con riesgo operativo.

## When Not To Use

- No hay implementacion/diff que revisar.
- Cambio trivial ya cubierto por verificacion automatica y bajo riesgo.
- La fase actual solo esta creando arquitectura, no codigo.
- Final Verification ya cubre la verificacion proporcional de una microtarea.

## Owner

QA & Debug Engineer

## Participants

- Engineering Architect (decide trade-offs y aprueba desviaciones con ADR).
- Technical Documentation Engineer (valida docs/ADRs afectados).
- Especialista de dominio si el diff toca PLC, robotica, vision o
  comunicaciones industriales.

## Required Inputs

- Diff o cambios producidos.
- Spec/PRD/plan/requisitos aplicables.
- Standards del repo o modulo.
- ADRs aplicables.
- Resultados de tests existentes.

## Procedure

1. Identificar el alcance del diff y los requisitos aplicables.
2. Eje SPEC -- Verificar:
   - Los requisitos estan implementados.
   - Los criterios de aceptacion se cumplen.
   - El alcance no excede lo especificado (scope creep).
   - El comportamiento esperado es correcto.
3. Eje STANDARDS -- Verificar:
   - La arquitectura sigue ADRs aplicables.
   - Las convenciones del repo/modulo se respetan.
   - La mantenibilidad y testabilidad son adecuadas.
   - La documentacion afectada esta actualizada.
4. Verificar evidencia de error paths: identificar desde los contratos
   fuente (requirements, specs, disenos aprobados) los comportamientos de
   fallo, recuperacion, manejo de excepciones y salidas de error
   contractualmente relevantes. Comprobar si existe evidencia de tests
   proporcional para cada uno. Distinguir:
   - Paths criticos: comportamientos de fallo exigidos contractualmente
     cuyo incumplimiento puede afectar criterios de aceptacion, integridad
     de datos, recuperacion, integracion, diagnosticabilidad o
     comportamiento externamente visible. La ausencia de evidencia
     suficiente puede impedir PASS segun severidad.
   - Paths defensivos/inalcanzables: branches no alcanzables mediante uso
     contractual normal. Pueden justificarse sin test directo cuando el
     test exigiria manipulacion artificial de internals, no representa
     comportamiento contractual, y existe evidencia de no-regresion
     proporcional.
   Clasificar gaps de evidencia segun impacto. Justificar explicitamente
   cualquier path relevante sin test directo.
5. Para cada hallazgo, registrar:
   - Finding ID.
   - Severity: CRITICAL, MAJOR, MINOR u OBSERVATION.
   - Axis: SPEC o STANDARDS.
   - Evidence (referencia al codigo o documento).
   - Impact (consecuencia si no se corrige).
   - Required Action (accion concreta para resolver).
   - Owner (responsable de la correccion).
   - Status (open/resolved/waived).
6. Verificar que no hay desviaciones arquitectonicas importantes sin ADR.
7. Producir el artefacto de salida con la decision PASS o FAIL.

## Required Outputs

Artefacto: `IMPLEMENTATION_REVIEW.md`

Contenido obligatorio:

- Findings clasificados por severidad y eje.
- Eje SPEC: requisitos faltantes, scope creep, comportamiento incorrecto.
- Eje STANDARDS: incumplimientos de convenciones, diseno, mantenibilidad.
- Desviaciones arquitectonicas detectadas y estado de ADR.
- Evidencia de error paths: paths criticos con evidencia, paths defensivos
  justificados, gaps clasificados.
- Decision: PASS o FAIL.

## PASS Criteria

- No hay findings CRITICAL ni MAJOR sin resolver.
- El diff implementa los requisitos aplicables.
- Los standards relevantes se cumplen o hay justificacion documentada.
- Las desviaciones arquitectonicas tienen ADR o estan justificadas.
- Los error paths contractualmente relevantes tienen evidencia de tests
  proporcional o justificacion documentada.

## FAIL Criteria

- Falta algun requisito importante.
- Hay desviacion de arquitectura sin ADR.
- Hay problemas criticos de seguridad, integracion, testabilidad o
  mantenibilidad.
- Un error path critico contractualmente requerido carece de evidencia
  de test y no tiene justificacion documentada.
- No hay spec verificable para comparar.

## Corrective Actions

- Corregir findings CRITICAL y MAJOR (owner: asignado por finding).
- Actualizar spec si el requisito cambio (owner: Engineering Architect).
- Crear ADR si se acepta una desviacion (owner: Engineering Architect).
- Repetir review tras correcciones (owner: QA & Debug Engineer).

## Evidence Required

- `IMPLEMENTATION_REVIEW.md` con todos los findings registrados.
- Referencias concretas al codigo o documento para cada finding.
- ADRs creados para desviaciones aceptadas.
- Evidencia de que los findings CRITICAL y MAJOR fueron resueltos antes del
  PASS.
- Evidencia de verificacion de error paths (paths identificados, evidencia
  de tests o justificacion de ausencia).

## Handoff

- **PASS** -> Final Verification.
- **FAIL** -> correccion y repeticion del gate.
