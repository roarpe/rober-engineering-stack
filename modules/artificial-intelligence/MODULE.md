# Module -- artificial-intelligence

## Name

artificial-intelligence

## Purpose

Seleccionar y componer agentes, skills y gates relevantes para proyectos de IA
aplicada: inferencia, modelos, integracion industrial, deployment de modelos,
observabilidad, lifecycle y fallback.

## Activation Triggers

- Hay IA aplicada, inferencia o modelos que integrar.
- Hay deployment de modelos en entorno industrial.
- Hay observabilidad, lifecycle o fallback de IA que definir.
- Hay pipelines de IA, evals, prompts o razonamiento.

## When Not To Activate

- La IA no afecta diseno, validacion ni operacion.
- IA solo aparece como contexto futuro no abordado.
- El proyecto es puramente PLC o robotica sin componente de IA.
- El cambio es documental menor sin contenido de IA.

## Primary Agents

- **Software Engineer**: implementacion de IA, integracion, deployment,
  observabilidad, lifecycle.

## Optional Agents

- **Engineering Architect**: cuando la integracion es transversal o hay
  multiples dominios.
- **Robotics Engineer**: cuando hay IA robotica (picking, trayectorias
  adaptativas).
- **Industrial Automation Engineer**: cuando hay IA en PLC o control.
- **QA & Debug Engineer**: cuando hay implementacion que verificar, evals o
  validacion.
- **Technical Documentation Engineer**: cuando hay outputs duraderos.

## Relevant Skills

Custom Industrial Skills (activar por trigger, no automaticamente):

- `vision-ai-integration`: cuando hay integracion de IA en sistema industrial.
- `industrial-python-engineering`: cuando hay Python para IA en entorno
  industrial.
- `industrial-communications-design`: cuando hay comunicaciones con servicio
  de IA.
- `machine-diagnostics`: cuando hay diagnostico que involucra IA.
- `industrial-documentation`: cuando hay estrategia documental industrial.
- `industrial-project-verification`: cuando hay verificacion transversal.

Optional Library Skills (segun ARCHITECTURE.md 6.4):

- `agentic-engineering`, `agent-harness-construction`, `agent-eval`
  (experimental), `skill-stocktake`, `continuous-learning-v2` (solo
  experimental y aprobado).

## Gates Policy

- **Requirements Quality**: cuando hay ambiguedad o proyecto mediano/grande.
- **Decision Readiness**: cuando hay decisiones de modelo/arquitectura
  blocking.
- **Implementation Review**: cuando hay codigo/pipelines que revisar.
- **Final Verification**: siempre proporcional, antes de claims.
- Ningun gate se omite por riesgo en proyecto grande.

## Typical Inputs

- Requisitos de IA.
- Arquitectura o plan del proyecto.
- Modelos disponibles o por integrar.
- Interfaces con PLC, robot, vision, datos.
- ADRs aplicables.

## Typical Outputs

- AI integration design (trigger, resultado, confianza, fallback).
- Model deployment plan.
- Observabilidad y lifecycle de IA.
- Criterios de validacion y evals.

## Cross-Domain Interfaces

- **Software**: APIs, servicios, integracion.
- **Vision**: inferencia visual, modelos de vision.
- **PLC/OT**: triggers, resultados, degradado.
- **Datos**: datasets, telemetria de inferencia, historizacion.

## Risk Signals

- Model drift sin monitorizacion.
- Fallback no definido ante fallo de inferencia.
- Latencia de inferencia no acotada.
- IA sin trazabilidad de version ni evidencia.
- IA como caja negra sin validacion.

## Scaling Policy

- **Small**: SE solo, skills por trigger, FV proporcional.
- **Medium**: SE + QA, RQ + IR + FV, evals definidos, ADRs necesarios.
- **Large/High-Risk**: EA coordina + SE + RE + IAE + QA + TDE, los cuatro
  gates, trazabilidad, verificacion transversal.

## Composition Rules

- Cuando se compone con `computer-vision`, `vision-ai-integration` se activa
  una sola vez. El modulo no se convierte en guia de machine learning.
- Cuando se compone con `software-development`, `industrial-python-engineering`
  se activa una sola vez si Python aplica.
- Cuando se compone con `industrial-automation`, los triggers y resultados de
  IA requieren contrato explicito con PLC.
- Las skills compartidas se activan una sola vez por necesidad.

## Handoff Expectations

- Handoff a QA & Debug Engineer para validacion y evals.
- Handoff a Technical Documentation Engineer para documentacion.
- Handoff a Engineering Architect para decisiones transversales.
- Todo handoff incluye artefacto, estado, evidencia, decisiones, riesgos,
  siguiente owner.

## Done Criteria

- AI integration design coherente con requisitos y ADRs.
- Model deployment plan definido.
- Observabilidad y lifecycle especificados.
- Fallback y degradado definidos.
- Gates aplicados segun proporcionalidad.
- Handoffs completados.
