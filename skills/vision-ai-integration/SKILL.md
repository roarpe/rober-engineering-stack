# Skill -- vision-ai-integration

## Name

vision-ai-integration

## Purpose

Disenar la integracion de vision artificial o IA dentro de un sistema industrial
sin tratar un modelo o algoritmo aislado como si fuera el sistema completo.
Definir el contrato de integracion del componente de vision/IA con PLC, robot y
software, no el modelo ni el algoritmo interno.

## Activation Triggers

- Proyecto involucra vision artificial, IA o inferencia integrada con sistema
  industrial.
- Hay necesidad de definir como se dispara, consume y valida un resultado de
  vision/IA.
- Hay necesidad de definir comportamiento ante resultado invalido, incierto,
  tardio o no disponible.
- Requirements Quality PASS y Decision Readiness PASS (si aplica).

## When Not To Use

- El proyecto no involucra vision ni IA.
- La vision/IA opera aislada sin integracion con PLC, robot o software.
- Requirements Quality no ha superado PASS.
- Se necesita entrenar o seleccionar un modelo definitivo sin evidencia (la
  skill no entrena modelos ni selecciona sin evidencia).
- El cambio es trivial (ej. ajuste de umbral de confianza) sin impacto en
  integracion.

## Primary Owner

Engineering Architect (integracion transversal)

## Participants

- Software Engineer (implementacion de software de vision/IA).
- Robotics Engineer (integracion robot-vision: picking, calibracion, frames).
- Industrial Automation Engineer (integracion PLC-vision: trigger, resultado,
  fallback).
- QA & Debug Engineer (define criterios de verificacion de integracion).
- Technical Documentation Engineer (documenta contrato de integracion).

## Required Inputs

- Requisitos validados (salida de Requirements Quality Gate).
- Decision map resuelto (salida de Decision Readiness Gate, si aplica).
- `PROJECT_DISCOVERY.md` si existe.
- Arquitecturas de dominio existentes (PLC, robot, software).
- Especificaciones de hardware de vision cuando aplique.
- ADRs aplicables.

## Procedure

1. Confirmar precondiciones: RQ PASS y DR PASS (si aplica).
2. Describir el problema operativo que la vision/IA resuelve.
3. Definir input: que recibe el sistema de vision/IA (imagen, stream, datos,
   trigger).
4. Definir output: que produce el sistema de vision/IA (resultado, coordenadas,
   clasificacion, medicion).
5. Definir consumer: quien consume el resultado (PLC, robot, software).
6. Definir acquisition trigger: cuando y como se dispara la adquisicion.
7. Definir timing: latencia, throughput, deadlines.
8. Definir hardware constraints y deployment environment.
9. Definir pipeline: preprocessing, inference, postprocessing.
10. Definir confidence/quality semantics: que significa el score de confianza,
    umbral de aceptacion, gradacion de incertidumbre.
11. Definir invalid result behavior: que pasa si el resultado es invalido o
    fuera de rango.
12. Definir timeout behavior: que pasa si la inferencia tarda mas de lo
    esperado.
13. Definir fallback behavior: modo degradado, reintentos, alternativa manual.
14. Definir degraded mode: operacion sin vision/IA disponible.
15. Definir traceability: como se rastrea cada resultado a su input, modelo y
    version.
16. Definir dataset provenance cuando aplique (origen, version, sesgo conocido).
17. Definir versionado de modelo y mecanismo de actualizacion.
18. Definir rollback: como se vuelve a una version anterior si el modelo falla.
19. Definir observabilidad: metricas, logs, alertas de drift cuando aplique.
20. Definir integracion con PLC (trigger, resultado, fallback).
21. Definir integracion con robot (coordenadas, frames, picking).
22. Definir integracion con software (API, servicio, persistencia).
23. Para cada resultado de vision/IA, registrar:
    - Producer (quien produce el resultado).
    - Consumer (quien lo consume).
    - Meaning (que significa el resultado).
    - Confidence/Quality semantics (como se interpreta la confianza).
    - Timing constraints (deadline, latencia maxima).
    - Invalid/Unavailable behavior (que pasa si es invalido o no hay).
    - Fallback behavior (modo alternativo).
    - Traceability requirements (como se rastrea).
    - Verification method (como se verifica).
24. Distinguir entre model/algorithm quality, software integration quality, e
    industrial system behavior.
25. Producir el artefacto de salida.

### Niveles de calidad

- **Model/algorithm quality**: precision, recall, F1, error de medicion,
  robustez. Se evalua offline con dataset de test. No es responsabilidad de
  esta skill.
- **Software integration quality**: latencia, throughput, manejo de errores,
  observabilidad. Se evalua con tests de integracion.
- **Industrial system behavior**: comportamiento de PLC, robot y celula ante
  resultado valido, invalido, incierto, tardio o no disponible. Se evalua con
  tests de sistema.

## Required Outputs

Artefacto: `VISION_AI_INTEGRATION.md`

Contenido obligatorio:

- Problema operativo.
- Input, output, consumer.
- Acquisition trigger.
- Timing (latencia, throughput, deadlines).
- Hardware constraints y deployment environment.
- Pipeline (preprocessing, inference, postprocessing).
- Confidence/quality semantics.
- Invalid result behavior.
- Timeout behavior.
- Fallback behavior y degraded mode.
- Traceability requirements.
- Dataset provenance cuando aplique.
- Versionado de modelo, actualizacion y rollback.
- Observabilidad y drift.
- Integracion con PLC, robot y software.
- Tabla de resultados con los 9 campos obligatorios por resultado.
- Distincion entre model/algorithm quality, software integration quality, e
  industrial system behavior.

## Consumer

Engineering Architect (coherencia transversal), especialistas de dominio
(planificacion e implementacion de integracion).

## Stop Condition

La skill se detiene cuando la vision/IA tiene un contrato de integracion
verificable y se conocen los comportamientos ante resultado valido, invalido,
incierto, tardio o no disponible. No es necesario que el modelo este entrenado
ni que el pipeline este implementado.

## Gates Interaction

- **Precondicion**: Requirements Quality PASS. Decision Readiness PASS (si
  aplica).
- **Despues de**: el contrato de integracion se entrega a planificacion e
  implementacion. Implementation Review revisara la implementacion posterior.
- **No ejecuta**: Implementation Review, Final Verification ni ningun gate.
- **No selecciona modelo definitivo**: si no hay evidencia suficiente para
  seleccionar un modelo, se registra como decision abierta y se escala a
  Decision Readiness Gate.

## Agent Interaction

- **Activada por**: Engineering Architect (owner de integracion transversal).
- **Participan**: Software Engineer (software), Robotics Engineer (robot),
  Industrial Automation Engineer (PLC).
- **Handoff a**: especialistas de dominio para implementacion de su lado del
  contrato.

## Evidence Required

- `VISION_AI_INTEGRATION.md` con todos los campos obligatorios.
- Tabla de resultados con los 9 campos por resultado de vision/IA.
- Comportamiento ante resultado valido, invalido, incierto, tardio y no
  disponible definido.
- Distincion entre model/algorithm quality, software integration quality, e
  industrial system behavior.
- Traceability requirements definidos.

## Failure Modes

- Tratar el modelo como el sistema completo (ignorar integracion).
- No definir comportamiento ante resultado invalido o no disponible.
- No definir timeout ni fallback.
- Asumir que IA siempre devuelve resultado valido.
- Seleccionar modelo definitivo sin evidencia.
- Disenar PLC completo o robot completo (invadir dominio).
- No distinguir model quality de integration quality de system behavior.
- No definir versionado ni rollback de modelo.
- No definir drift detection cuando aplique.

## Escalation Rules

- Decision de modelo no resuelta -> escalar a Decision Readiness Gate.
- Conflicto de integracion entre dominios -> Engineering Architect resuelve.
- Interface con PLC -> Industrial Automation Engineer.
- Interface con robot -> Robotics Engineer.
- Interface con software -> Software Engineer.
- Seguridad funcional -> escalar al usuario o especialista certificado.
- Drift o degradacion de modelo fuera de dominio de integracion -> escalar a
  especialista de ML/vision.

## Done Criteria

- `VISION_AI_INTEGRATION.md` completo con todos los campos obligatorios.
- Tabla de resultados con los 9 campos por resultado.
- Comportamiento ante resultado valido, invalido, incierto, tardio y no
  disponible definido.
- Distincion entre model/algorithm quality, software integration quality, e
  industrial system behavior.
- Integracion con PLC, robot y software definida.
- Versionado, rollback y traceability definidos.
- Artefacto entregado a especialistas de dominio para implementacion.
