# Skill -- plc-software-architecture

## Name

plc-software-architecture

## Purpose

Transformar requisitos de automatizacion suficientemente maduros y decisiones
bloqueantes resueltas en una arquitectura PLC mantenible, modular,
diagnosticable y verificable. Producir arquitectura, no implementacion
completa.

## Activation Triggers

- Requirements Quality Gate ha superado PASS.
- Decision Readiness Gate ha superado PASS (si existieron decisiones blocking).
- Hay requisitos de automatizacion que requieren arquitectura PLC.
- Modulo industrial-automation activo.

## When Not To Use

- Requirements Quality no ha superado PASS.
- Existieron decisiones blocking y Decision Readiness no ha superado PASS.
- El proyecto no involucra PLC ni automatizacion.
- El cambio es trivial y no requiere arquitectura (ej. ajuste de parametro).
- Se necesita discovery, no arquitectura (usar `industrial-project-discovery`).
- Se necesita implementacion detallada, no arquitectura (la skill produce
  arquitectura, no codigo completo).

## Primary Owner

Industrial Automation Engineer

## Participants

- Engineering Architect (coordina coherencia transversal, aprueba ADRs).
- Robotics Engineer (define interfaces robot-PLC).
- Software Engineer (define interfaces software-PLC).
- Technical Documentation Engineer (documenta arquitectura).
- QA & Debug Engineer (define criterios de testabilidad).

## Required Inputs

- Requisitos validados (salida de Requirements Quality Gate).
- Decision map resuelto (salida de Decision Readiness Gate, si aplica).
- `PROJECT_DISCOVERY.md` si existe.
- ADRs aplicables.
- Especificaciones de hardware, senales y comunicaciones.
- Interfaces con otros subsistemas (robot, software, vision, datos).

## Procedure

1. Confirmar precondiciones: RQ PASS y DR PASS (si aplica).
2. Definir estructura del programa PLC (tareas, prioridades, ciclo de
   ejecucion).
3. Separar responsabilidades en Program Organization Units (POUs).
4. Disenar Function Blocks, Functions y Data Blocks o equivalentes.
5. Definir maquinas de estados principales y subestados.
6. Disenar secuencias y logica de control.
7. Definir modos de operacion (auto, manual, mantenimiento, simulacion).
8. Disenar command/status interfaces entre modulos.
9. Definir I/O abstraction (capa de abstraccion de senales fisicas).
10. Disenar alarmas y diagnostico.
11. Definir recuperacion ante fallos.
12. Definir configuracion y recetas cuando aplique.
13. Disenar interfaces de comunicaciones (OPC UA, Modbus, Profinet, etc.) a
    nivel de contrato, no de protocolo interno.
14. Definir estrategia de simulacion y testabilidad.
15. Definir limites con robot, software y vision (contratos, no diseno interno
    de otros dominios).
16. Identificar decisiones arquitectonicas dificiles de revertir o con
    alternativas reales y proponer ADRs.
17. Distinguir explicitamente entre arquitectura, diseno detallado e
    implementacion.
18. Producir el artefacto de salida.

### Niveles de abstraccion

- **Arquitectura**: estructura, modulos, responsabilidades, interfaces,
  estados, modos, estrategias. Es lo que produce esta skill.
- **Diseno detallado**: logica interna de cada FB, algoritmos, parametros. Se
  produce durante planificacion/implementacion, no aqui.
- **Implementacion**: codigo PLC completo. Se produce durante ejecucion, no
  aqui.

## Required Outputs

Artefacto: `PLC_ARCHITECTURE.md`

Contenido obligatorio:

- Estructura del programa (tareas, prioridades, ciclo).
- POUs y separacion de responsabilidades.
- Function Blocks, Functions y Data Blocks principales.
- Maquinas de estados principales.
- Secuencias y logica de control de alto nivel.
- Modos de operacion.
- Command/status interfaces.
- I/O abstraction.
- Alarmas y diagnostico.
- Recuperacion ante fallos.
- Configuracion y recetas (si aplica).
- Interfaces de comunicaciones (contratos).
- Estrategia de simulacion y testabilidad.
- Limites con robot, software y vision.
- ADRs propuestos (para decisiones dificiles de revertir).
- Distincion explicita entre arquitectura, diseno detallado e implementacion.

## Consumer

Engineering Architect (coherencia transversal) e Industrial Automation Engineer
(planificacion e implementacion).

## Stop Condition

La skill se detiene cuando existe arquitectura suficiente para planificacion e
implementacion verificable. No es necesario que todo el codigo PLC este
disenado ni que cada FB tenga su logica interna definida.

## Gates Interaction

- **Precondicion**: Requirements Quality PASS. Decision Readiness PASS (si
  aplica).
- **Despues de**: la arquitectura se entrega a planificacion/implementacion.
  Implementation Review revisara la implementacion posterior.
- **No ejecuta**: Implementation Review, Final Verification ni ningun gate.
- **No reemplaza**: ADRs. Las decisiones arquitectonicas dificiles de revertir
  se proponen como ADR para aprobacion de Engineering Architect.

## Agent Interaction

- **Activada por**: Industrial Automation Engineer (owner).
- **Coordina con**: Engineering Architect para coherencia transversal y
  aprobacion de ADRs.
- **Interfaces con**: Robotics Engineer (robot-PLC), Software Engineer
  (software-PLC), QA & Debug Engineer (testabilidad).
- **Handoff a**: Industrial Automation Engineer para planificacion e
  implementacion.

## Evidence Required

- `PLC_ARCHITECTURE.md` con todos los campos obligatorios.
- ADRs propuestos para decisiones dificiles de revertir o con alternativas
  reales.
- Distincion explicita entre arquitectura, diseno detallado e implementacion.
- Interfaces con otros subsistemas definidas como contratos.

## Failure Modes

- Intentar producir implementacion completa en lugar de arquitectura.
- Diseñar arquitectura robotica interna o backend general (fuera de dominio).
- No proponer ADR para decisiones difficiles de revertir.
- Mezclar arquitectura con diseno detallado.
- Asumir decisiones blocking resueltas sin verificar DR PASS.
- Vendor lock-in innecesario (la arquitectura base debe ser vendor-neutral).
- No definir estrategia de testabilidad.

## Escalation Rules

- Decision arquitectonica transversal -> Engineering Architect.
- Interface con robot -> Robotics Engineer.
- Interface con software -> Software Engineer.
- Seguridad funcional -> escalar al usuario o especialista certificado.
- Testabilidad insuficiente -> QA & Debug Engineer.
- Decision dificil de revertir -> proponer ADR, escalar a Engineering Architect
  para aprobacion.

## Done Criteria

- `PLC_ARCHITECTURE.md` completo con todos los campos obligatorios.
- Estructura, POUs, FBs, estados, modos y alarmas definidos.
- Interfaces con otros subsistemas definidas como contratos.
- ADRs propuestos para decisiones difficiles de revertir.
- Distincion explicita entre arquitectura, diseno detallado e implementacion.
- Estrategia de simulacion y testabilidad definida.
- Arquitectura vendor-neutral salvo justificacion explicita.
- Artefacto entregado a Industrial Automation Engineer para planificacion.
