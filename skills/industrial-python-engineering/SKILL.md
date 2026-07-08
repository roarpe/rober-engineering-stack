# Skill -- industrial-python-engineering

## Name

industrial-python-engineering

## Purpose

Definir estandares de ingenieria Python para sistemas industriales: estructura,
configuracion, logging, excepciones, typing, testing, comunicaciones,
persistencia, packaging, despliegue y observabilidad. No es una guia generica
de Python; especializa para entornos industriales con requisitos de
fiabilidad, observabilidad y integracion con PLC, robots, vision y datos.

## Activation Triggers

- Hay codigo Python que se ejecuta en entorno industrial (produccion,
  mantenimiento, laboratorio, celula robotizada).
- Hay necesidad de definir estandares de estructura, config, logging,
  excepciones, testing u observabilidad para un proyecto Python industrial.
- Modulo software-development, data-engineering o computer-vision activo con
  Python como lenguaje principal o secundario.
- Requirements Quality PASS y Decision Readiness PASS (si aplica).

## When Not To Use

- El proyecto no involucra Python.
- El codigo Python es un script desechable sin requisitos de mantenibilidad ni
  produccion.
- Ya existen estandares Python industriales validados y no han cambiado.
- Se necesita arquitectura de comunicaciones (usar
  `industrial-communications-design`).
- Se necesita integracion de vision/IA (usar `vision-ai-integration`).
- Se necesita arquitectura PLC (usar `plc-software-architecture`).

## Primary Owner

Software Engineer

## Participants

- Engineering Architect (coherencia transversal).
- QA & Debug Engineer (criterios de testabilidad y observabilidad).
- Industrial Automation Engineer (interfaces con PLC/comunicaciones
  industriales).
- Robotics Engineer (interfaces con robot).
- Technical Documentation Engineer (documentacion de estandares).

## Required Inputs

- Requisitos validados (salida de Requirements Quality Gate).
- Decision map resuelto (salida de Decision Readiness Gate, si aplica).
- Arquitectura de software si existe.
- Interfaces con PLC, robot, vision y datos.
- ADRs aplicables.
- Estandares externos aplicables (PEP 8, PEP 484, etc.) cuando sean relevantes.

## Procedure

1. Confirmar precondiciones: RQ PASS y DR PASS (si aplica).
2. Definir estructura del proyecto Python (layout, modulos, paquetes,
   separacion de responsabilidades).
3. Definir gestion de configuracion (ficheros, variables de entorno, perfiles,
   secretos, configuracion por entorno).
4. Definir estandares de logging (niveles, formato, structured logging,
   correlacion, rotacion, retencion).
5. Definir estrategia de excepciones (jerarquia, captura, propagacion,
  reporte, no silenciar).
6. Definir estandares de typing (mypy, strictness, type hints en APIs
   publicas).
7. Definir estrategia de testing (unitarios, integracion, fixtures, cobertura
   minima, pruebas de comunicaciones, pruebas de fallo).
8. Definir patrones de comunicaciones industriales desde Python (OPC UA,
  MQTT, Modbus, REST) a nivel de cliente, no de contrato (el contrato lo
  define `industrial-communications-design`).
9. Definir persistencia (bases de datos, ficheros, caches, migraciones,
  retencion).
10. Definir packaging y despliegue (entornos virtuales, contenedores,
    dependencias, versionado, reproducibilidad).
11. Definir observabilidad (metricas, traces, health checks, alertas,
    dashboards).
12. Definir comportamiento ante fallos externos (PLC no responde, robot en
    error, vision no disponible, red caida, datos invalidos).
13. Definir graceful shutdown y manejo de senales.
14. Definir estrategia de compatibilidad y versionado de APIs Python.
15. Identificar decisiones dificiles de revertir y proponer ADRs.
16. Producir el artefacto de salida.

### Comportamiento ante fallos externos

Para cada interfaz externa (PLC, robot, vision, datos, red):

- Timeout: cuanto esperar, que hacer si expira.
- Reconexion: estrategia, backoff, max retries, circuit breaker cuando
  aplique.
- Datos invalidos: validacion, rechazo, log, fallback.
- Servicio no disponible: modo degradado, reporte, alerta.
- Graceful shutdown: cleanup de recursos, notificacion a subsistemas.

## Required Outputs

Artefacto: `INDUSTRIAL_PYTHON_STANDARDS.md`

Contenido obligatorio:

- Estructura del proyecto.
- Gestion de configuracion.
- Estandares de logging.
- Estrategia de excepciones.
- Estandares de typing.
- Estrategia de testing.
- Patrones de comunicaciones industriales (cliente, no contrato).
- Persistencia.
- Packaging y despliegue.
- Observabilidad.
- Comportamiento ante fallos externos por interfaz.
- Graceful shutdown y manejo de senales.
- Versionado de APIs Python.
- ADRs propuestos.

## Consumer

Engineering Architect (coherencia transversal), Software Engineer
(planificacion e implementacion), QA & Debug Engineer (testabilidad).

## Stop Condition

La skill se detiene cuando existen estandares Python suficientes para
planificacion, implementacion y verificacion sin ambiguedades criticas. No es
necesario que cada modulo tenga su codigo implementado ni que cada test este
escrito.

## Gates Interaction

- **Precondicion**: Requirements Quality PASS. Decision Readiness PASS (si
  aplica).
- **Despues de**: los estandares se entregan a planificacion e
  implementacion. Implementation Review revisara la implementacion posterior.
- **No ejecuta**: Implementation Review, Final Verification ni ningun gate.
- **No reemplaza**: ADRs. Las decisiones de estandares dificiles de revertir
  se proponen como ADR.

## Agent Interaction

- **Activada por**: Software Engineer (owner).
- **Coordina con**: Industrial Automation Engineer (interfaces PLC), Robotics
  Engineer (interfaces robot), QA & Debug Engineer (testabilidad/observabilidad).
- **Handoff a**: Software Engineer para planificacion e implementacion.

## Evidence Required

- `INDUSTRIAL_PYTHON_STANDARDS.md` con todos los campos obligatorios.
- Comportamiento ante fallos externos definido por interfaz.
- Estandares de logging y observabilidad definidos.
- Estrategia de testing definida.

## Failure Modes

- Ser una guia generica de Python sin especializacion industrial.
- No definir comportamiento ante fallos externos (PLC, robot, vision, red).
- Duplicar contratos de comunicacion (responsabilidad de
  `industrial-communications-design`).
- Duplicar integracion de vision/IA (responsabilidad de
  `vision-ai-integration`).
- No definir graceful shutdown.
- No definir observabilidad ni alertas.
- Mezclar estandares con implementacion completa.
- Asumir entorno perfecto sin fallos de red ni servicios caidos.

## Escalation Rules

- Decision de arquitectura transversal -> Engineering Architect.
- Interface con PLC -> Industrial Automation Engineer.
- Interface con robot -> Robotics Engineer.
- Contrato de comunicaciones -> escalar a `industrial-communications-design`.
- Integracion de vision/IA -> escalar a `vision-ai-integration`.
- Testabilidad insuficiente -> QA & Debug Engineer.
- Decision de estandar dificil de revertir -> proponer ADR.

## Done Criteria

- `INDUSTRIAL_PYTHON_STANDARDS.md` completo con todos los campos obligatorios.
- Comportamiento ante fallos externos definido por interfaz.
- Estandares de estructura, config, logging, excepciones, typing, testing,
  observabilidad y despliegue definidos.
- Graceful shutdown definido.
- No duplica contratos de comunicacion ni integracion de vision/IA.
- Artefacto entregado a Software Engineer para planificacion.
