# Module -- robotics

## Name

robotics

## Purpose

Seleccionar y componer agentes, skills y gates relevantes para proyectos de
robotica industrial: robots industriales, ROS 2, integracion robot-PLC, celulas
robotizadas, tooling, frames, trayectorias y recuperacion de errores.

## Activation Triggers

- Hay robot industrial, ROS 2 o celula robotizada.
- Hay integracion robot-PLC, vision-robot o herramientas roboticas.
- Hay trayectorias, frames o cinematica que definir.
- Hay recuperacion de errores roboticos que disenar.

## When Not To Activate

- El robot no forma parte del sistema o solo se menciona como contexto no
  operativo.
- El trabajo es puramente PLC sin interfaz robot.
- El cambio es software backend sin integracion robotica.
- Robotica solo aparece como requisito futuro no abordado en la fase.

## Primary Agents

- **Robotics Engineer**: robot cell architecture, trayectorias, frames,
  integracion robot-PLC, recuperacion de errores.

## Optional Agents

- **Engineering Architect**: cuando hay multiples dominios o riesgo
  arquitectonico.
- **Industrial Automation Engineer**: cuando hay PLC interno o comunicaciones
  OT.
- **Software Engineer**: cuando hay software backend o integracion.
- **QA & Debug Engineer**: cuando hay implementacion que verificar o test
  roboticos.
- **Technical Documentation Engineer**: cuando hay outputs duraderos.

## Relevant Skills

Custom Industrial Skills (activar por trigger, no automaticamente):

- `robotics-cell-integration`: cuando hay celula robotizada que integrar.
- `industrial-communications-design`: cuando hay comunicaciones robot-PLC o
  robot-software.
- `vision-ai-integration`: cuando hay vision-robot o IA en la celula.
- `machine-diagnostics`: cuando hay diagnostico de robot o celula.
- `industrial-documentation`: cuando hay estrategia documental industrial.
- `industrial-project-verification`: cuando hay verificacion transversal.

Optional Library Skills (segun ARCHITECTURE.md 6.3):

- `prototype` para incertidumbre de estado/flujo. ADRs para decisiones de
  integracion.

## Gates Policy

- **Requirements Quality**: cuando hay ambiguedad o proyecto mediano/grande.
- **Decision Readiness**: cuando hay decisiones de robot/integracion blocking.
- **Implementation Review**: cuando hay codigo robotico/interfaces que revisar.
- **Final Verification**: siempre proporcional, antes de claims.
- Ningun gate se omite por riesgo en proyecto grande.

## Typical Inputs

- Requisitos de robotica.
- Arquitectura o plan del proyecto.
- Especificaciones de robot y herramientas.
- Interfaces con PLC, software y vision.
- ADRs aplicables.

## Typical Outputs

- Robot cell architecture (estado, senales, recuperacion).
- Trayectorias y frames definidos.
- Contratos de integracion robot-PLC.
- Especificaciones de herramientas y perifericos.
- Criterios de test roboticos.

## Cross-Domain Interfaces

- **PLC/OT**: contratos robot-PLC, secuencias, handshake, senales.
- **Software**: estado robotico, APIs, integracion.
- **Vision**: calibracion, picking, resultados de inspeccion.
- **Datos**: telemetria robotica, historizacion.

## Risk Signals

- Seguridad robotica sin especialista certificado.
- Integracion robot-PLC sin contrato explicito.
- Recuperacion de errores no definida.
- Trayectorias sin validacion de singulares ni limites.
- Vision-robot sin calibracion trazable.

## Scaling Policy

- **Small**: RE solo, skills por trigger, FV proporcional.
- **Medium**: RE + IAE + QA, RQ + IR + FV, interfaces definidas, simulacion
  robotica.
- **Large/High-Risk**: EA coordina + RE + IAE + SE + QA + TDE, los cuatro
  gates, trazabilidad, verificacion transversal.

## Composition Rules

- Cuando se compone con `industrial-automation`, `robotics-cell-integration`
  define la integracion; `industrial-communications-design` se activa una
  sola vez.
- Cuando se compone con `computer-vision`, `vision-ai-integration` se activa
  una sola vez. RE integra vision desde perspectiva robotica.
- Cuando se compone con `software-development`, los contratos robot-software
  los define RE; SE implementa el lado software.
- Las skills compartidas se activan una sola vez por necesidad.

## Handoff Expectations

- Handoff a Industrial Automation Engineer para integracion PLC.
- Handoff a Software Engineer para interfaces software.
- Handoff a QA & Debug Engineer para test roboticos.
- Handoff a Technical Documentation Engineer para documentacion.
- Todo handoff incluye artefacto, estado, evidencia, decisiones, riesgos,
  siguiente owner.

## Done Criteria

- Robot cell architecture completa con estado, senales y recuperacion.
- Trayectorias y frames definidos.
- Contratos de integracion robot-PLC documentados.
- Criterios de test especificados.
- Gates aplicados segun proporcionalidad.
- Handoffs completados.
