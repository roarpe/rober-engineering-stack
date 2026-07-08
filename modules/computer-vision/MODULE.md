# Module -- computer-vision

## Name

computer-vision

## Purpose

Seleccionar y componer agentes, skills y gates relevantes para proyectos de
vision por computador industrial: adquisicion de imagen, procesamiento,
inspeccion, localizacion, metrologia, vision robotizada e inferencia visual.

Este modulo puede operar de forma independiente aunque incluya un modelo de
inferencia visual. `artificial-intelligence` se activa conjuntamente solo cuando
hay responsabilidades de IA independientes o significativas (model lifecycle,
deployment, evals, observabilidad especifica, MLOps, gobernanza, integracion IA
transversal).

## Activation Triggers

- Hay camaras, adquisicion de imagen o procesamiento de imagen.
- Hay inspeccion, clasificacion o localizacion por vision.
- Hay calibracion, iluminacion o dataset de vision.
- Hay vision robotizada (picking, guidance, metrologia).
- Hay inferencia visual en sistema industrial.

## When Not To Activate

- Vision solo aparece como requisito futuro no abordado en la fase.
- El proyecto no involucra camaras ni procesamiento de imagen.
- El cambio es puramente PLC o software sin componente de vision.
- La vision ya esta integrada y validada sin cambios.

## Primary Agents

- **Software Engineer**: cuando el consumidor principal es software (dashboard,
  API, pipeline).
- **Robotics Engineer**: cuando el consumidor principal es robotica (picking,
  guidance, metrologia robotizada).
- Engineering Architect resuelve ownership transversal cuando ambos consumen.

## Optional Agents

- **Engineering Architect**: cuando hay multiples dominios o ambiguity de
  ownership.
- **Industrial Automation Engineer**: cuando hay triggers desde PLC o
  integracion OT.
- **QA & Debug Engineer**: cuando hay implementacion que verificar o validacion
  de inspeccion.
- **Technical Documentation Engineer**: cuando hay outputs duraderos.

## Relevant Skills

Custom Industrial Skills (activar por trigger, no automaticamente):

- `vision-ai-integration`: cuando hay integracion de vision o IA visual en
  sistema industrial.
- `robotics-cell-integration`: cuando hay vision robotizada en celula.
- `industrial-python-engineering`: cuando hay Python para procesamiento de
  vision.
- `industrial-communications-design`: cuando hay comunicaciones con servicio
  de vision.
- `machine-diagnostics`: cuando hay diagnostico que involucra vision.
- `industrial-project-verification`: cuando hay verificacion transversal.

Optional Library Skills (segun ARCHITECTURE.md 6.5):

- `prototype` si se necesita validar pipeline o UI. `systematic-debugging`
  para fallos de integracion.

## Gates Policy

- **Requirements Quality**: cuando hay ambiguedad o proyecto mediano/grande.
- **Decision Readiness**: cuando hay decisiones de arquitectura de vision
  blocking.
- **Implementation Review**: cuando hay codigo/pipelines de vision que revisar.
- **Final Verification**: siempre proporcional, antes de claims.
- Ningun gate se omite por riesgo en proyecto grande.

## Typical Inputs

- Requisitos de inspeccion, metrologia o vision robotizada.
- Arquitectura o plan del proyecto.
- Especificaciones de camaras, iluminacion y hardware.
- Interfaces con PLC, robot, software, IA.
- ADRs aplicables.

## Typical Outputs

- Vision system design (adquisicion, procesamiento, resultado).
- Calibration plan.
- Inspection criteria y tolerancias.
- Integration contracts con consumidores (robot, PLC, software).

## Cross-Domain Interfaces

- **Robotica**: calibracion robot-camara, picking, guidance.
- **PLC/OT**: triggers de inspeccion, resultados, handshake.
- **Software**: APIs, dashboards, pipelines.
- **IA**: modelos de inferencia visual, fallback.

## Risk Signals

- Calibracion sin trazabilidad ni periodicidad.
- Iluminacion no controlada ni documentada.
- Falsos positivos/negativos sin umbral definido.
- Latencia de inspeccion no acotada para ciclo de maquina.
- Dataset sin versionado ni evidencia de cobertura.

## Scaling Policy

- **Small**: SE o RE solo, skills por trigger, FV proporcional.
- **Medium**: SE/RE + QA, RQ + IR + FV, interfaces definidas, calibration
  plan.
- **Large/High-Risk**: EA coordina + SE + RE + IAE + QA + TDE, los cuatro
  gates, trazabilidad, verificacion transversal.

## Composition Rules

- Cuando se compone con `robotics`, `vision-ai-integration` y
  `robotics-cell-integration` se activan por trigger, no duplicadamente.
- Cuando se compone con `artificial-intelligence`, `vision-ai-integration` se
  activa una sola vez. `computer-vision` puede operar solo con inferencia
  visual; `artificial-intelligence` es complementario cuando hay responsabilidades
  de IA independientes.
- Cuando se compone con `industrial-automation`, los triggers de inspeccion y
  handshake los define el lado de automatizacion.
- Cuando se compone con `software-development`,
  `industrial-python-engineering` se activa una sola vez si Python aplica.
- Las skills compartidas se activan una sola vez por necesidad.

## Handoff Expectations

- Handoff a Robotics Engineer para integracion robot-vision.
- Handoff a Industrial Automation Engineer para triggers PLC.
- Handoff a Software Engineer para pipelines y APIs.
- Handoff a QA & Debug Engineer para validacion de inspeccion.
- Handoff a Technical Documentation Engineer para documentacion.
- Todo handoff incluye artefacto, estado, evidencia, decisiones, riesgos,
  siguiente owner.

## Done Criteria

- Vision system design coherente con requisitos.
- Calibration plan definido y trazable.
- Inspection criteria y tolerancias especificados.
- Integration contracts con consumidores definidos.
- Gates aplicados segun proporcionalidad.
- Handoffs completados.
