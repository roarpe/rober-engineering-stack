# Module -- data-engineering

## Name

data-engineering

## Purpose

Seleccionar y componer agentes, skills y gates relevantes para proyectos de
datos: adquisicion, almacenamiento, transformacion, historizacion, pipelines,
calidad, trazabilidad y analytics.

## Activation Triggers

- Hay adquisicion, procesamiento o almacenamiento de datos.
- Hay historizacion, ETL o telemetria.
- Hay pipelines de datos o analytics.
- Hay calidad, trazabilidad o gobernanza de datos que definir.

## When Not To Activate

- Los datos no salen del equipo/local o no hay persistencia/analisis.
- Data solo aparece como contexto futuro no abordado.
- El cambio es puramente PLC sin componente de datos.
- El proyecto es documental menor sin contenido de datos.

## Primary Agents

- **Software Engineer**: arquitectura de datos, pipelines, persistencia,
  transformacion, analytics.

## Optional Agents

- **Engineering Architect**: cuando hay multiples dominios o riesgo
  arquitectonico.
- **Industrial Automation Engineer**: cuando hay adquisicion desde PLC/OT.
- **QA & Debug Engineer**: cuando hay implementacion que verificar o calidad
  de datos.
- **Technical Documentation Engineer**: cuando hay outputs duraderos.

## Relevant Skills

Custom Industrial Skills (activar por trigger, no automaticamente):

- `industrial-python-engineering`: cuando hay Python para pipelines o
  transformacion.
- `industrial-communications-design`: cuando hay adquisicion via comunicaciones
  industriales.
- `machine-diagnostics`: cuando hay diagnostico que involucra datos.
- `industrial-documentation`: cuando hay estrategia documental industrial.
- `industrial-project-verification`: cuando hay verificacion transversal.

Optional Library Skills (segun ARCHITECTURE.md 6.6):

- `api-design` si hay contratos de datos/API. `writing-plans`. ADRs.

## Gates Policy

- **Requirements Quality**: cuando hay ambiguedad o proyecto mediano/grande.
- **Decision Readiness**: condicionado a decisiones de arquitectura de datos.
- **Implementation Review**: cuando hay codigo/pipelines que revisar.
- **Final Verification**: siempre proporcional, antes de claims.
- Ningun gate se omite por riesgo en proyecto grande.

## Typical Inputs

- Requisitos de datos (fuentes, formato, frecuencia, calidad).
- Arquitectura o plan del proyecto.
- Interfaces con PLC, software, web.
- ADRs aplicables.

## Typical Outputs

- Data architecture (fuentes, almacenamiento, transformacion).
- Pipeline design.
- Data contracts y esquemas.
- Criterios de calidad y trazabilidad.

## Cross-Domain Interfaces

- **PLC/OT**: adquisicion de telemetria, alarmas, senales.
- **Software**: APIs, servicios, integracion.
- **Web**: dashboards, visualizacion, APIs web.
- **IA**: datasets, features, inferencia.

## Risk Signals

- Datos sin esquema ni contrato versionado.
- Pipeline sin manejo de fallos ni reintentos.
- Calidad de datos sin validacion ni metricas.
- Persistencia sin estrategia de retencion ni limpieza.
- Scalabilidad no evaluada para volumen esperado.

## Scaling Policy

- **Small**: SE solo, skills por trigger, FV proporcional.
- **Medium**: SE + QA, RQ + IR + FV, interfaces definidas, ADRs necesarios.
- **Large/High-Risk**: EA coordina + SE + IAE + QA + TDE, los cuatro gates,
  trazabilidad, verificacion transversal.

## Composition Rules

- Cuando se compone con `industrial-automation`, `industrial-communications-
  design` se activa una sola vez para adquisicion OT.
- Cuando se compone con `software-development`,
  `industrial-python-engineering` se activa una sola vez si Python aplica.
- Cuando se compone con `web-development`, los contratos de datos los define
  SE; el modulo web consume.
- Las skills compartidas se activan una sola vez por necesidad.

## Handoff Expectations

- Handoff a QA & Debug Engineer para verificacion de calidad.
- Handoff a Technical Documentation Engineer para documentacion.
- Handoff a Engineering Architect para decisiones transversales.
- Todo handoff incluye artefacto, estado, evidencia, decisiones, riesgos,
  siguiente owner.

## Done Criteria

- Data architecture coherente con requisitos.
- Pipeline design definido con manejo de fallos.
- Data contracts y esquemas versionados.
- Criterios de calidad y trazabilidad especificados.
- Gates aplicados segun proporcionalidad.
- Handoffs completados.
