# Skill -- industrial-python-engineering

## Name

industrial-python-engineering

## Purpose

Disenar la ingenieria de software Python industrial necesaria para producir
sistemas mantenibles, diagnosticables, testeables, desplegables e integrables
con OT (PLC, robots, vision, datos). Los estandares (estructura, config,
logging, excepciones, typing, testing, packaging, observabilidad) son parte
del diseno de ingenieria, no el proposito completo. No es una guia generica
de Python; especializa para entornos industriales con requisitos de
fiabilidad, observabilidad, integracion con OT y comportamiento ante fallos
de subsistemas externos.

## Activation Triggers

- Hay codigo Python que se ejecuta en entorno industrial (produccion,
  mantenimiento, laboratorio, celula robotizada).
- Hay necesidad de disenar ingenieria de software Python industrial: estructura,
  arquitectura de aplicacion, lifecycle, concurrencia, observabilidad, testing,
  despliegue o comportamiento ante fallos externos.
- Modulo software-development, data-engineering o computer-vision activo con
  Python como lenguaje principal o secundario.
- Requirements Quality PASS y Decision Readiness PASS (si aplica).

## When Not To Use

- El proyecto no involucra Python.
- El codigo Python es un script desechable sin requisitos de mantenibilidad ni
  produccion.
- Ya existe diseno de ingenieria Python industrial validado y no ha cambiado.
- Se necesita arquitectura de comunicaciones (usar
  `industrial-communications-design`).
- Se necesita integracion de vision/IA (usar `vision-ai-integration`).
- Se necesita arquitectura PLC (usar `plc-software-architecture`).
- Se necesita arquitectura robotica interna (usar `robotics-cell-integration`).

## Primary Owner

Software Engineer

## Participants

- Engineering Architect (coherencia transversal).
- QA & Debug Engineer (criterios de testabilidad y observabilidad).
- Industrial Automation Engineer (interfaces con PLC/comunicaciones
  industriales).
- Robotics Engineer (interfaces con robot).
- Technical Documentation Engineer (documentacion de ingenieria).

## Required Inputs

- Requisitos validados (salida de Requirements Quality Gate).
- Decision map resuelto (salida de Decision Readiness Gate, si aplica).
- Arquitectura de software si existe.
- Interfaces con PLC, robot, vision y datos.
- ADRs aplicables.
- Estandares externos aplicables (PEP 8, PEP 484, etc.) cuando sean relevantes.
- Restricciones de despliegue, entornos y operacion.

## Procedure

1. Confirmar precondiciones: RQ PASS y DR PASS (si aplica).
2. Definir objetivo y contexto del software Python en el sistema industrial.
3. Definir arquitectura de aplicacion (capas, componentes, responsabilidades,
   dependencias internas).
4. Definir estructura del proyecto Python (layout, modulos, paquetes,
   separacion de responsabilidades).
5. Definir componentes y responsabilidades (que hace cada componente, que no
   hace, fronteras).
6. Definir contratos externos (que interfaces expone y consume el software
   Python con PLC, robot, vision, datos) a nivel de aplicacion, no de
   protocolo (el contrato de comunicacion lo define
   `industrial-communications-design`).
7. Definir gestion de configuracion y secretos (ficheros, variables de
   entorno, perfiles, secretos, configuracion por entorno).
8. Definir estrategia de errores y excepciones (jerarquia, captura,
   propagacion, reporte, no silenciar).
9. Definir logging (niveles, formato, structured logging, correlacion,
   rotacion, retencion).
10. Definir lifecycle de la aplicacion: startup, shutdown, cleanup, manejo de
    senales.
11. Definir concurrencia y async cuando aplique (threads, asyncio, locks,
    queues, race conditions, resource limits).
12. Definir tipos y validacion de datos (type hints, mypy, pydantic/schemas,
    validacion de input/output).
13. Definir serializacion (JSON, protobuf, pickle, formatos binarios cuando
    aplique).
14. Definir patrones de comunicaciones industriales desde Python (OPC UA,
    MQTT, Modbus, REST) a nivel de cliente, no de contrato.
15. Definir persistencia (bases de datos, ficheros, caches, migraciones,
    retencion).
16. Definir dependencias y packaging (entornos virtuales, contenedores,
    dependencias, versionado, reproducibilidad).
17. Definir entornos (desarrollo, testing, staging, produccion; diferencias,
    variables, configuracion).
18. Definir estrategia de testing (unitarios, integracion, fixtures, cobertura
    minima, pruebas de comunicaciones, pruebas de fallo).
19. Definir simulacion (mocks de PLC, robot, vision; simulacion de fallos;
    entornos de test reproducibles).
20. Evaluar dependencia temporal: identificar si el sistema tiene
    comportamiento dependiente del tiempo (watchdogs, timeouts, retries,
    backoff, validacion de timestamps, freshness, ventanas de recuperacion,
    debounce/delay, scheduled behavior). Si existe, decidir explicitamente
    si clock injection aplica y documentar la decision. Ver subseccion
    "Inyeccion de reloj".
21. Definir observabilidad (metricas, traces, health checks, alertas,
    dashboards).
22. Definir despliegue (estrategia, pipeline, rollback cuando aplique,
    zero-downtime cuando aplique).
23. Definir comportamiento ante fallos externos (PLC no responde, robot en
    error, vision no disponible, red caida, datos invalidos, stale data).
24. Definir riesgos y decisiones abiertas.
25. Identificar decisiones dificiles de revertir y proponer ADRs.
26. Producir el artefacto de salida.

### Comportamiento ante fallos externos

Para cada interfaz externa (PLC, robot, vision, datos, red):

- Timeout: cuanto esperar, que hacer si expira.
- Reconexion: estrategia, backoff, max retries, circuit breaker cuando
  aplique.
- Datos invalidos: validacion, rechazo, log, fallback.
- Stale data: deteccion de datos obsoletos, criterio de frescura, que hacer
  cuando los datos no se actualizan pero la conexion sigue activa.
- Servicio no disponible: modo degradado, reporte, alerta.
- Graceful shutdown: cleanup de recursos, notificacion a subsistemas.

### Inyeccion de reloj

Cuando el sistema tiene comportamiento dependiente del tiempo, evaluar
explicitamente si clock injection (abstraccion de fuente de tiempo
inyectable) es apropiado.

**Clock injection es apropiado cuando:**

- El comportamiento depende de tiempo observable (elapsed time, cadencia,
  timeouts, freshness).
- Los tests requieren avanzar o controlar el tiempo para verificar
  transiciones, umbrales o recuperacion.
- Usar wall-clock real introduciria sleeps, latencia o no determinismo.
- Timeout/recovery behavior necesita reproduccion precisa y repetible.

**Clock injection es innecesario cuando:**

- El sistema no tiene comportamiento temporal relevante.
- Los timestamps son datos pasivos sin decisiones basadas en elapsed time.
- No existen timeouts, watchdogs, ventanas de recuperacion ni logica
  programada.
- Anadir abstraccion no mejora testabilidad ni diseno.

**Cuando clock injection aplique:**

- Definir una abstraccion minima de tiempo (interfaz, protocolo o funcion)
  que exponga las operaciones temporales necesarias (e.g. tiempo
  monotono, timestamp UTC, avance controlado).
- Inyectar la fuente de tiempo unicamente en componentes que toman
  decisiones temporales. No envolver todo el codigo.
- Usar la fuente de tiempo real (wall-clock) en produccion.
- Usar una fuente controlada o fake en tests que permita avanzar el
  tiempo deterministicamente.
- Evitar llamadas dispersas directas al wall clock (`time.time()`,
  `time.monotonic()`) en logica de dominio. Centralizar el acceso al
  tiempo a traves de la abstraccion.
- Evitar sleeps reales en tests cuando el tiempo pueda controlarse
  mediante la abstraccion inyectada.
- Mantener ownership claro: un unico componente posee el estado temporal.
- Documentar unidades y semantica temporal: monotonico vs wall-clock,
  timezone, unidades de timestamp, unidades de timeout, reglas de
  freshness, ventanas de recuperacion, cadencia esperada.

**Proporcionalidad:**

- No imponer una clase concreta, Protocol concreto, nombres
  especificos, libreria, async, threads, scheduler framework ni
  dependency injection framework.
- La abstraccion debe ser la minima necesaria para testabilidad y
  determinismo.
- No exigir clock injection en proyectos sin comportamiento temporal
  relevante.
- Los requisitos temporales provienen de los contratos upstream
  (requirements, interface contracts, diagnostics contracts, approved
  designs). El Skill no inventa timeouts, thresholds ni valores
  concretos.

**Testabilidad temporal:**

Cuando exista logica temporal relevante, la estrategia de testing debe
contemplar evidencia para:

- Antes del umbral, en el umbral, despues del umbral.
- Transicion de timeout.
- Transicion de recuperacion.
- Comportamiento de eventos repetidos o consecutivos.
- Timestamps stale o future cuando aplique.

La seleccion de tests debe derivarse del contrato temporal real, no
imponer todos los casos a todos los proyectos. Favorecer tests
deterministicos, avance reproducible del tiempo, sin real waits cuando
sean evitables, y verificacion explicita de boundaries temporales.

## Required Outputs

Artefacto: `INDUSTRIAL_PYTHON_ENGINEERING.md`

Contenido obligatorio:

- Objetivo y contexto.
- Arquitectura de aplicacion.
- Estructura del proyecto.
- Componentes y responsabilidades.
- Contratos externos (a nivel de aplicacion, no de protocolo).
- Configuracion y secretos.
- Errores y excepciones.
- Logging.
- Lifecycle: startup, shutdown, cleanup.
- Concurrencia/async cuando aplique.
- Tipos y validacion de datos.
- Serializacion.
- Patrones de comunicaciones industriales (cliente, no contrato).
- Persistencia.
- Dependencias y packaging.
- Entornos.
- Testing.
- Simulacion.
- Observabilidad.
- Despliegue y rollback cuando aplique.
- Comportamiento ante fallos externos por interfaz (incluyendo stale data).
- Evaluacion de dependencia temporal y decision de clock injection cuando
  aplique.
- Riesgos.
- Decisiones abiertas.
- ADRs propuestos cuando aplique.

## Consumer

Engineering Architect (coherencia transversal), Software Engineer
(planificacion e implementacion), QA & Debug Engineer (testabilidad).

## Stop Condition

La skill se detiene cuando existe diseno de ingenieria Python suficiente para
permitir implementacion, testing, despliegue y diagnostico verificables. No
debe continuar hasta disenar cada funcion o clase.

## Gates Interaction

- **Precondicion**: Requirements Quality PASS. Decision Readiness PASS (si
  aplica).
- **Despues de**: el diseno de ingenieria se entrega a planificacion e
  implementacion. Implementation Review revisara la implementacion posterior.
- **No ejecuta**: Implementation Review, Final Verification ni ningun gate.
- **No reemplaza**: ADRs. Las decisiones de ingenieria dificiles de revertir
  se proponen como ADR.

## Agent Interaction

- **Activada por**: Software Engineer (owner).
- **Coordina con**: Industrial Automation Engineer (interfaces PLC), Robotics
  Engineer (interfaces robot), QA & Debug Engineer (testabilidad/observabilidad).
- **Handoff a**: Software Engineer para planificacion e implementacion.

## Evidence Required

- `INDUSTRIAL_PYTHON_ENGINEERING.md` con todos los campos obligatorios.
- Comportamiento ante fallos externos definido por interfaz (incluyendo stale
  data).
- Arquitectura de aplicacion, lifecycle y observabilidad definidos.
- Estrategia de testing y simulacion definida.
- Evaluacion de dependencia temporal documentada. Si clock injection
  aplica, abstraccion, ownership y semantica temporal definidos. Si no
  aplica, justificacion documentada.

## Failure Modes

- Ser una guia generica de Python sin especializacion industrial.
- Quedarse solo en estandares sin disenar arquitectura de aplicacion, lifecycle
  y comportamiento ante fallos.
- No definir comportamiento ante fallos externos (PLC, robot, vision, red,
  stale data).
- Duplicar contratos de comunicacion (responsabilidad de
  `industrial-communications-design`).
- Duplicar integracion de vision/IA (responsabilidad de
  `vision-ai-integration`).
- Duplicar arquitectura PLC o robotica interna.
- No definir lifecycle, startup, shutdown ni cleanup.
- No definir observabilidad ni alertas.
- Mezclar diseno de ingenieria con implementacion completa.
- Asumir entorno perfecto sin fallos de red ni servicios caidos.
- No evaluar dependencia temporal cuando el sistema tiene comportamiento
  dependiente del tiempo (watchdogs, timeouts, recovery, freshness).
- Usar wall-clock real directamente en logica de dominio cuando clock
  injection mejoraria testabilidad y determinismo.

## Escalation Rules

- Decision de arquitectura transversal -> Engineering Architect.
- Interface con PLC -> Industrial Automation Engineer.
- Interface con robot -> Robotics Engineer.
- Contrato de comunicaciones -> escalar a `industrial-communications-design`.
- Integracion de vision/IA -> escalar a `vision-ai-integration`.
- Testabilidad insuficiente -> QA & Debug Engineer.
- Arquitectura robotica interna -> escalar a `robotics-cell-integration`.
- Decision de ingenieria dificil de revertir -> proponer ADR.

## Done Criteria

- `INDUSTRIAL_PYTHON_ENGINEERING.md` completo con todos los campos obligatorios.
- Arquitectura de aplicacion, componentes y responsabilidades definidos.
- Lifecycle (startup, shutdown, cleanup) definido.
- Comportamiento ante fallos externos definido por interfaz (incluyendo stale
  data).
- Estandares de estructura, config, logging, excepciones, typing, testing,
  observabilidad y despliegue integrados en el diseno de ingenieria.
- Concurrencia/async definido cuando aplique.
- Simulacion y testing definidos.
- Dependencia temporal evaluada. Clock injection decidido y documentado.
- No duplica contratos de comunicacion, integracion de vision/IA, arquitectura
  PLC ni arquitectura robotica.
- Artefacto entregado a Software Engineer para planificacion.
