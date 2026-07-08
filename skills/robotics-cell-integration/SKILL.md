# Skill -- robotics-cell-integration

## Name

robotics-cell-integration

## Purpose

Disenar la integracion operativa y tecnica de una celula robotizada sin invadir
la arquitectura interna del PLC, software backend o sistema de vision. Definir
el contrato de integracion entre dominios, no el diseno interno de cada
dominio.

## Activation Triggers

- Proyecto involucra robot industrial integrado con PLC, vision, software u
  otros subsistemas.
- Hay necesidad de definir handshake PLC-robot, estados compartidos, permisos,
  interlocks o secuencia de celula.
- Modulo robotics activo con multiples subsistemas interactuando.
- Requirements Quality PASS y Decision Readiness PASS (si aplica).

## When Not To Use

- El robot opera aislado sin integracion con PLC u otros subsistemas.
- El proyecto no involucra robotica.
- Requirements Quality no ha superado PASS.
- El cambio es trivial (ej. ajuste de parametro de trayectoria) sin impacto en
  integracion.
- Se necesita arquitectura PLC interna (usar `plc-software-architecture`).
- Se necesita diseno de comunicaciones como artefacto principal (usar
  `industrial-communications-design`).

## Primary Owner

Robotics Engineer

## Participants

- Industrial Automation Engineer (define lado PLC del contrato).
- Software Engineer (define lado software del contrato).
- Engineering Architect (coordina coherencia transversal).
- QA & Debug Engineer (define criterios de testabilidad de integracion).
- Technical Documentation Engineer (documenta contrato de integracion).

## Required Inputs

- Requisitos validados (salida de Requirements Quality Gate).
- Decision map resuelto (salida de Decision Readiness Gate, si aplica).
- `PROJECT_DISCOVERY.md` si existe.
- Arquitectura PLC si existe (`PLC_ARCHITECTURE.md`).
- Arquitectura de software si existe.
- Especificaciones de robot, herramientas y perifericos.
- ADRs aplicables.

## Procedure

1. Confirmar precondiciones: RQ PASS y DR PASS (si aplica).
2. Definir objetivo de la celula robotizada.
3. Asignar responsabilidades por comportamiento: que hace el PLC, que hace el
   robot, que hace software, que hace vision.
4. Definir modos operativos de la celula (auto, manual, mantenimiento,
   simulacion).
5. Disenar secuencia funcional de alto nivel de la celula.
6. Definir handshake PLC-robot: senales, orden, condiciones.
7. Disenar command/status interface entre PLC y robot.
8. Definir estados de la celula y transiciones.
9. Definir permisos y interlocks de seguridad operativa.
10. Definir recuperacion ante fallos: reset, restart, homing.
11. Definir tooling, frames y cambios de herramienta.
12. Definir senales, tiempos de espera, timeouts y watchdogs.
13. Definir coordinacion con vision (trigger, resultado, fallback).
14. Definir estrategia de simulacion y testabilidad de integracion.
15. Definir criterios de aceptacion de integracion.
16. Para cada comportamiento, registrar ownership explicito: PLC, robot, u
    otro.
17. Distinguir entre robot internal behavior, PLC orchestration, e interface
    contract.
18. Producir el artefacto de salida.

### Niveles de responsabilidad

- **Robot internal behavior**: cinematica, trayectorias, frames, homing,
  recuperacion interna del robot. Ownership: Robotics Engineer.
- **PLC orchestration**: secuenciacion de la celula, modos, permisos,
  interlocks, alarmas de celula. Ownership: Industrial Automation Engineer.
- **Interface contract**: senales, handshake, command/status, timing, timeouts,
  watchdogs. Ownership: Robotics Engineer con IAE como co-definidor del lado
  PLC.

## Required Outputs

Artefacto: `ROBOTICS_CELL_INTEGRATION.md`

Contenido obligatorio:

- Objetivo de la celula.
- Responsabilidades por comportamiento (PLC, robot, software, vision).
- Modos operativos.
- Secuencia funcional de alto nivel.
- Handshake PLC-robot.
- Command/status interface.
- Estados de la celula y transiciones.
- Permisos e interlocks.
- Recuperacion ante fallos (reset, restart, homing).
- Tooling, frames y cambios de herramienta.
- Senales, timeouts y watchdogs.
- Coordinacion con vision.
- Estrategia de simulacion y testabilidad.
- Criterios de aceptacion de integracion.
- Ownership explicito por comportamiento.
- Distincion entre robot internal behavior, PLC orchestration, e interface
  contract.

## Consumer

Engineering Architect (coherencia transversal), Robotics Engineer (planificacion
e implementacion robotica), Industrial Automation Engineer (planificacion PLC).

## Stop Condition

La skill se detiene cuando existe un contrato de integracion suficientemente
claro para que PLC y robot puedan planificarse e implementarse sin ownership
ambiguo. No es necesario que las trayectorias finales esten disenadas ni que el
programa PLC este completo.

## Gates Interaction

- **Precondicion**: Requirements Quality PASS. Decision Readiness PASS (si
  aplica).
- **Despues de**: el contrato de integracion se entrega a planificacion e
  implementacion. Implementation Review revisara la implementacion posterior.
- **No ejecuta**: Implementation Review, Final Verification ni ningun gate.
- **No reemplaza**: ADRs. Las decisiones de integracion dificiles de revertir
  se proponen como ADR.

## Agent Interaction

- **Activada por**: Robotics Engineer (owner).
- **Coordina con**: Industrial Automation Engineer (lado PLC), Software
  Engineer (lado software), Engineering Architect (transversal).
- **Handoff a**: Robotics Engineer e Industrial Automation Engineer para
  planificacion e implementacion en sus dominios.

## Evidence Required

- `ROBOTICS_CELL_INTEGRATION.md` con todos los campos obligatorios.
- Ownership explicito por comportamiento.
- Distincion entre robot internal behavior, PLC orchestration, e interface
  contract.
- Comportamiento ante timeout, fallo de comunicacion, y reset definido.

## Failure Modes

- Invadir arquitectura interna del PLC (disenar logica PLC en lugar de
  contrato).
- Invadir arquitectura interna del robot (disenar trayectorias finales en
  lugar de contrato).
- Ownership ambiguo: comportamiento sin owner claro.
- Asumir que robot y PLC comparten automaticamente el mismo modelo de estados.
- No definir comportamiento ante timeout o fallo de handshake.
- No definir recuperacion ante fallos.
- Mezclar interface contract con robot internal behavior.

## Escalation Rules

- Conflicto de ownership entre PLC y robot -> Engineering Architect resuelve.
- Interface con vision -> escalar a especialista de vision/IA.
- Interface con software -> Software Engineer.
- Seguridad funcional -> escalar al usuario o especialista certificado.
- Decision de integracion dificil de revertir -> proponer ADR, escalar a
  Engineering Architect.
- Testabilidad insuficiente -> QA & Debug Engineer.

## Done Criteria

- `ROBOTICS_CELL_INTEGRATION.md` completo con todos los campos obligatorios.
- Ownership explicito por comportamiento sin ambiguedad.
- Handshake PLC-robot definido con senales, orden y condiciones.
- Comportamiento ante timeout, fallo y reset definido.
- Distincion entre robot internal behavior, PLC orchestration, e interface
  contract.
- Estrategia de simulacion y testabilidad definida.
- Artefacto entregado a Robotics Engineer e Industrial Automation Engineer para
  planificacion.
