# Skill -- machine-diagnostics

## Name

machine-diagnostics

## Purpose

Disenar la estrategia de diagnostico de una maquina o sistema industrial: como
el sistema permitira detectar, localizar, explicar y recuperar fallos. No es
una lista de alarmas, no es debugging de un incidente especifico, no reemplaza
`systematic-debugging` ni a QA & Debug Engineer.

## Activation Triggers

- Hay maquina, celula o sistema industrial con multiples subsistemas (PLC,
  robot, vision, software, datos) que requiere diagnostico.
- Hay necesidad de definir alarmas, eventos, contexto de fallo, recuperacion
  o troubleshooting verificable.
- Modulo industrial-automation, robotics o software-development activo con
  requisitos de diagnostico.
- Requirements Quality PASS y Decision Readiness PASS (si aplica).

## When Not To Use

- El sistema es trivial sin requisitos de diagnostico.
- Ya existe estrategia de diagnostico validada y no ha cambiado.
- Se necesita debugging de un fallo concreto existente (usar
  `systematic-debugging` con QA & Debug Engineer).
- Se necesita arquitectura PLC (usar `plc-software-architecture`).
- Se necesita contratos de comunicacion (usar
  `industrial-communications-design`).
- Se necesita observabilidad interna de software (usar
  `industrial-python-engineering` o estandares de software).

## Primary Owner

Industrial Automation Engineer

## Participants

- Engineering Architect (coherencia transversal).
- Robotics Engineer (diagnostico de robot).
- Software Engineer (diagnostico de software/observabilidad).
- QA & Debug Engineer (verificacion de estrategia de diagnostico).
- Technical Documentation Engineer (documentacion de troubleshooting).

## Required Inputs

- Requisitos validados (salida de Requirements Quality Gate).
- Decision map resuelto (salida de Decision Readiness Gate, si aplica).
- Arquitecturas de dominio existentes (PLC, robot, software, comunicaciones).
- Especificaciones de hardware, senales y equipos.
- ADRs aplicables.

## Procedure

1. Confirmar precondiciones: RQ PASS y DR PASS (si aplica).
2. Definir objetivos de diagnostico: que fallos deben detectarse, localizarse,
   explicarse y recuperarse.
3. Definir limites del sistema: que subsistemas estan dentro del alcance de
   diagnostico.
4. Definir dominios de fallo: PLC, robot, vision, software, comunicaciones,
   hardware, entorno.
5. Asignar ownership de diagnostico por dominio de fallo.
6. Definir taxonomia de fallos: categorias, tipos, causas comunes.
7. Definir modelo de severidad: CRITICAL, MAJOR, MINOR, INFO.
8. Definir lifecycle de alarmas y eventos: generacion, activacion,
   acknowledment, reset, clearance.
9. Definir estrategia first-out cuando aplique (primera alarma que disparó
   una cascada).
10. Definir captura de contexto en fallo: estado de maquina, senales, modo
    operativo, timestamp, secuencia de eventos previos.
11. Definir logging, metricas y traces de diagnostico: que se registra, con
    que frecuencia, durante cuanto tiempo, como se accede.
12. Definir contratos de diagnostico por subsistema: que informacion de
    diagnostico provee cada subsistema (PLC, robot, vision, software).
13. Definir modelo de recuperacion:
    - Que puede hacer el operador (reset, acknowledge, modo manual).
    - Que puede hacer mantenimiento (inspeccion, ajuste, reemplazo).
    - Que requiere intervencion de ingenieria (cambio de logica, bug,
      diseno).
14. Definir guia de operador: acciones permitidas, acciones prohibidas,
    informacion a reportar.
15. Definir guia de mantenimiento: procedimientos de diagnostico, herramientas,
    repuestos, seguridad.
16. Definir escalado a ingenieria: criterios, informacion requerida, canal.
17. Definir verificacion de recuperacion: como se confirma que el fallo esta
    resuelto y el sistema puede reanudar.
18. Definir riesgos de la estrategia de diagnostico (falsos positivos, falsos
    negativos, sobrecarga de alarmas, contexto perdido).
19. Registrar decisiones abiertas de diagnostico.
20. Producir el artefacto de salida.

### Distincion fundamental

- **Diagnostics design** (esta skill): como el sistema permitira detectar,
  localizar, explicar y recuperar fallos. Es diseno proactivo.
- **Debugging execution** (systematic-debugging + QA & Debug Engineer):
  investigacion concreta de un fallo existente. Es reactivo.

machine-diagnostics diseña lo primero. systematic-debugging y QA & Debug
Engineer ejecutan lo segundo.

### Preguntas de diagnostico

Para cada dominio de fallo, la estrategia debe permitir responder:

- What was the likely root cause?
- What evidence supports that conclusion?
- What can the operator do?
- What can maintenance do?
- What requires engineering intervention?
- How is recovery verified?

## Required Outputs

Artefacto: `MACHINE_DIAGNOSTICS.md`

Contenido obligatorio:

- Objetivos de diagnostico.
- Limites del sistema.
- Dominios de fallo con ownership.
- Taxonomia de fallos.
- Modelo de severidad.
- Lifecycle de alarmas y eventos.
- Estrategia first-out cuando aplique.
- Captura de contexto en fallo.
- Logging, metricas y traces de diagnostico.
- Contratos de diagnostico por subsistema.
- Modelo de recuperacion (operador, mantenimiento, ingenieria).
- Guia de operador.
- Guia de mantenimiento.
- Escalado a ingenieria.
- Verificacion de recuperacion.
- Riesgos de la estrategia de diagnostico.
- Decisiones abiertas.
- Distincion explicita entre diagnostics design y debugging execution.

## Consumer

Engineering Architect (coherencia transversal), especialistas de dominio
(planificacion e implementacion de diagnostico), QA & Debug Engineer
(verificacion).

## Stop Condition

La skill se detiene cuando existe una estrategia diagnostica suficiente para
que los subsistemas puedan implementar observabilidad, alarmas, contexto,
recuperacion y troubleshooting verificables. No debe continuar hasta definir
cada alarma concreta de toda la maquina.

## Gates Interaction

- **Precondicion**: Requirements Quality PASS. Decision Readiness PASS (si
  aplica).
- **Despues de**: la estrategia se entrega a planificacion e implementacion.
  Implementation Review revisara la implementacion posterior.
- **No ejecuta**: Implementation Review, Final Verification ni ningun gate.
- **No reemplaza**: ADRs. Las decisiones de diagnostico dificiles de revertir
  se proponen como ADR.

## Agent Interaction

- **Activada por**: Industrial Automation Engineer (owner).
- **Coordina con**: Robotics Engineer (robot), Software Engineer (software),
  QA & Debug Engineer (verificacion), Engineering Architect (transversal).
- **Handoff a**: especialistas de dominio para implementacion de diagnostico
  en su subsistema.

## Evidence Required

- `MACHINE_DIAGNOSTICS.md` con todos los campos obligatorios.
- Ownership de diagnostico por dominio de fallo definido.
- Modelo de recuperacion con roles (operador, mantenimiento, ingenieria).
- Distincion explicita entre diagnostics design y debugging execution.
- Contratos de diagnostico por subsistema definidos.

## Failure Modes

- Convertirse en una simple lista de alarmas sin estrategia.
- Duplicar `systematic-debugging` (debugging reactivo vs diseno proactivo).
- Duplicar arquitectura PLC (definir logica PLC en lugar de estrategia de
  diagnostico).
- Duplicar contratos de comunicacion.
- Duplicar observabilidad interna de software.
- No distinguir diagnostics design de debugging execution.
- No definir ownership de diagnostico por dominio.
- No definir modelo de recuperacion con roles.
- Definir cada alarma concreta en lugar de estrategia (scope creep).
- Aprobar seguridad funcional (fuera de scope).

## Escalation Rules

- Conflicto de ownership de diagnostico entre dominios -> Engineering
  Architect resuelve.
- Diagnostico de robot -> Robotics Engineer.
- Diagnostico de software -> Software Engineer.
- Verificacion de estrategia -> QA & Debug Engineer.
- Fallo que requiere cambio arquitectonico -> Engineering Architect.
- Seguridad funcional -> escalar al usuario o especialista certificado.
- Decision de diagnostico dificil de revertir -> proponer ADR.

## Done Criteria

- `MACHINE_DIAGNOSTICS.md` completo con todos los campos obligatorios.
- Ownership de diagnostico por dominio de fallo sin ambiguedad.
- Modelo de recuperacion con roles (operador, mantenimiento, ingenieria).
- Distincion explicita entre diagnostics design y debugging execution.
- Contratos de diagnostico por subsistema definidos.
- Verificacion de recuperacion definida.
- Riesgos de la estrategia identificados.
- No es una lista de alarmas.
- No duplica systematic-debugging, arquitectura PLC, contratos de
  comunicacion ni observabilidad de software.
- Artefacto entregado a especialistas de dominio para implementacion.
