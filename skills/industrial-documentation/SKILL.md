# Skill -- industrial-documentation

## Name

industrial-documentation

## Purpose

Disenar y mantener una estrategia documental industrial que permita a los
distintos consumidores encontrar, comprender, utilizar y mantener la
informacion tecnica necesaria durante el ciclo de vida del sistema. La
documentacion es parte del sistema de ingenieria, no un subproducto. No es
una skill para escribir documentos; es una skill para disenar que
documentacion necesita el proyecto, quien la consume, quien la mantiene, cual
es la fuente de verdad y como se mantiene trazable con el sistema real.

## Activation Triggers

- Proyecto industrial mediano o grande con multiples disciplinas.
- Participan PLC, robot, software, vision, IA o comunicaciones.
- Existe transferencia a operacion, mantenimiento u otro equipo de ingenieria.
- Existen requisitos de trazabilidad.
- Existen ADRs, procedimientos operativos, procedimientos de mantenimiento o
  troubleshooting.
- Existe riesgo de documentacion obsoleta.
- El proyecto tiene vida util suficientemente larga para requerir
  mantenimiento documental.

## When Not To Use

- La tarea documental es trivial o es una correccion menor.
- El proyecto es un prototipo desechable sin requisitos documentales.
- Ya existe una estrategia documental valida y el sistema no ha cambiado.
- No hay outputs duraderos que documentar.

## Primary Owner

Technical Documentation Engineer

## Participants

- Engineering Architect (coherencia transversal, ADRs).
- Industrial Automation Engineer (correccion tecnica de documentacion PLC).
- Robotics Engineer (correccion tecnica de documentacion robotica).
- Software Engineer (correccion tecnica de documentacion de software).
- QA & Debug Engineer (verificacion de documentacion).
- Usuario (requisitos de audiencia y accesibilidad).

## Required Inputs

- Requisitos validados (salida de Requirements Quality Gate).
- Decision map resuelto (salida de Decision Readiness Gate, si aplica).
- Arquitecturas de dominio existentes (PLC, robot, software, comunicaciones,
  vision/IA).
- ADRs existentes.
- Glosarios y terminos de dominio existentes.
- Procedimientos operativos y de mantenimiento conocidos.
- Restricciones de audiencia y accesibilidad.

## Procedure

1. Confirmar precondiciones: RQ PASS y DR PASS (si aplica).
2. Definir objetivos de documentacion: que necesita el proyecto, por que.
3. Identificar audiencias: desarrolladores, ingenieros, operadores,
   mantenimiento, arquitectura, usuarios.
4. Clasificar tipos documentales cuando aplique:
   - Architecture Documentation: estructura, decisiones, componentes,
     responsabilidades, interfaces, dependencias, ADRs.
   - Developer/Engineering Documentation: desarrollo, configuracion, testing,
     simulacion, integracion, despliegue, herramientas.
   - Operator Documentation: operacion normal, modos, comandos, estados,
     alarmas, recuperacion permitida, limitaciones.
   - Maintenance Documentation: diagnostico, troubleshooting, inspeccion,
     sustitucion, recuperacion, escalado.
5. Definir information architecture: como se organiza, donde se encuentra,
   como se navega.
6. Para cada artefacto documental relevante, definir Documentation Contract:
   - Document/Artifact.
   - Purpose.
   - Audience.
   - Owner.
   - Contributors.
   - Reviewer cuando aplique.
   - Source of Truth.
   - Inputs.
   - Update Triggers.
   - Verification Method.
   - Consumer/Handoff Target.
   - Lifecycle Status (planned, draft, active, needs-review, deprecated,
     archived).
7. Definir Source of Truth Policy: para cada informacion relevante, cual es
   la fuente autoritativa, cuales son derivadas, como se sincronizan, quien
   responde de la coherencia.
8. Definir terminology y glossary strategy.
9. Definir estrategia de diagramas, interfaces y troubleshooting.
10. Definir operational knowledge, maintenance knowledge, architecture
    knowledge y developer knowledge necesarios.
11. Definir evidence references: como se vincula la documentacion con
    evidencia tecnica (ADRs, tests, inspecciones).
12. Definir Documentation Freshness: que cambios del sistema disparan
    revision documental (cambio arquitectonico, ADR aceptado, cambio de
    interfaz, cambio de secuencia, cambio de modo operativo, cambio de
    alarmas, cambio de recuperacion, cambio de despliegue, cambio de
    configuracion, cambio de procedimiento).
13. Definir review cadence cuando aplique.
14. Definir lifecycle: obsolescence, archival y transicion entre estados.
15. Definir accesibilidad: quien puede acceder, como, restricciones.
16. Definir riesgos de la estrategia documental.
17. Registrar decisiones abiertas.
18. Producir el artefacto de salida.

### Source of Truth Policy

La skill debe impedir documentacion duplicada sin ownership claro. Para
informacion relevante debe existir una fuente de verdad identificable. Cuando
varias representaciones sean necesarias:

- Definir cual es autoritativa.
- Definir cuales son derivadas.
- Definir como se sincronizan.
- Definir quien responde de la coherencia.

### Documentation Freshness

No debe asumir que documentacion existente significa documentacion valida.
Debe definir que cambios del sistema disparan revision documental.

### Division de responsabilidad

- El especialista tecnico responde de la correccion tecnica del contenido de
  su dominio.
- Technical Documentation Engineer responde de estructura, claridad,
  coherencia, mantenibilidad y lifecycle documental.

## Required Outputs

Artefacto: `INDUSTRIAL_DOCUMENTATION.md`

Contenido obligatorio:

- Documentation objectives.
- Audiences.
- Documentation map (artefactos identificados).
- Classification (Architecture, Developer/Engineering, Operator,
  Maintenance cuando aplique).
- Artifact contracts (12 campos por artefacto).
- Ownership (owner, contributors, reviewer).
- Sources of truth (autoritativa, derivadas, sincronizacion).
- Traceability (vinculo con sistema real y evidencia).
- Terminology/glossary strategy.
- Update triggers.
- Verification methods.
- Lifecycle (estados, obsolescence, archival).
- Accessibility.
- Riesgos.
- Decisiones abiertas.

## Consumer

Engineering Architect (coherencia transversal), Technical Documentation
Engineer (mantenimiento), especialistas de dominio (correccion tecnica), QA &
Debug Engineer (verificacion de documentacion).

## Stop Condition

La skill se detiene cuando existe una estrategia documental suficiente para
que cada artefacto necesario tenga proposito, audiencia, owner, fuente de
verdad, trigger de actualizacion, metodo de verificacion y consumidor. No
debe continuar hasta escribir todos los documentos del proyecto.

## Gates Interaction

- **Precondicion**: Requirements Quality PASS. Decision Readiness PASS (si
  aplica).
- **Participa en**: Implementation Review (valida docs/ADRs afectados), Final
  Verification (verifica documentos actualizados).
- **No ejecuta**: la decision PASS/FAIL de ningun gate. Final Verification
  Gate conserva autoridad exclusiva.
- **No reemplaza**: ADRs. Los ADRs son decisiones aprobadas; la skill los
  documenta y mantiene, no los crea unilateralmente.

## Agent Interaction

- **Activada por**: Technical Documentation Engineer (owner).
- **Coordina con**: especialistas de dominio para correccion tecnica,
  Engineering Architect para ADRs y coherencia transversal.
- **Handoff a**: QA & Debug Engineer para verificacion de documentacion;
  especialistas para revision tecnica.

## Evidence Required

- `INDUSTRIAL_DOCUMENTATION.md` con todos los campos obligatorios.
- Documentation Contract completo por artefacto relevante.
- Source of Truth identificada por informacion relevante.
- Update triggers definidos.
- No documentacion sin owner ni consumer.

## Failure Modes

- Convertirse en una skill de escritura sin estrategia.
- Inventar comportamiento no verificado.
- Documentar supuestos como hechos.
- Sustituir al especialista tecnico en correccion de contenido.
- Tomar decisiones arquitectonicas unilateralmente.
- Duplicar documentacion sin ownership claro.
- Crear documentacion sin consumidor.
- Crear documentacion sin owner.
- Asumir que mas documentacion significa mejor documentacion.
- No definir freshness ni update triggers.
- No definir source of truth.
- Aprobar su propia precision tecnica cuando requiere especialista.
- Ejecutar Final Verification.

## Escalation Rules

- Correccion tecnica de contenido -> especialista de dominio correspondiente.
- Decision arquitectonica no aprobada -> Engineering Architect.
- Conflicto entre documentacion y codigo -> QA & Debug Engineer.
- Conflicto de source of truth entre dominios -> Engineering Architect.
- Falta de informacion para documentar -> escalar al owner del artefacto
  tecnico.
- Decision de estrategia documental dificil de revertir -> proponer ADR.

## Done Criteria

- `INDUSTRIAL_DOCUMENTATION.md` completo con todos los campos obligatorios.
- Cada artefacto documental relevante tiene owner, consumer y source of
  truth.
- Classification distingue Architecture, Developer/Engineering, Operator y
  Maintenance cuando aplique.
- Update triggers definidos.
- No documentacion sin owner ni consumer.
- No documentacion duplicada sin source of truth claro.
- Especialistas responsables de correccion tecnica identificados.
- Artefacto entregado a Technical Documentation Engineer para mantenimiento.
