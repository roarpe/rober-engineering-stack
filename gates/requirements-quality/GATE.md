# Gate 1 -- Requirements Quality

## Name

Requirements Quality Gate

## Purpose

Comprobar si existe informacion suficiente para pasar de idea/discovery a
decisiones y arquitectura. Validar que los requisitos tienen objetivo, alcance,
restricciones y criterios de aceptacion claros. Detectar ambiguedades,
vocabulario contradictorio y decisiones bloqueantes antes de invertir en
arquitectura o implementacion.

## Trigger

- Proyecto nuevo no trivial.
- Cambio con impacto en dominio, arquitectura, PLC/robot/vision/datos.
- Requisitos ambiguos o sin criterios de aceptacion.
- Transicion desde discovery a planificacion.

## When Not To Use

- Tarea pequena, local y claramente especificada.
- Correccion mecanica con test/bug reproducible.
- Cambio documental menor sin ambiguedad.
- El proyecto ya tiene requisitos validados y no han cambiado.

## Owner

Engineering Architect

## Participants

- Technical Documentation Engineer (valida vocabulario y glosario).
- Agente de dominio si aplica (Industrial Automation, Robotics, Software,
  Computer Vision, Data Engineering) segun tecnologia involucrada.

## Required Inputs

- Idea inicial o `PROJECT_DISCOVERY.md`.
- Contexto del repo/proyecto.
- Restricciones del usuario.
- Glosario, CONTEXT o ADRs existentes si existen.

## Procedure

1. Identificar el objetivo del proyecto o cambio en una frase verificable.
2. Delimitar el alcance: que esta dentro y que fuera.
3. Identificar usuarios y stakeholders cuando aplique.
4. Listar restricciones tecnicas, operativas y de plazos.
5. Verificar que existen criterios de aceptacion para cada objetivo.
6. Revisar vocabulario de dominio: detectar terminos ambiguos o
   contradictorios.
7. Detectar decisiones tecnicas abiertas que puedan bloquear arquitectura.
8. Clasificar cada decision como bloqueante o deferible.
9. Producir el artefacto de salida con la decision PASS o FAIL.

## Required Outputs

Artefacto: `REQUIREMENTS_GATE_REPORT.md`

Contenido obligatorio:

- Objetivo validado.
- Alcance delimitado.
- Usuarios/stakeholders identificados (si aplica).
- Restricciones listadas.
- Criterios de aceptacion por objetivo.
- Ambiguedades detectadas y resueltas.
- Ambiguedades restantes.
- Terminos de dominio candidatos para glosario.
- Decisiones abiertas detectadas (bloqueantes y deferibles).
- Decision: PASS o FAIL.

## PASS Criteria

- Objetivo, alcance, usuarios, restricciones y criterios de aceptacion estan
  claros.
- No hay vocabulario de dominio contradictorio sin resolver.
- Las decisiones bloqueantes estan resueltas o derivadas al Decision Readiness
  Gate. Cuando existen decisiones blocking derivadas, Requirements Quality
  puede completar su responsabilidad (PASS), pero el workflow NO puede avanzar
  a arquitectura/planificacion hasta que Decision Readiness Gate supere con
  PASS.
- Existe output documental suficiente para arquitectura o planificacion.

## FAIL Criteria

- Faltan criterios de aceptacion.
- El alcance mezcla subsistemas independientes sin separacion.
- Hay decisiones tecnicas bloqueantes sin informacion.
- El vocabulario de dominio es confuso o contradictorio.
- El objetivo no es verificable.

## Corrective Actions

- Ejecutar discovery adicional (ej. `industrial-project-discovery`).
- Dividir el proyecto en subsistemas separados.
- Pedir datos o aclaraciones al usuario.
- Crear lista de decisiones pendientes y derivar al Decision Readiness Gate.
- Owner de cada accion correctiva: Engineering Architect salvo delegacion
  explicita.

## Evidence Required

- Documento de requisitos con objetivo, alcance y criterios de aceptacion
  escritos.
- Lista de ambiguedades detectadas y su estado (resuelta/pendiente).
- Lista de decisiones abiertas con clasificacion bloqueante/deferible.
- Evidencia de validacion de vocabulario (glosario o terminos confirmados).

## Handoff

- **PASS sin decisiones blocking** -> arquitectura/planificacion.
- **PASS con decisiones blocking derivadas** -> Decision Readiness Gate. El
  workflow queda bloqueado hasta que DR supere con PASS.
- **FAIL** -> discovery adicional o consulta al usuario.
