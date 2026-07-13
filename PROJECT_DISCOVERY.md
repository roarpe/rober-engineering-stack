# PROJECT_DISCOVERY.md

ROBER ENGINEERING STACK -- Project Discovery
Project: Industrial Robot Software Validation -- 6-axis pick-and-place (KUKA KRL)
Date: 2026-07-10
Owner: Engineering Architect
Skill: industrial-project-discovery

---

## 1. Objetivo del proyecto

Desarrollar el software de control para un robot industrial de 6 ejes que ejecuta
un ciclo automatico de pick-and-place en KUKA KRL, con arquitectura modular,
diagnosticos, recuperacion ante fallos y verificacion basada en evidencia.

**Clasificacion**: CONSTRAINT (objetivo definido por el usuario).

---

## 2. Problema operativo

Se requiere software de robot que ejecute un ciclo productivo de pick-and-place
de forma automatica, segura y diagnosticable. El software debe ser modular,
separando secuencia de produccion, logica de movimiento, control de gripper,
manejo de interfaces, diagnosticos y comportamiento de recuperacion.

El proyecto sirve ademas como ejercicio de validacion del Rober Engineering Stack
aplicado a robotica industrial en KRL.

**Clasificacion**: FACT.

---

## 3. Proceso fisico de alto nivel

```
  [Espera autorizacion]
         |
         v
  [Verificar condiciones operativas]
         |
         v
  [Mover a pick approach]
         |
         v
  [Mover a pick position]
         |
         v
  [Activar gripper]
         |
         v
  [Verificar agarre]
         |
         v
  [Retirar de pick area]
         |
         v
  [Mover a place approach]
         |
         v
  [Mover a place position]
         |
         v
  [Soltar pieza]
         |
         v
  [Verificar liberacion]
         |
         v
  [Retornar a posicion segura]
         |
         v
  [Reportar completitud de ciclo]
         |
         v
  [Espera autorizacion] (loop)
```

**Clasificacion**: FACT (secuencia definida por el usuario).

---

## 4. Stakeholders y usuarios

| Stakeholder | Rol | Clasificacion |
|---|---|---|
| Usuario (definidor del proyecto) | Define requisitos, restricciones y alcance | FACT |
| Engineering Architect | Coordina proyecto, ejecuta RQ y DR Gates | FACT (asignado por framework) |
| Robotics Engineer | Disena e implementa software del robot | FACT (asignado por framework) |
| QA & Debug Engineer | Verifica implementacion | FACT (asignado por framework) |
| Operador de produccion (implícito) | Autoriza ciclos, supervisa operacion | ASSUMPTION -- no explicitamente mencionado |
| Personal de mantenimiento (implícito) | Diagnostica fallos, ejecuta recuperacion | ASSUMPTION -- no explicitamente mencionado |

---

## 5. Modos de operacion y secuencia funcional

### Modos identificados

| Modo | Descripcion | Clasificacion |
|---|---|---|
| Produccion (auto) | Ejecuta ciclo automatico pick-and-place | FACT (requerido por usuario) |
| Diagnosticos | Inspecciona estado, senales, errores | FACT (requerido por usuario: "The robot must support production operation, diagnostics and recovery from failures") |
| Recuperacion | Responde a fallos, reset, restart | FACT (requerido por usuario) |
| Manual / mantenimiento | Movimiento manual, teaching, homing | ASSUMPTION -- no explicitamente requerido pero estandar en robotica industrial |
| Simulacion | Pruebas sin hardware real | ASSUMPTION -- necesario para verificacion pero no explicitamente requerido |

### Secuencia funcional

Ver seccion 3. La secuencia de 12 pasos esta definida por el usuario.

**Clasificacion**: FACT para secuencia; ASSUMPTION para modos no explicitos.

---

## 6. Equipos involucrados

| Equipo | En alcance | Clasificacion |
|---|---|---|
| Robot industrial 6 ejes (KUKA) | Si -- software del robot | FACT (KUKA KRL especificado) |
| Controlador KUKA | Si -- plataforma de ejecucion | UNKNOWN -- modelo exacto no especificado (KR C4, KR C5, Sunrise) |
| Gripper | Si -- controlado por robot via senales digitales | FACT (en alcance); UNKNOWN -- tipo y especificaciones |
| PLC | No -- fuera de alcance | CONSTRAINT (excluido por usuario) |
| Sistema de vision | No -- fuera de alcance | CONSTRAINT (excluido por usuario) |
| Conveyor | No -- fuera de alcance | CONSTRAINT (excluido por usuario) |
| Base de datos | No -- fuera de alcance | CONSTRAINT (excluido por usuario) |
| Software backend | No -- fuera de alcance | CONSTRAINT (excluido por usuario) |

**Interacciones externas**: "External interactions may be represented only through explicit interface contracts and simulated signals when required for robot software development and verification."

**Clasificacion**: CONSTRAINT para exclusiones; UNKNOWN para modelo de controlador.

---

## 7. Interfaces, senales y comunicaciones conocidas

### Interfaces identificadas desde requisitos

| Interface | Direccion | Tipo | Clasificacion |
|---|---|---|---|
| Autorizacion de ciclo | Externo → Robot | Digital signal (assumption) | UNKNOWN -- signal name, tipo, fuente no definidos |
| Control de gripper | Robot → Gripper | Digital signals | FACT -- "through digital signals"; UNKNOWN -- cuales senales, cuantas, encoding |
| Feedback de gripper | Gripper → Robot | Digital signal (assumption) | UNKNOWN -- existe sensor de agarre? que senal? |
| Reporte de completitud | Robot → Externo | Digital signal (assumption) | UNKNOWN -- signal name, tipo, destino no definidos |
| Condiciones operativas | Externo → Robot | Digital signals (assumption) | UNKNOWN -- que condiciones, cuantas senales |
| Diagnosticos | Robot → Externo | Unknown | UNKNOWN -- formato, destino, audiencia |

### Comunicaciones

No se especifica protocolo de comunicaciones. Las senales digitales son el
mecanismo implicito. No se menciona EtherNet/IP, Profinet, ni otro protocolo
industrial.

**Clasificacion**: UNKNOWN para la mayoria de interfaces; CONSTRAINT para
"explicit interface contracts and simulated signals only".

---

## 8. Restricciones

### Restricciones tecnicas

| Restriccion | Clasificacion |
|---|---|
| Lenguaje: KUKA KRL | CONSTRAINT |
| Arquitectura modular | CONSTRAINT |
| Separacion: produccion, motion, gripper, interfaces, diagnosticos, recuperacion | CONSTRAINT |
| Ownership explicito | CONSTRAINT |
| Contratos de ingenieria formales | CONSTRAINT |
| Reviews basados en evidencia | CONSTRAINT |
| Ingenieria proporcional | CONSTRAINT |
| Handoffs explicitos | CONSTRAINT |
| No scope creep | CONSTRAINT |
| Interfaces externas solo mediante contratos explicitos y senales simuladas | CONSTRAINT |
| No implementar PLC, vision, Python, base de datos | CONSTRAINT |
| No modificar el framework durante el proyecto | CONSTRAINT |

### Restricciones operativas

| Restriccion | Clasificacion |
|---|---|
| No iniciar ciclo sin autorizacion | CONSTRAINT |
| Usar posiciones de aproximacion antes de pick y place | CONSTRAINT |
| Prevenir ejecucion duplicada de ciclo | CONSTRAINT |
| Retornar a estado seguro cuando se requiera | CONSTRAINT |

### Restricciones de plazos

No se especifican plazos.

**Clasificacion**: UNKNOWN.

### Restricciones de entorno

No se especifica entorno de despliegue (fabrica, laboratorio, celda de pruebas).

**Clasificacion**: UNKNOWN.

---

## 9. Entorno de ejecucion, disponibilidad y mantenimiento

| Aspecto | Valor | Clasificacion |
|---|---|---|
| Controlador KUKA | No especificado | UNKNOWN -- KR C4 / KR C5 / Sunrise afecta KRL features, safety, motion |
| KRL version | No especificada | UNKNOWN -- KSS version afecta sintaxis y features disponibles |
| Simulador | No especificado | UNKNOWN -- KUKA Sim Pro, Office Lite, HIL, puro |
| Disponibilidad requerida | No especificada | UNKNOWN |
| Mantenimiento | No especificado | UNKNOWN |

---

## 10. Requisitos de diagnostico y recuperacion

### Diagnosticos

| Requisito | Clasificacion |
|---|---|
| "The robot shall detect relevant execution failures" | FACT -- requerido; UNKNOWN -- que fallos son "relevantes" |
| "The robot shall provide useful diagnostics" | FACT -- requerido; UNKNOWN -- que es "util", formato, audiencia |

### Recuperacion

| Requisito | Clasificacion |
|---|---|
| "The robot shall support recovery from failures when appropriate" | FACT -- requerido; UNKNOWN -- estrategias, condiciones |
| "The robot shall return to a defined safe state when required" | FACT -- requerido; UNKNOWN -- que estado, que trigger |

### Fallos potencialmente relevantes (clarificados por usuario 2026-07-10)

**Fallos relevantes requeridos a nivel de proyecto**:

| Fallo | Clasificacion |
|---|---|
| Fallo de agarre (gripper no confirma) | FACT -- confirmado por usuario como relevante |
| Fallo de liberacion (pieza no soltada) | FACT -- confirmado por usuario como relevante |
| Perdida o invalidacion de autorizacion de ciclo | FACT -- confirmado por usuario como relevante |
| Condicion operativa requerida no satisfecha antes del inicio | FACT -- confirmado por usuario como relevante |
| Estado interno de ciclo invalido o inesperado | FACT -- confirmado por usuario como relevante |

**Fallos NO requeridos como requisitos a nivel de proyecto en esta etapa**:

| Fallo | Clasificacion |
|---|---|
| Fallos de movimiento del controlador | EXCLUDED -- fuera de scope de software del proyecto |
| Colisiones | EXCLUDED -- fuera de scope de software del proyecto |
| Activacion de parada de emergencia | EXCLUDED -- fuera de scope de software del proyecto |
| Fallos del sistema de seguridad | EXCLUDED -- fuera de scope de software del proyecto |
| Desviacion de posicion fisica | EXCLUDED -- fuera de scope de software del proyecto |
| Perdida de comunicacion con sistemas externos | EXCLUDED -- fuera de scope de software del proyecto |
| Timeout de ciclo | EXCLUDED -- fuera de scope de software del proyecto |

**Nota**: Estas exclusiones significan que el manejo de estos fallos esta fuera del alcance del software del proyecto a menos que una decision de ingenieria posterior demuestre que se requiere manejo explicito a nivel de aplicacion KRL. No significan que el controlador del robot o el sistema de seguridad deban ignorar tales condiciones.

---

## 11. Criterios de aceptacion (aprobados por usuario)

Criterios de aceptacion derivados de la informacion del proyecto y aprobados
por el usuario el 2026-07-10. Ver `ROBOT_REQUIREMENTS_CLARIFICATION.md` para
el analisis detallado de derivacion.

| ID | Requisito | Criterio de aceptacion | Estado |
|---|---|---|---|
| R01 | Ejecutar ciclo automatico pick-and-place | El software del robot ejecutara la secuencia completa de 12 pasos (seccion 3) desde [Espera autorizacion] hasta [Reportar completitud de ciclo] y retornara a [Espera autorizacion], sin omitir ni reordenar pasos. | APROBADO |
| R02 | No iniciar ciclo sin autorizacion | El software del robot no transitara del estado de espera al estado de verificacion de condiciones a menos que una senal de autorizacion este presente. | APROBADO |
| R03 | Usar posiciones de aproximacion | El software del robot movera a una posicion de aproximacion antes de mover a la posicion de pick (paso 3 a paso 4), y movera a una posicion de aproximacion antes de mover a la posicion de place (paso 7 a paso 8). | APROBADO |
| R04 | Controlar gripper via senales digitales | El software del robot activara el gripper via senal(es) de salida digital en el paso 5 y desactivara el gripper via senal(es) de salida digital en el paso 9. | APROBADO |
| R05 | Verificar agarre | El software del robot verificara que el gripper ha agarrado la pieza antes de proceder del paso 6 al paso 7. Si el agarre no se confirma, el robot no procedera al paso 7 y transitara a un estado de manejo de fallos. | APROBADO |
| R06 | Verificar liberacion | El software del robot verificara que la pieza ha sido liberada antes de proceder del paso 10 al paso 11. Si la liberacion no se confirma, el robot no procedera al paso 11 y transitara a un estado de manejo de fallos. | APROBADO |
| R07 | Detectar fallos relevantes | El software del robot detectara los siguientes fallos de ejecucion relevantes: (a) fallo de agarre, (b) fallo de liberacion, (c) autorizacion de ciclo perdida o invalida cuando se evalue segun el contrato final de autorizacion, (d) condicion operativa requerida no satisfecha antes del inicio del ciclo, (e) estado interno de ciclo invalido o inesperado. Al detectar un fallo, el robot transitara a un estado diagnostico en lugar de continuar el ciclo. Los siguientes fallos NO son requisitos a nivel de proyecto en esta etapa: fallos de movimiento del controlador, colisiones, parada de emergencia, fallos del sistema de seguridad, desviacion de posicion fisica, perdida de comunicacion con sistemas externos, timeout de ciclo. Estas exclusiones significan que el manejo de estos fallos esta fuera del alcance del software del proyecto a menos que una decision de ingenieria posterior demuestre que se requiere manejo explicito a nivel de aplicacion KRL. | APROBADO (clarificado por usuario) |
| R08 | Proporcionar diagnosticos utiles | El software del robot registrara y pondra a disposicion informacion diagnostica cuando se detecte un fallo. La informacion diagnostica identificara como minimo: (a) el paso o estado actual de la secuencia de produccion, (b) el tipo de fallo detectado, (c) si se requiere intervencion del operador o mantenimiento, (d) si la recuperacion esta disponible segun la estrategia final de recuperacion. Los diagnosticos estan destinados principalmente a personal de mantenimiento e ingenieria. No se requiere timestamp. No se requiere modelo de niveles de severidad. No se requiere HMI externo, base de datos, sistema de logging o protocolo de comunicacion. La representacion final en KRL se determinara durante arquitectura e implementacion. | APROBADO (clarificado por usuario) |
| R09 | Soportar recuperacion | The KRL application shall support recovery from application-level failures per the D009 recovery strategy: (a) maximum one automatic gripping retry per production cycle with sequence: record diagnostic, open gripper, verify open, re-grip, verify grip; (b) maximum one automatic release retry per production cycle with sequence: record diagnostic, re-open, verify release, no robot motion; (c) if retry fails, cycle terminates unsuccessfully, CYCLE_COMPLETE remains inactive, application enters SAFE_IDLE, diagnostics preserved; (d) no unlimited retry; (e) no automatic restart from SAFE_IDLE; (f) leaving SAFE_IDLE requires RECOVERY_RESET; (g) invalid internal cycle state: no auto recovery, enter SAFE_IDLE; (h) invalid pre-cycle conditions: cycle not started, request not consumed, return to waiting. | APROBADO (DR Gate V2) |
| R10 | Prevenir duplicacion de ciclo | El software del robot no iniciara un nuevo ciclo mientras un ciclo este en progreso. El software del robot no ejecutara mas de un ciclo por senal de autorizacion. | APROBADO |
| R11 | Retornar a estado seguro | The KRL application shall enter SAFE_IDLE when application-level logic determines that normal cycle execution cannot continue and no immediate automatic recovery action is authorized: (a) SAFE_IDLE is an application-level state, not a safety-rated state; (b) in SAFE_IDLE: no cycle active, no new cycle may start, no recovery active, no automatic motion, no gripper actuation, diagnostics preserved; (c) explicit authorization (RECOVERY_RESET) required to leave SAFE_IDLE; (d) SAFE_IDLE shall not replace emergency stop, protective stop, controller safety functions, or external safety architecture; (e) entry into SAFE_IDLE shall not automatically command movement; (f) physical robot position and application state are separate concepts. | APROBADO (DR Gate V2) |
| R12 | Arquitectura modular | El software del robot estara estructurado en los seis modulos especificados: (1) secuencia de produccion, (2) logica de movimiento, (3) control de gripper, (4) manejo de interfaces, (5) diagnosticos, (6) comportamiento de recuperacion. Cada modulo tendra ownership explicito e interfaces definidas a otros modulos. | APROBADO |

**Resumen**: 12 criterios aprobados (R01-R12). R09 y R11 aprobados durante DR Gate V2 tras resolucion de D009 y D010.

---

## 12. Riesgos e incertidumbres

| Riesgo | Clasificacion | Impacto |
|---|---|---|
| Modelo de robot/controlador desconocido | UNKNOWN | HIGH -- afecta motion, safety, KRL features |
| Especificaciones de gripper desconocidas | UNKNOWN | HIGH -- afecta control y verificacion |
| Posiciones y frames no definidos | UNKNOWN | MEDIUM -- pueden definirse durante arquitectura |
| Criterios de aceptacion: 10 aprobados, 2 bloqueados | PARTIALLY RESOLVED | MEDIUM -- R09 y R11 bloqueados por D009/D010 |
| Arquitectura de seguridad no definida | DECISION NEEDED | HIGH -- bloqueante para arquitectura |
| Entorno de simulacion no definido | DECISION NEEDED | MEDIUM -- bloqueante para planificacion de verificacion |
| Sin plazos | UNKNOWN | LOW -- no bloqueante para ingenieria |
| Framework puede carecer de skill para arquitectura de software robot en KRL | UNKNOWN | MEDIUM -- ver VL-023; determinar durante fases posteriores |
| Alcance de `robotics-cell-integration` con PLC fuera de alcance | UNKNOWN | LOW -- la skill puede aplicar parcialmente |

---

## 13. Decisiones abiertas

### DECISION RESOLVED -- D001: Modelo de robot y controlador KUKA

| Campo | Valor |
|---|---|
| Question | Que modelo de robot KUKA y controlador se utilizan? |
| Context | El modelo determina capacidades de movimiento, KRL features disponibles, safety features, y entorno de simulacion compatible. KR C4 vs KR C5 tienen diferentes KSS versions y safety integrations. |
| Options | (a) KR C4 con KSS 8.x, (b) KR C5 con KSS 8.x/9.x, (c) Sunrise controller, (d) otro |
| Missing info | ~~Modelo exacto de robot (KR...), modelo de controlador, KSS version~~ -- RESOLVED |
| Dependencies | D002 (simulacion), D003 (safety) -- now unblocked for resolution |
| Risk | HIGH -- diseno de motion y safety dependen del controlador |
| Reversibility | Dificil de revertir una vez implementado |
| Owner | Project Owner |
| Resolution method | user decision |
| Status | **RESOLVED** -- 2026-07-10 |
| Blocking? | ~~BLOCKING~~ -- **RESOLVED** |
| Latest phase to resolve | **Decision Readiness Gate** (resolved during Phase 1) |
| Resolution | Robot model: KUKA KR 6 R900 sixx; Controller: KR C4; KSS version: KSS 8.3. Standard KRL development for KR C4. No optional technology packages assumed unless explicitly authorized by later engineering decision. |
| Evidence | ADR-0001 (docs/decisions/ADR-0001-robot-model-and-controller.md) |
| Validation log | VL-075 |

### DECISION RESOLVED -- D002: Entorno de simulacion y verificacion

| Campo | Valor |
|---|---|
| Question | Como se verificara el software del robot? |
| Context | La estrategia de verificacion afecta la arquitectura (testabilidad), los criterios de aceptacion, y el plan de implementacion. KUKA Sim Pro permite simulacion 3D. Office Lite permite ejecutar KRL en PC. HIL requiere hardware. |
| Options | (a) KUKA Sim Pro + Office Lite, (b) Office Lite solo, (c) HIL con controlador real, (d) simulacion pura sin KUKA tools, (e) combinacion |
| Missing info | ~~Disponibilidad de herramientas, presupuesto, hardware~~ -- RESOLVED |
| Dependencies | ~~D001 (modelo de controlador)~~ -- D001 RESOLVED |
| Risk | MEDIUM -- afecta plan de verificacion pero no arquitectura central |
| Reversibility | Reversible con costo |
| Owner | Project Owner |
| Resolution method | user decision |
| Status | **RESOLVED** -- 2026-07-10 |
| Blocking? | ~~BLOCKING~~ -- **RESOLVED** |
| Latest phase to resolve | **Decision Readiness Gate** (resolved during Phase 2) |
| Resolution | KUKA.Sim for robot-cell simulation and offline validation. KUKA OfficeLite compatible with KR C4 / KSS 8.3 for KRL execution and software-level verification. No physical robot hardware available. No HIL environment available. No production deployment in scope. Verification strategy must distinguish: (1) evidence obtainable through software execution/controller simulation, (2) evidence obtainable through robot-cell simulation, (3) evidence requiring physical hardware (cannot be produced). Absence of physical hardware shall not be hidden. Requirements that cannot be fully verified without physical hardware must report verification limitations. No optional KUKA technology packages assumed. |
| Evidence | Documented Project Owner decision (VALIDATION_LOG.md VL-081). ADR not required per proportionality: MEDIUM risk, reversible with cost, framework allows documented user decision as evidence. |
| Validation log | VL-081 |

### DECISION RESOLVED -- D003: Arquitectura de seguridad

| Campo | Valor |
|---|---|
| Question | Que arquitectura de seguridad se aplica al robot? |
| Context | "Retornar a estado seguro" requiere definir que es seguro y como se implementa. KUKA ofrece safety features (SOS, SBC, SLP, safe monitoring) que dependen del controlador y configuracion. Si hay un safety controller externo (PLC de seguridad), el robot debe integrarse con el. |
| Options | (a) Safety integrada en controlador KUKA (safe operation stop, safe monitoring), (b) Safety controller externo (PLC de seguridad), (c) Sin safety architecture dedicada (solo E-stop estandar), (d) Combinacion |
| Missing info | ~~Configuracion de seguridad actual, presencia de PLC de seguridad, requisitos normativos~~ -- RESOLVED |
| Dependencies | ~~D001 (modelo de controlador)~~ -- D001 RESOLVED |
| Risk | HIGH -- seguridad es critica en robotica industrial |
| Reversibility | Dificil de revertir |
| Owner | Project Owner + Safety Specialist |
| Resolution method | user decision + specialist consultation |
| Status | **RESOLVED** -- 2026-07-10 |
| Blocking? | ~~BLOCKING~~ -- **RESOLVED** |
| Latest phase to resolve | **Decision Readiness Gate** (resolved during Phase 2) |
| Resolution | Safety-rated functions are outside implementation scope. KRL application shall not implement, emulate, replace, or claim responsibility for safety-rated functions. Explicit boundary maintained between: (1) safety-rated robot/controller functions, (2) external safety architecture, (3) application-level KRL state and error handling. Emergency stop, protective stop, safety-rated motion monitoring, safety I/O config, safety PLC, SafeOperation config -- all outside project scope. KRL application may: detect application-level operating conditions, enter defined application states, stop/inhibit production sequence per normal logic, expose diagnostics, require authorization before restart. KRL application shall not: bypass controller safety, auto-recover from safety-rated stops, auto-restart after safety event, claim application-level safe state equals safety-rated state. Application-level recovery shall never be described as safety-rated. Safety Specialist confirms scope boundary sufficient for validation project. This decision does NOT constitute safety assessment, risk assessment, CE conformity, or production safety design. Future physical deployment requires independent safety engineering. |
| Evidence | ADR-0002 (docs/decisions/ADR-0002-safety-architecture-boundary.md). ADR warranted: HIGH risk, difficult to reverse, real alternatives, future agent could reopen without context. Safety Specialist consultation confirmed. |
| Validation log | VL-082 |

### DECISION RESOLVED -- D004: Especificaciones de gripper y pieza

| Campo | Valor |
|---|---|
| Question | Que gripper se utiliza y que pieza se manipula? |
| Context | El tipo de gripper (neumatico, electrico, magnetico), numero de senales, presencia de sensor de agarre, dimensiones y peso de la pieza afectan el control del gripper y la verificacion de agarre/liberacion. |
| Options | (a) Gripper neumatico con sensor de agarre, (b) Gripper neumatico sin sensor, (c) Gripper electrico, (d) Gripper magnetico, (e) otro |
| Missing info | ~~Tipo de gripper, senales disponibles, especificaciones de pieza~~ -- RESOLVED |
| Dependencies | Ninguna |
| Risk | MEDIUM -- afecta control y verificacion pero no arquitectura general |
| Reversibility | Reversible |
| Owner | Project Owner |
| Resolution method | user decision |
| Status | **RESOLVED** -- 2026-07-10 |
| Blocking? | ~~BLOCKING~~ -- **RESOLVED** |
| Latest phase to resolve | **Decision Readiness Gate** (resolved during Phase 1) |
| Resolution | Gripper: pneumatic parallel gripper, pneumatic cylinder actuation. Control: 2 digital outputs (OPEN, CLOSE). Feedback: 3 digital inputs (GRIPPER_OPEN, GRIPPER_CLOSED, PART_PRESENT). Part: rigid rectangular industrial component, 100mm x 60mm x 40mm, 0.5 kg, rigid surface, non-fragile, no special orientation constraints. Handling: no leave pick until gripping confirmed (GRIPPER_CLOSED + PART_PRESENT active); no report release until gripper open confirmed and PART_PRESENT inactive. Signal names are functional identifiers only; final KRL I/O mapping during architecture/implementation. No pneumatic pressure assumed. No gripping force assumed. No additional sensors assumed. No analog signals assumed. |
| Evidence | Documented Project Owner decision (VALIDATION_LOG.md VL-076). ADR not required per proportionality: MEDIUM risk, reversible, framework allows documented user decision as evidence. |
| Validation log | VL-076 |

### DECISION RESOLVED -- D005: Definicion de "condiciones operativas"

| Campo | Valor |
|---|---|
| Question | Que condiciones operativas deben verificarse antes de iniciar un ciclo? |
| Context | El paso 1 del ciclo es "verifies that the required operating conditions are satisfied". Sin saber que condiciones, no se puede disenar la logica de verificacion ni los criterios de aceptacion. |
| Options | (a) Solo senales del propio robot (gripper, posicion), (b) Senales externas (PLC ready, conveyor ready, safety OK), (c) Combinacion |
| Missing info | ~~Lista de condiciones, senales asociadas, fuente de cada una~~ -- RESOLVED |
| Dependencies | ~~D003 (safety)~~ -- D003 RESOLVED, ~~D004 (gripper)~~ -- D004 RESOLVED |
| Risk | MEDIUM -- afecta inicio de ciclo pero no arquitectura completa |
| Reversibility | Reversible |
| Owner | Project Owner |
| Resolution method | user decision |
| Status | **RESOLVED** -- 2026-07-10 |
| Blocking? | ~~BLOCKING~~ -- **RESOLVED** |
| Latest phase to resolve | **Decision Readiness Gate** (resolved during Phase 3) |
| Resolution | Application-level operating conditions verified before cycle start: (1) robot in IDLE state, (2) no application-level fault active, (3) no recovery sequence active, (4) no previous cycle active/incomplete, (5) gripper confirmed open via GRIPPER_OPEN, (6) gripper not confirmed closed via GRIPPER_CLOSED, (7) no part detected via PART_PRESENT, (8) valid cycle authorization per D006 contract. Cycle start inhibited if any condition not satisfied. Application provides diagnostic evidence identifying the preventing condition. Safety-rated conditions outside this contract. KRL shall not duplicate/emulate/replace controller or external safety checks. Physical robot position not mandatory cycle-start condition at this stage unless architecture demonstrates requirement. |
| Evidence | Documented Project Owner decision (VALIDATION_LOG.md VL-088). ADR not required per proportionality: MEDIUM risk, reversible, framework allows documented user decision as evidence. |
| Validation log | VL-088 |

### DECISION RESOLVED -- D006: Interface de autorizacion de ciclo

| Campo | Valor |
|---|---|
| Question | Como se autoriza un ciclo y como se previene la duplicacion? |
| Context | "The robot waits for authorization to begin a cycle" y "shall prevent unintended duplicate cycle execution". El mecanismo (signal edge, handshake, command from HMI) afecta el diseno de la maquina de estados y la interface. |
| Options | (a) Signal edge detection (rising edge de senal digital), (b) Handshake bidireccional (request/ack), (c) Comando desde HMI/software, (d) Combinacion |
| Missing info | ~~Fuente de autorizacion, tipo de signal, mecanismo anti-duplicacion~~ -- RESOLVED |
| Dependencies | ~~D001 (controlador)~~ -- D001 RESOLVED, ~~D005 (condiciones)~~ -- D005 RESOLVED |
| Risk | MEDIUM -- afecta maquina de estados pero no arquitectura completa |
| Reversibility | Reversible |
| Owner | Project Owner |
| Resolution method | user decision |
| Status | **RESOLVED** -- 2026-07-10 |
| Blocking? | ~~BLOCKING~~ -- **RESOLVED** |
| Latest phase to resolve | **Decision Readiness Gate** (resolved during Phase 4) |
| Resolution | Application-level digital handshake: CYCLE_REQUEST + CYCLE_COMPLETE. Signal names are functional identifiers only; final KRL I/O mapping during architecture/implementation. Authorization contract: new cycle accepted only when all D005 conditions satisfied, CYCLE_REQUEST active, request not consumed, not waiting for previous request clearing. On acceptance: request marked consumed, exactly one cycle initiated, continued CYCLE_REQUEST activation does not cause additional cycles. After successful completion: CYCLE_COMPLETE active, wait for CYCLE_REQUEST inactive, then rearm, then CYCLE_COMPLETE cleared. Anti-duplication: internal request-consumption state, mandatory request clearing before rearming, one accepted request = at most one cycle. Continuously active CYCLE_REQUEST never causes repeated cycles. Request not accepted while: cycle active, recovery active, fault active, SAFE_IDLE, previous request consumed and not rearmed. Abnormal: CYCLE_REQUEST inactive after acceptance but before completion does not abort cycle; accepted request remains consumed; cycle continues unless other failure. Unsuccessful cycle: request remains consumed, no auto-retry, no CYCLE_COMPLETE, subsequent behavior per D009. No automatic retry authorized by D006. Scope: defines application-level authorization and anti-duplication contract only. Does NOT define: PLC, HMI, external protocols, safety-rated authorization, automatic recovery, KRL state-machine details, physical I/O addresses. |
| Evidence | Documented Project Owner decision (VALIDATION_LOG.md VL-095). ADR not required per proportionality: MEDIUM risk, reversible, framework allows documented user decision as evidence. |
| Validation log | VL-095 |

### DECISION NEEDED -- D007: Criterios de aceptacion

| Campo | Valor |
|---|---|
| Question | Que criterios de aceptacion definen el exito de cada requisito? |
| Context | Ningun requisito tiene criterios de aceptacion. RQ Gate requiere "criterios de aceptacion para cada objetivo". Sin criterios, el gate no puede PASS. |
| Options | (a) Criterios funcionales (ciclo completo correctamente), (b) Criterios de rendimiento (tiempo de ciclo, precision), (c) Criterios de seguridad (safe state alcanzado en X ms), (d) Combinacion |
| Missing info | Definicion de exito para cada requisito, tolerancias, evidencia requerida |
| Dependencies | D001-D006 (todas las decisiones afectan los criterios) |
| Risk | HIGH -- sin criterios no hay verificacion posible |
| Reversibility | Reversible |
| Owner | Usuario con Engineering Architect |
| Resolution method | user decision + specialist consultation |
| Status | Open |
| Blocking? | **BLOCKING** -- debe resolverse antes de RQ Gate PASS |
| Latest phase to resolve | **Requirements Quality Gate** (antes de PASS) |

### DECISION RESOLVED -- D008: Estrategia de diagnosticos

| Campo | Valor |
|---|---|
| Question | Que diagnosticos se requieren, en que formato y para que audiencia? |
| Context | "Useful diagnostics" es subjetivo sin definicion. Los diagnosticos pueden ser variables de sistema KUKA, mensajes al HMI, senales digitales de estado, o logs estructurados. |
| Options | (a) Variables KUKA + mensajes HMI, (b) Senales digitales de estado/error, (c) Logs estructurados, (d) Combinacion |
| Missing info | ~~Audiencia, formato, severidad, conjunto de fallos~~ -- RESOLVED |
| Dependencies | D003 (safety) -- RESOLVED, D005 (condiciones) -- RESOLVED |
| Risk | LOW-MEDIUM -- afecta diseno de diagnostico pero no arquitectura central |
| Reversibility | Reversible |
| Owner | Usuario con Robotics Engineer |
| Resolution method | engineering decision during architecture |
| Status | **RESOLVED** -- 2026-07-10 (Architecture phase) |
| Blocking? | ~~NON-BLOCKING~~ -- **RESOLVED** |
| Latest phase to resolve | **Arquitectura** (resolved during Architecture phase) |
| Resolution | Application-level diagnostics via KRL variables in diag.src/diag.dat. No external HMI, database, or logging protocol. R08 acceptance criterion defines minimum content: (a) step/state, (b) failure type, (c) intervention required, (d) recovery available. Diagnostics preserved across state transitions, cleared only during RECOVERY_RESET. 7 failure type codes defined. Accessible via KRL variable inspection in OfficeLite/simulation. |
| Evidence | Documented engineering decision (VALIDATION_LOG.md VL-118). ROBOT_SOFTWARE_ARCHITECTURE.md section 9. ADR not required: LOW-MEDIUM risk, reversible, framework allows documented engineering decision. |
| Validation log | VL-118 |

### DECISION RESOLVED -- D009: Estrategia de recuperacion

| Campo | Valor |
|---|---|
| Question | Que estrategias de recuperacion aplican y bajo que condiciones? |
| Context | "Recovery from failures when appropriate" requiere definir que recuperaciones son automaticas vs manuales, que fallos las disparan, y que secuencia de recuperacion sigue el robot. El usuario exige separacion arquitectural explicita de "recovery behavior" como uno de los seis modulos del software. La estrategia de recuperacion determina los estados de error/recovery en la maquina de estados, las transiciones de recovery, y la estructura del modulo de recovery. Sin esta decision, la arquitectura del software del robot no puede definir la maquina de estados completa ni el modulo de recovery. |
| Options | (a) Auto-retry N veces luego de error, (b) Reset manual siempre, (c) Homing + restart automatico, (d) Combinacion por tipo de fallo |
| Missing info | ~~Tipos de fallo, politicas de retry, condiciones de "when appropriate"~~ -- RESOLVED |
| Dependencies | ~~D003 (safety)~~ -- D003 RESOLVED, ~~D004 (gripper)~~ -- D004 RESOLVED, ~~D005 (condiciones)~~ -- D005 RESOLVED, ~~D010 (safe state)~~ -- D010 RESOLVED |
| Risk | MEDIUM -- afecta maquina de estados y comportamiento ante fallos |
| Reversibility | Reversible |
| Owner | Project Owner + Robotics Engineer |
| Resolution method | user decision + specialist consultation |
| Status | **RESOLVED** -- 2026-07-10 |
| Blocking? | ~~BLOCKING~~ -- **RESOLVED** |
| Latest phase to resolve | **Decision Readiness Gate** (resolved during Phase 5) |
| Resolution | Application-level recovery only (D003 scope). Distinguishes recoverable vs non-recoverable application-level failures. Automatic recovery limited, deterministic, explicitly defined. No unlimited retry. No auto-restart from SAFE_IDLE. Failed cycle never reports CYCLE_COMPLETE. Accepted CYCLE_REQUEST remains consumed after unsuccessful cycle. Recovery preserves diagnostics. Gripping failure: max 1 auto retry per cycle (open, verify open, re-grip, verify grip). Retry success: cycle continues, same consumed request. Retry fail: cycle terminates unsuccessfully, no CYCLE_COMPLETE, enter SAFE_IDLE, diagnostics preserved. Release failure: max 1 auto retry per cycle (re-open, verify release). No robot motion during release retry. Retry success: cycle completes, CYCLE_COMPLETE per D006. Retry fail: cycle terminates, no CYCLE_COMPLETE, enter SAFE_IDLE, diagnostics preserved. Invalid pre-cycle conditions: cycle not started, request not consumed, return to waiting state, diagnostics on failed condition. No SAFE_IDLE entry unless independent failure. Invalid internal cycle state: no auto recovery, no motion, no gripper actuation, cycle terminates unsuccessfully, no CYCLE_COMPLETE, request remains consumed if accepted, diagnostics preserved, enter SAFE_IDLE. Leaving SAFE_IDLE: no auto-leave. Requires RECOVERY_RESET signal (functional identifier only). Valid RECOVERY_RESET only when: no recovery active, no auto motion, no gripper actuation, conditions evaluated, previous CYCLE_REQUEST inactive. After valid reset: clear fault, clear recovery state, rearm request consumption, return to IDLE, acknowledge/archive diagnostics. Recovery reset shall NOT: auto-start cycle, auto-execute motion, auto-actuate gripper, bypass D005/D006, bypass safety. New cycle requires new D006 authorization. Retry state: internal state ensures max 1 grip retry + 1 release retry per cycle. KRL representation during architecture. Scope: application-level recovery only. Does NOT define: safety-rated recovery, controller fault recovery, external safety reset, auto-recovery from E-stop/protective stop, collision recovery, maintenance, production restart after safety events. |
| Evidence | Documented Project Owner decision (VALIDATION_LOG.md VL-101). ADR not required per proportionality: MEDIUM risk, reversible per original classification, framework allows documented user decision as evidence. Recovery strategy is behavioral (retry counts, sequences), not structural — modifiable without architectural redesign. |
| Validation log | VL-101 |
| Correction rationale | Originalmente clasificado como NON-BLOCKING (deferible a arquitectura). Corregido: la estrategia de recuperacion afecta materialmente la arquitectura del software del robot, el diseno de la maquina de estados y el manejo de fallos. El usuario exige separacion modular explicita de recovery behavior. No se puede crear arquitectura sin conocer las estrategias de recuperacion. |

### DECISION RESOLVED -- D010: Definicion de "safe state"

| Campo | Valor |
|---|---|
| Question | Cual es el "defined safe state" del robot? |
| Context | "Return to a defined safe state when required" -- el safe state puede ser una posicion fisica, un estado de la maquina de estados, o ambos. "When required" no esta definido. El safe state es un elemento de la maquina de estados que debe existir antes de disenar la arquitectura. Esta directamente relacionado con D003 (Safety Architecture) que define el sistema de seguridad, y con D009 (Recovery Strategy) que define como el robot se recupera -- la recuperacion frecuentemente implica retornar al safe state. Sin esta decision, la maquina de estados no puede disenarse porque falta un estado clave, y el modulo de recovery no puede definirse porque no se conoce el estado objetivo de recuperacion. |
| Options | (a) Posicion de espera segura (HOME/safe pose), (b) Estado de maquina IDLE/SAFE, (c) Combinacion (posicion + estado), (d) Stop de movimiento inmediato |
| Missing info | ~~Posicion segura definida, trigger para "when required", relacion con safety architecture~~ -- RESOLVED |
| Dependencies | ~~D003 (safety)~~ -- D003 RESOLVED, ~~D001 (modelo de robot)~~ -- D001 RESOLVED |
| Risk | HIGH -- afecta comportamiento de seguridad y maquina de estados (upgraded from MEDIUM based on architectural significance and difficulty of reversal) |
| Reversibility | Dificil de revertir -- state machine designed around SAFE_IDLE |
| Owner | Project Owner + Robotics Engineer + Safety Specialist |
| Resolution method | user decision + specialist consultation |
| Status | **RESOLVED** -- 2026-07-10 |
| Blocking? | ~~BLOCKING~~ -- **RESOLVED** |
| Latest phase to resolve | **Decision Readiness Gate** (resolved during Phase 3) |
| Resolution | Application-level safe state = SAFE_IDLE. Not a safety-rated state. In SAFE_IDLE: no cycle active, no new cycle may start, no recovery active, no automatic motion command, no gripper actuation, diagnostics preserved, explicit authorization required to leave. Entry when normal cycle cannot continue and no immediate automatic recovery authorized by D009. SAFE_IDLE shall NOT: be safety-rated, replace E-stop/protective stop/controller safety/external safety, guarantee physical position. Physical position and application state are separate. Physical home/recovery position may be defined during architecture. Entry into SAFE_IDLE shall not command movement. Robotics Engineer confirms sufficient for state-machine target. Safety Specialist confirms distinction preserves D003 boundary. |
| Evidence | ADR-0003 (docs/decisions/ADR-0003-application-level-safe-state.md). ADR warranted: HIGH risk, difficult to reverse (state machine designed around it), real alternatives, future agent could confuse SAFE_IDLE with safety-rated state. |
| Validation log | VL-090 |
| Correction rationale | Originalmente clasificado como NON-BLOCKING (deferible a arquitectura). Corregido: el safe state es un elemento de la maquina de estados requerido antes de crear la arquitectura. D009 (Recovery) depende de D010 (Safe State). D003 (Safety) esta relacionado. Sin safe state definido, la arquitectura no puede proceder. |

---

## 14. Clasificacion FACT/ASSUMPTION/UNKNOWN/CONSTRAINT/DECISION NEEDED

### Resumen de clasificacion

| Clasificacion | Cantidad | Items |
|---|---|---|
| FACT | 13 | Objetivo, problema, secuencia de 12 pasos, modos produccion/diagnostico/recuperacion, KUKA KRL, gripper via senales digitales, exclusiones de scope, stakeholders framework, posiciones arquitecturales (U014a: pick approach, pick, place approach, place, safe wait -- conocidas desde la secuencia del ciclo) |
| ASSUMPTION | 5 | Operador implicito, mantenimiento implicito, modo manual, modo simulacion, fallos potencialmente relevantes (8 tipos listados) |
| UNKNOWN | 19 (U001-U013, U014b, U015-U018) | Modelo de controlador, KRL version, simulador, disponibilidad, mantenimiento, plazos, entorno, 6 interfaces sin definir, valores fisicos de posiciones, ciclo tiempo, especificaciones de pieza, criterios de aceptacion (todos). U014a reclasificado como FACT (posiciones conocidas desde secuencia del ciclo). |
| CONSTRAINT | 14 | KUKA KRL, modular, separacion de responsabilidades, ownership explicito, contratos formales, evidencia, proporcionalidad, handoffs, no scope creep, interfaces externas solo contratos, no PLC/vision/Python/DB, no modificar framework, no iniciar sin autorizacion, posiciones de aproximacion, prevenir duplicacion, retornar a seguro |
| DECISION NEEDED | 10 total -- **10 RESOLVED** (D001-D010, all resolved including D008 during Architecture phase) |

### Items UNKNOWN con explicacion, blocking y latest phase

| ID | Item | Por que importa | Blocking? | Latest phase to resolve |
|---|---|---|---|---|
| U001 | Modelo de controlador KUKA | Determina KRL features, safety, motion, simulacion | ~~Si~~ -- **RESOLVED** (D001: KR C4) | Decision Readiness Gate (resolved) |
| U002 | KRL/KSS version | Sintaxis y features disponibles | ~~Si~~ -- **RESOLVED** (D001: KSS 8.3) | Decision Readiness Gate (resolved) |
| U003 | Entorno de simulacion | Plan de verificacion, testabilidad | ~~Si~~ -- **RESOLVED** (D002: KUKA.Sim + OfficeLite, no hardware) | Decision Readiness Gate (resolved) |
| U004 | Disponibilidad requerida | Criterios de aceptacion, diseno | No (deferible) | Arquitectura |
| U005 | Mantenimiento | Diagnostico, documentacion | No (deferible) | Arquitectura |
| U006 | Plazos | Planificacion | No (deferible) | Planificacion |
| U007 | Entorno de despliegue | Safety, integracion | No (deferible) | Arquitectura |
| U008 | Interface de autorizacion | Diseno de maquina de estados | ~~Si~~ -- **RESOLVED** (D006: CYCLE_REQUEST + CYCLE_COMPLETE handshake) | Decision Readiness Gate (resolved) |
| U009 | Interface de gripper (senales) | Control de gripper, verificacion | ~~Si~~ -- **RESOLVED** (D004: 2 digital outputs OPEN/CLOSE) | Decision Readiness Gate (resolved) |
| U010 | Feedback de gripper | Verificacion de agarre/liberacion | ~~Si~~ -- **RESOLVED** (D004: 3 digital inputs GRIPPER_OPEN/GRIPPER_CLOSED/PART_PRESENT) | Decision Readiness Gate (resolved) |
| U011 | Reporte de completitud | Interface externa | Si (blocking para arquitectura) | Decision Readiness Gate |
| U012 | Condiciones operativas | Logica de inicio de ciclo | ~~Si~~ -- **RESOLVED** (D005: 8 application-level conditions defined) | Decision Readiness Gate (resolved) |
| U013 | Formato de diagnosticos | Diseno de diagnostico | ~~No (deferible)~~ -- **RESOLVED** (D008: KRL variable diagnostics) | ~~Arquitectura~~ -- Arquitectura (resolved) |
| U014a | Posiciones -- identidad arquitectural | La secuencia del ciclo define que posiciones existen (pick approach, pick, place approach, place, safe wait). Esto es FACT, no UNKNOWN. La estructura de frames (base, tool, work frames) es una decision arquitectural, no una decision pre-arquitectura. | No (no blocking -- las posiciones son conocidas desde la secuencia; la estructura de frames es parte del trabajo de arquitectura) | Arquitectura |
| U014b | Posiciones -- valores fisicos | Los valores de coordenadas (X, Y, Z, A, B, C) requieren teaching o calibracion en el robot real. No son necesarios para arquitectura. | No (no blocking para arquitectura -- necesario para implementacion/despliegue) | Implementacion |
| U015 | Ciclo tiempo / rendimiento | Criterios de aceptacion, motion | No (deferible) | Arquitectura |
| U016 | Especificaciones de pieza | Gripper, verificacion | ~~Si~~ -- **RESOLVED** (D004: 100x60x40mm, 0.5kg, rigid rectangular) | Decision Readiness Gate (resolved) |
| U017 | Criterios de aceptacion | RQ Gate no puede PASS sin ellos | Si (blocking para RQ Gate) | Requirements Quality Gate |
| U018 | Fallos relevantes (enumeracion) | Deteccion, diagnostico, recuperacion | Si (blocking para arquitectura) | Decision Readiness Gate |

### Items DECISION NEEDED con blocking y latest phase

| ID | Decision | Blocking? | Latest phase to resolve |
|---|---|---|---|
| D001 | Modelo de robot y controlador | ~~BLOCKING~~ -- **RESOLVED** (KR 6 R900 sixx, KR C4, KSS 8.3) | Decision Readiness Gate (resolved Phase 1) |
| D002 | Entorno de simulacion y verificacion | ~~BLOCKING~~ -- **RESOLVED** (KUKA.Sim + OfficeLite, no hardware) | Decision Readiness Gate (resolved Phase 2) |
| D003 | Arquitectura de seguridad | ~~BLOCKING~~ -- **RESOLVED** (safety-rated functions out of scope, application-level boundary defined) | Decision Readiness Gate (resolved Phase 2) |
| D004 | Especificaciones de gripper y pieza | ~~BLOCKING~~ -- **RESOLVED** (pneumatic parallel, 2 DO + 3 DI, 100x60x40mm 0.5kg) | Decision Readiness Gate (resolved Phase 1) |
| D005 | Definicion de condiciones operativas | ~~BLOCKING~~ -- **RESOLVED** (8 application-level conditions, safety excluded) | Decision Readiness Gate (resolved Phase 3) |
| D006 | Interface de autorizacion y anti-duplicacion | ~~BLOCKING~~ -- **RESOLVED** (CYCLE_REQUEST/CYCLE_COMPLETE handshake, consumption-based anti-duplication) | Decision Readiness Gate (resolved Phase 4) |
| D007 | Criterios de aceptacion | ~~BLOCKING~~ -- **RESOLVED** (10 approved, 2 blocked by D009/D010) | Requirements Quality Gate (resolved) |
| D008 | Estrategia de diagnosticos | ~~NON-BLOCKING~~ -- **RESOLVED** (KRL variable diagnostics, 7 failure type codes, preserved across transitions) | Arquitectura (resolved during Architecture phase) |
| D009 | Estrategia de recuperacion | ~~BLOCKING~~ -- **RESOLVED** (limited auto-retry, SAFE_IDLE on failure, RECOVERY_RESET to leave) | Decision Readiness Gate (resolved Phase 5) |
| D010 | Definicion de safe state | ~~BLOCKING~~ -- **RESOLVED** (SAFE_IDLE, application-level, not safety-rated) | Decision Readiness Gate (resolved Phase 3) |

---

## 15. Framework observations (validation evidence)

### Framework observation: No KRL-specific robot software architecture skill

**Reference**: VL-023 (SUPERSEDED BY VL-031 -- see VALIDATION_LOG.md). VL-031
is the current authoritative entry for this observation.

**Observation**: The framework has `robotics-cell-integration` (integration
contract between robot and external systems) and `plc-software-architecture`
(PLC internal architecture), but no skill specifically for robot internal
software architecture in KRL. The Robotics Engineer agent is responsible for
"robot cell architecture" and "trayectorias y frames" but there is no skill
that produces a `ROBOT_SOFTWARE_ARCHITECTURE.md` or equivalent artefact for the
internal structure of robot software (state machines, motion logic modules,
gripper control modules, error handling, KRL program organization).

**Status**: UNDETERMINED. The discovery process cannot yet conclude whether
this is a confirmed framework gap. The following must be evaluated before
concluding:

1. Can `robotics-cell-integration` produce sufficient architecture guidance
   even when PLC is out of scope? Its procedure includes "robot internal
   behavior" ownership (step 16-17) but its required outputs focus on
   integration contracts, not internal software architecture.
2. Can the Robotics Engineer agent produce robot software architecture without
   a dedicated skill? The agent contract says "Disenar robot cell architecture"
   but does not specify a skill for internal software architecture.
3. Is the absence of a KRL-specific skill intentional (the framework is
   vendor-neutral by design, per `plc-software-architecture` failure mode:
   "Vendor lock-in innecesario") or an oversight?

**Classification**: Framework observation -- UNDETERMINED. NOT a confirmed
defect. NOT a confirmed contract gap. Will be re-evaluated during RQ Gate
(step 9: dependency-order verification) and architecture phase.

**Action**: Do not modify framework. Continue tracking in VALIDATION_LOG.md
(VL-031 is the current authoritative entry).

---

## 16. Workflow sequencing analysis

### Question

Does the intended workflow require `Discovery -> RQ Gate -> DR Gate` even when
Discovery already identifies unresolved blocking decisions?

### Contract analysis

**industrial-project-discovery SKILL.md**:
- Gates Interaction: "Antes de: Requirements Quality Gate. La skill produce el
  insumo que el gate evalua."
- "No reemplaza: Requirements Quality Gate. Discovery recopila y estructura;
  el gate evalua suficiencia y coherencia."
- Consumer: "Requirements Quality Gate"
- Handoff: "Engineering Architect para entregar a Requirements Quality Gate"
- Stop condition: "cuando existe informacion suficiente para que Requirements
  Quality Gate pueda evaluar la calidad de los requisitos"

**Requirements Quality GATE.md**:
- Inputs: "Idea inicial o PROJECT_DISCOVERY.md"
- Procedure step 7: "Detectar decisiones tecnicas abiertas que puedan bloquear
  arquitectura."
- Procedure step 8: "Clasificar cada decision como bloqueante o deferible."
- PASS criteria: "Las decisiones bloqueantes estan resueltas o derivadas al
  Decision Readiness Gate. Cuando existen decisiones blocking derivadas,
  Requirements Quality puede completar su responsabilidad (PASS), pero el
  workflow NO puede avanzar a arquitectura/planificacion hasta que Decision
  Readiness Gate supere con PASS."
- FAIL criteria: "Hay decisiones tecnicas bloqueantes sin informacion."
- Handoff: "PASS con decisiones blocking derivadas -> Decision Readiness Gate.
  El workflow queda bloqueado hasta que DR supere con PASS."

**Decision Readiness GATE.md**:
- Trigger: "Requirements Quality detecta decisiones abiertas."
- Inputs: "Requisitos validados (salida de Requirements Quality Gate)."

**ARCHITECTURE.md section 5.1-5.2**:
- RQ Gate PASS: "Decisiones bloqueantes estan resueltas o enviadas al Decision
  Readiness Gate."
- DR Gate Trigger: "Requirements Quality detecta decisiones abiertas."
- DR Gate Inputs: "Requisitos validados."

### Conclusion

**Executing RQ Gate with known unresolved blocking decisions is intentional
framework behavior and required routing behavior.**

The framework contracts clearly define the workflow as:

```
Discovery (optional, pre-Gate)
  -> RQ Gate (evaluates sufficiency, detects/classifies decisions)
  -> DR Gate (if RQ detects blocking decisions, resolves them)
  -> Architecture/Planning (after RQ and DR PASS)
```

RQ Gate is designed to receive input that may contain unresolved blocking
decisions. Its job is to:
1. Evaluate whether requirements have sufficient objective, scope, constraints,
   and acceptance criteria.
2. Detect and classify blocking decisions (step 7-8).
3. Route blocking decisions to DR Gate (PASS with derivations) or FAIL if
   there is insufficient information to even classify them.

Discovery identifying and structuring decisions is complementary to RQ Gate,
not a bypass. Discovery provides structured input; RQ Gate evaluates
sufficiency and coherence. The two components have different responsibilities:
- Discovery: collect and structure (produces PROJECT_DISCOVERY.md)
- RQ Gate: evaluate sufficiency and coherence (produces REQUIREMENTS_GATE_REPORT.md)

**This is NOT a framework sequencing gap.** The workflow is clearly defined in
the contracts. RQ Gate cannot be bypassed even when Discovery has already
identified blocking decisions.

**Classification**: Framework observation -- workflow sequencing is intentional
and correctly defined. No gap detected.

---

## 17. Handoff

This `PROJECT_DISCOVERY.md` is delivered to the Engineering Architect for
handoff to Requirements Quality Gate.

The discovery skill stops here. It has produced structured information for RQ
Gate to evaluate. It has not resolved decisions, created architecture, or
implemented code.

**Next authorized action**: Execute Requirements Quality Gate with this
artefact as input. This requires explicit authorization.

Per framework contracts, RQ Gate will:
1. Validate objective, scope, constraints, and acceptance criteria.
2. Detect and classify blocking decisions (D001-D006, D009, D010).
3. Route blocking decisions to DR Gate (if PASS with derivations) or FAIL
   if acceptance criteria are missing (D007/U017).
4. Verify dependency-order consistency (step 9, C3 improvement).
5. Produce REQUIREMENTS_GATE_REPORT.md with PASS or FAIL.

Expected outcome: RQ Gate will likely return FAIL because acceptance criteria
are missing (D007/U017). Corrective action: request acceptance criteria from
user. Once provided, RQ Gate can PASS with blocking decisions derived to DR
Gate.
