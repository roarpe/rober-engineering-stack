# Module -- software-development

## Name

software-development

## Purpose

Seleccionar y componer agentes, skills y gates relevantes para proyectos de
software: aplicaciones, servicios, APIs, backend, integraciones, Python, C++,
C#, bases de datos, packaging, deployment y observabilidad.

## Activation Triggers

- Hay codigo backend, CLI, servicios, librerias o integraciones.
- Hay APIs, bases de datos o servicios que disenar.
- Hay packaging, despliegue u observabilidad que definir.
- Hay integracion software con otros subsistemas (PLC, robot, vision, datos).

## When Not To Activate

- El trabajo es solo documentacion industrial sin software.
- El proyecto es puramente PLC sin interfaces software.
- El cambio es documental menor sin codigo.
- Software solo aparece como contexto futuro no abordado.

## Primary Agents

- **Software Engineer**: diseno e implementacion de software, APIs, backend,
  bases de datos, packaging, despliegue, observabilidad.

## Optional Agents

- **Engineering Architect**: cuando hay multiples dominios o riesgo
  arquitectonico.
- **QA & Debug Engineer**: cuando hay implementacion que verificar o debug.
- **Technical Documentation Engineer**: cuando hay outputs duraderos.
- **Industrial Automation Engineer**: cuando hay interfaces PLC/OT.
- **Robotics Engineer**: cuando hay interfaces robot.

## Relevant Skills

Custom Industrial Skills (activar por trigger, no automaticamente):

- `industrial-python-engineering`: cuando hay Python en entorno industrial.
- `industrial-communications-design`: cuando hay comunicaciones industriales
  o contratos de integracion.
- `vision-ai-integration`: cuando hay integracion de vision o IA.
- `machine-diagnostics`: cuando hay diagnostico de maquina o sistema.
- `industrial-documentation`: cuando hay estrategia documental industrial.
- `industrial-project-verification`: cuando hay verificacion transversal.

Optional Library Skills (segun ARCHITECTURE.md 6.1):

- `writing-plans`, `systematic-debugging`, `test-driven-development`,
  `api-design`, `architecture-decision-records`, `code-review`.

## Gates Policy

- **Final Verification**: siempre proporcional, antes de claims.
- **Implementation Review**: cuando hay diff con riesgo o proyecto mediano.
- **Requirements Quality**: cuando hay ambiguedad o proyecto mediano/grande.
- **Decision Readiness**: condicionado a incertidumbre tecnica o multiples
  alternativas.
- Ningun gate se omite por riesgo en proyecto grande.

## Typical Inputs

- Requisitos de software.
- Arquitectura o plan del proyecto.
- Interfaces con PLC, robot, vision, datos.
- ADRs aplicables.
- Standards del repo o modulo.

## Typical Outputs

- Software architecture (modulos, capas, dependencias).
- API/data contracts.
- Codigo implementado.
- Plan de implementacion.
- Criterios de test de software.

## Cross-Domain Interfaces

- **PLC/OT**: tags, senales, comunicaciones industriales.
- **Robotica**: contratos de integracion robot-software.
- **Vision**: consumo de resultados de inspeccion, triggers.
- **Datos**: pipelines, persistencia, analytics.

## Risk Signals

- Integracion con subsistemas industriales no definida.
- Dependencias circulares entre modulos software.
- Falta de observabilidad en produccion.
- APIs sin contratos versionados.
- Mezcla de responsabilidades backend/frontend.

## Scaling Policy

- **Small**: Software Engineer solo, skills por trigger, FV proporcional, IR
  solo si diff con riesgo.
- **Medium**: Software Engineer + QA, RQ + IR + FV, interfaces definidas,
  ADRs necesarios.
- **Large/High-Risk**: EA coordina + SE + QA + TDE, los cuatro gates si
  aplica, trazabilidad, verificacion transversal.

## Composition Rules

- Cuando se compone con `industrial-automation`, las interfaces PLC-software
  requieren contrato explicito. `industrial-communications-design` se activa
  una sola vez.
- Cuando se compone con `robotics`, los contratos robot-software los define
  Robotics Engineer; Software Engineer implementa el lado software.
- Cuando se compone con `computer-vision`, `vision-ai-integration` se activa
  una sola vez.
- Cuando se compone con `data-engineering`, `industrial-python-engineering` se
  activa una sola vez si Python aplica.
- Las skills compartidas se activan una sola vez por necesidad.

## Handoff Expectations

- Handoff a QA & Debug Engineer para verificacion.
- Handoff a Technical Documentation Engineer para documentacion.
- Handoff a Engineering Architect para decisiones transversales.
- Todo handoff incluye artefacto, estado, evidencia, decisiones, riesgos,
  siguiente owner.

## Done Criteria

- Software architecture coherente con requisitos y ADRs.
- Codigo implementado segun plan.
- API/data contracts definidos.
- Gates aplicados segun proporcionalidad.
- Handoffs completados.
