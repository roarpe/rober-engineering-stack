# Skill -- industrial-communications-design

## Name

industrial-communications-design

## Purpose

Disenar contratos de comunicacion mantenibles, diagnosticables y verificables
entre subsistemas industriales. Definir el contrato de comunicacion, no
implementar drivers, servidores, clientes ni protocolos completos.

## Activation Triggers

- Hay multiples subsistemas que necesitan comunicarse (PLC, robot, software,
  vision, datos).
- Hay necesidad de definir data model, timing, failure behavior o
  reconnection entre subsistemas.
- Requirements Quality PASS y Decision Readiness PASS (si aplica).
- Modulo industrial-automation, robotics, data-engineering o
  software-development activo con interfaces entre dominios.

## When Not To Use

- Un solo subsistema sin interfaces externas.
- Las comunicaciones ya estan definidas y validadas y no han cambiado.
- Existe una decision blocking abierta sobre tecnologia de comunicaciones (la
  skill no selecciona tecnologia si hay decision sin resolver).
- El cambio es trivial (ej. cambiar un tag name) sin impacto en contrato.
- Se necesita arquitectura de dominio (usar `plc-software-architecture` o
  `robotics-cell-integration`).

## Primary Owner

- Industrial Automation Engineer cuando predomina OT/PLC.
- Software Engineer cuando predomina aplicacion/API.
- Engineering Architect resuelve ownership si es transversal o hay conflicto.

## Participants

- Engineering Architect (resuelve ownership transversal).
- Robotics Engineer (define lado robot del contrato).
- Software Engineer (define lado software del contrato).
- QA & Debug Engineer (define criterios de verificacion de comunicaciones).
- Technical Documentation Engineer (documenta contratos).

## Required Inputs

- Requisitos validados (salida de Requirements Quality Gate).
- Decision map resuelto (salida de Decision Readiness Gate, si aplica).
- Arquitecturas de dominio existentes (PLC, robot, software).
- Especificaciones de protocolo o tecnologia cuando este decidida.
- ADRs aplicables.

## Procedure

1. Confirmar precondiciones: RQ PASS y DR PASS (si aplica).
2. Identificar todas las interfaces relevantes entre subsistemas.
3. Para cada interfaz, registrar:
   - Producer (quien produce los datos).
   - Consumer (quien consume los datos).
   - Purpose (para que sirve la comunicacion).
   - Data Contract (naming, tipos, unidades, escalado, endianness cuando
     aplique).
   - Ownership (quien es owner del contrato).
   - Update Model (polling, eventos, ciclico, on-change).
   - Timing Expectations (frecuencia, latencia maxima, jitter tolerado).
   - Failure Behavior (que pasa si no hay datos, timeout, datos invalidos).
   - Recovery Behavior (reconexion, retry, heartbeat, watchdog).
   - Diagnostics (como se diagnostica un problema de comunicacion).
   - Verification Method (como se verifica que la comunicacion funciona).
4. Definir data model comun: naming, tipos, unidades, escalado.
5. Definir sincronizacion, timestamps y quality/status cuando aplique.
6. Definir timeouts, retries, watchdogs y heartbeat por interfaz.
7. Definir reconnection y idempotencia cuando aplique.
8. Definir versionado y compatibilidad de contratos.
9. Definir seguridad aplicable (autenticacion, autorizacion, cifrado cuando
   aplique).
10. Definir observabilidad y diagnostico de comunicaciones.
11. Verificar que no se duplica arquitectura de dominio (PLC, robot, software).
12. Producir el artefacto de salida.

## Required Outputs

Artefacto: `INDUSTRIAL_COMMUNICATIONS_DESIGN.md`

Contenido obligatorio:

- Lista de interfaces con todos los campos del procedimiento (Producer,
  Consumer, Purpose, Data Contract, Ownership, Update Model, Timing
  Expectations, Failure Behavior, Recovery Behavior, Diagnostics, Verification
  Method).
- Data model comun (naming, tipos, unidades, escalado, endianness).
- Sincronizacion, timestamps y quality/status.
- Timeouts, retries, watchdogs y heartbeat por interfaz.
- Reconnection e idempotencia cuando aplique.
- Versionado y compatibilidad.
- Seguridad aplicable.
- Observabilidad y diagnostico.

## Consumer

Engineering Architect (coherencia transversal), especialistas de dominio
(planificacion e implementacion de comunicaciones).

## Stop Condition

La skill se detiene cuando existen contratos de comunicacion suficientes para
planificacion, implementacion y verificacion sin ambiguedades criticas. No es
necesario que los drivers esten implementados ni que los protocolos esten
configurados.

## Gates Interaction

- **Precondicion**: Requirements Quality PASS. Decision Readiness PASS (si
  aplica).
- **Despues de**: los contratos se entregan a planificacion e implementacion.
  Implementation Review revisara la implementacion posterior.
- **No ejecuta**: Implementation Review, Final Verification ni ningun gate.
- **No selecciona tecnologia**: si existe decision blocking abierta sobre
  tecnologia de comunicaciones, la skill no la resuelve. Escala a Decision
  Readiness Gate.

## Agent Interaction

- **Activada por**: Industrial Automation Engineer o Software Engineer segun
  predominio.
- **Resolucion de ownership**: Engineering Architect si es transversal.
- **Coordina con**: especialistas de cada dominio involucrado en las
  interfaces.
- **Handoff a**: especialistas de dominio para implementacion de su lado del
  contrato.

## Evidence Required

- `INDUSTRIAL_COMMUNICATIONS_DESIGN.md` con todos los campos obligatorios.
- Cada interfaz con los 11 campos minimos definidos.
- Comportamiento ante timeout, perdida de conexion y datos invalidos definido
  por interfaz.
- Ownership del contrato definido por interfaz.

## Failure Modes

- Implementar drivers, servidores o clientes en lugar de contratos.
- Seleccionar tecnologia definitiva cuando existe decision blocking abierta.
- Duplicar arquitectura de dominio (definir logica PLC o robotica interna).
- No definir comportamiento ante timeout o perdida de conexion.
- No definir ownership del contrato.
- Asumir comunicaciones perfectas sin failure behavior.
- Mezclar data model con logica de aplicacion.

## Escalation Rules

- Decision de tecnologia no resuelta -> escalar a Decision Readiness Gate.
- Conflicto de ownership entre dominios -> Engineering Architect resuelve.
- Interface con seguridad funcional -> escalar al usuario o especialista
  certificado.
- Verificacion de comunicaciones insuficiente -> QA & Debug Engineer.
- Decision de versionado o compatibilidad dificil de revertir -> proponer ADR.

## Done Criteria

- `INDUSTRIAL_COMMUNICATIONS_DESIGN.md` completo con todos los campos
  obligatorios.
- Cada interfaz con los 11 campos minimos definidos.
- Comportamiento ante fallo definido por interfaz.
- Ownership del contrato definido por interfaz sin ambiguedad.
- No se ha seleccionado tecnologia con decision blocking abierta.
- Artefacto entregado a especialistas de dominio para implementacion.
