# Module -- industrial-automation

## Name

industrial-automation

## Purpose

Seleccionar y componer agentes, skills y gates relevantes para proyectos de
automatizacion industrial: PLC, IEC 61131-3, maquinas de estados, secuencias,
modos, alarmas, senales, I/O y comunicaciones industriales OT.

## Activation Triggers

- Hay PLC, IEC 61131-3, Structured Text, Ladder o Function Blocks.
- Hay maquinas de estados, secuencias, modos, alarmas o diagnostico.
- Hay comunicaciones industriales desde la perspectiva de automatizacion.
- Hay HMI, I/O o senales que disenar.

## When Not To Activate

- El proyecto no toca automatizacion, control o integracion industrial.
- PLC/automatizacion solo aparece como contexto futuro no abordado.
- El cambio es puramente software sin interfaces industriales.
- El trabajo es solo documentacion sin contenido tecnico de automatizacion.

## Primary Agents

- **Industrial Automation Engineer**: arquitectura PLC, secuencias, modos,
  alarmas, I/O, diagnostico, comunicaciones industriales OT.

## Optional Agents

- **Engineering Architect**: cuando hay multiples dominios o riesgo
  arquitectonico.
- **Robotics Engineer**: cuando hay integracion robot-PLC.
- **Software Engineer**: cuando hay interfaces software o backend.
- **QA & Debug Engineer**: cuando hay implementacion que verificar o simular.
- **Technical Documentation Engineer**: cuando hay outputs duraderos.

## Relevant Skills

Custom Industrial Skills (activar por trigger, no automaticamente):

- `industrial-project-discovery`: cuando hay idea inicial industrial que
  estructurar.
- `plc-software-architecture`: cuando hay arquitectura PLC que disenar.
- `industrial-communications-design`: cuando hay comunicaciones industriales
  que disenar.
- `machine-diagnostics`: cuando hay diagnostico de maquina o sistema.
- `industrial-documentation`: cuando hay estrategia documental industrial.
- `industrial-project-verification`: cuando hay verificacion transversal.

Optional Library Skills (segun ARCHITECTURE.md 6.2):

- `systematic-debugging` para fallos. ADRs para decisiones de arquitectura.

## Gates Policy

- **Requirements Quality**: cuando hay ambiguedad o proyecto mediano/grande.
- **Decision Readiness**: cuando hay decisiones de PLC/comunicaciones
  blocking.
- **Implementation Review**: cuando hay codigo PLC/interfaces que revisar.
- **Final Verification**: siempre proporcional, antes de claims.
- Ningun gate se omite por riesgo en proyecto grande.

## Typical Inputs

- Requisitos de automatizacion.
- Arquitectura o plan del proyecto.
- Especificaciones de hardware y senales.
- ADRs aplicables.
- Interfaces con otros subsistemas (robot, software, vision).

## Typical Outputs

- PLC architecture (FBs, estados, modos, alarmas).
- Secuencias y logica de control.
- Interfaces industriales (senales, tags, comunicaciones).
- Criterios de simulacion y test.

## Cross-Domain Interfaces

- **Robotica**: contratos robot-PLC, secuencias, handshake, senales.
- **Software**: tags, APIs, comunicaciones OT-IT.
- **Vision**: triggers de inspeccion, resultados, handshake.
- **Datos**: telemetria, historizacion, alarmas.

## Risk Signals

- Seguridad funcional no certificada o sin especialista.
- Comunicaciones industriales sin watchdog ni recuperacion.
- Estados de error no definidos o sin recuperacion.
- Interfaz robot-PLC sin contrato explicito.
- Alarmas sin prioridad ni lifecycle.

## Scaling Policy

- **Small**: IAE solo, skills por trigger, FV proporcional.
- **Medium**: IAE + QA, RQ + IR + FV, interfaces definidas, simulacion.
- **Large/High-Risk**: EA coordina + IAE + RE + SE + QA + TDE, los cuatro
  gates, trazabilidad, verificacion transversal.

## Composition Rules

- Cuando se compone con `robotics`, `robotics-cell-integration` define la
  integracion robot-PLC; `industrial-communications-design` se activa una
  sola vez.
- Cuando se compone con `software-development`, las interfaces OT-IT requieren
  contrato explicito. `industrial-communications-design` se activa una sola
  vez.
- Cuando se compone con `computer-vision`, los triggers de inspeccion y
  handshake los define el lado de automatizacion.
- Las skills compartidas se activan una sola vez por necesidad.

## Handoff Expectations

- Handoff a Robotics Engineer para integracion robot-PLC.
- Handoff a Software Engineer para interfaces software.
- Handoff a QA & Debug Engineer para simulacion y test.
- Handoff a Technical Documentation Engineer para documentacion.
- Todo handoff incluye artefacto, estado, evidencia, decisiones, riesgos,
  siguiente owner.

## Done Criteria

- PLC architecture completa con FBs, estados, modos y alarmas.
- Interfaces industriales definidas y documentadas.
- Criterios de simulacion/test especificados.
- Gates aplicados segun proporcionalidad.
- Handoffs completados.
