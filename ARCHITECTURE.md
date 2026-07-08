# ROBER ENGINEERING STACK v1.0 - Architecture

Fecha: 2026-07-07 (Fase 2); actualizado 2026-07-08 (Fase 9A)
Fase: 9A - Documentacion reconciliada tras implementacion de Fases 3-8
Estado: arquitectura implementada con 4 gates, 6 agentes, 9 skills y 8 modulos

## 1. Fuentes de verdad

Esta arquitectura se basa en:

- `ENVIRONMENT_AUDIT.md`
- `SKILLS_AUDIT.md`

Restricciones heredadas:

- No modificar configuracion global en esta fase.
- No instalar skills.
- No crear aun agentes definitivos.
- No implementar aun las 9 custom industrial skills.
- Mantener el Global Core pequeno.
- Evitar duplicidades entre discovery, requirements gate, planificacion, ADRs, review y verification.

## 2. Objetivo arquitectonico

ROBER ENGINEERING STACK v1.0 sera un sistema modular para proyectos de software, automatizacion industrial, PLC, robotica, vision artificial, IA, integracion de sistemas y datos.

El stack tendra cinco capas:

1. Global Core minimo.
2. Engineering Gates.
3. Project Modules.
4. Custom Industrial Skills.
5. Optional Skill Library.

El principio rector es cargar solo lo necesario para el proyecto y la fase actual. Las skills no son decoracion ni coleccion: son herramientas invocables con trigger, input, output y coste de contexto.

## 3. Principios permanentes vs skills bajo demanda

### Principios permanentes

Los principios permanentes deben vivir en el futuro `AGENTS.md` raiz. Son reglas cortas, siempre activas, que no requieren leer una skill completa.

Contenido recomendado para `AGENTS.md`:

- Analizar antes de implementar.
- Investigar antes de instalar.
- Verificar antes de declarar terminado.
- Mantener Global Core pequeno.
- Separar core, gates, modulos, skills industriales y biblioteca opcional.
- Elegir modulos, agentes y skills segun riesgo, complejidad y tecnologia.
- No usar una skill si su output no tiene consumidor claro.
- Registrar decisiones arquitectonicas relevantes como ADR.
- Evitar aprendizaje global automatico sin evidencia y aprobacion.
- Priorizar evidencia sobre afirmaciones.

### Skills bajo demanda

Las skills deben permanecer invocables bajo demanda cuando aportan un procedimiento especifico, largo o costoso.

Mantener como skill, no como regla permanente:

- `grill-with-docs`: entrevista y documentacion de requisitos.
- `code-review`: review separada por standards y spec.
- `verification-before-completion`: gate final con evidencia fresca.
- `prototype`: prototipo desechable.
- `to-prd` y `to-issues`: formalizacion de backlog.
- `api-design`: diseno REST/API.
- `using-git-worktrees`: aislamiento operativo.
- `improve-codebase-architecture`: analisis visual de arquitectura existente.
- `skill-stocktake` y `agent-sort`: auditorias periodicas de superficies.

Regla: si una instruccion es universal, breve y estable, sintetizarla en `AGENTS.md`. Si es larga, fase-especifica, costosa, interactiva o con side effects, mantenerla como skill o gate.

## 4. Global Core minimo

El Global Core inicial se inspira en `agentic-engineering`, `writing-plans` y `systematic-debugging`, pero no debe instalar paquetes completos.

### 4.1 agentic-engineering

Sintetizar como reglas permanentes:

- Definir criterios de completitud antes de ejecutar.
- Dividir trabajo en unidades verificables.
- Escalar modelo/agente segun complejidad y riesgo.
- Medir resultado con tests, evals o checks reproducibles.
- Controlar coste: no usar agentes o skills pesadas sin motivo.

Mantener como skill/biblioteca:

- Guias detalladas de model routing.
- Evals formales.
- Benchmarking de agentes.

### 4.2 writing-plans

Sintetizar como reglas permanentes:

- Todo trabajo mediano/grande debe tener plan.
- Cada tarea debe tener objetivo, archivos probables, verificacion y criterio de done.
- El plan debe ser proporcional: corto para tareas pequenas, detallado para ejecucion delegada.
- No aceptar planes con placeholders, pasos ambiguos o verificaciones vagas.

Mantener como skill:

- Generacion de planes largos con pasos exactos.
- Handoff a `subagent-driven-development` o `executing-plans`.
- Planes con codigo, comandos y checkpoints por tarea.

### 4.3 systematic-debugging

Sintetizar como reglas permanentes:

- No corregir sin entender causa raiz.
- Reproducir, leer errores, revisar cambios recientes y formular hipotesis.
- Probar una hipotesis a la vez.
- Si tres intentos fallan, cuestionar arquitectura o supuestos.

Mantener como skill:

- Debugging largo o de integracion.
- Analisis de causa raiz multi-componente.
- Instrumentacion y trazado detallado.

### 4.4 Excluido del Global Core

No incluir:

- `brainstorming`: solapa con `industrial-project-discovery` y `grill-with-docs`.
- `test-driven-development`: modulo, no regla universal.
- `subagent-driven-development`: solo con plan aprobado y tareas delegables.
- `continuous-learning-v2`: experimental y con hooks.
- `improve-codebase-architecture`: alto coste y uso especifico.

## 5. Engineering Gates

Los gates son controles de calidad en puntos concretos. No son skills siempre activas.

### 5.1 Gate 1 - Requirements Quality

Base: `grill-with-docs`.

Objetivo:

- Validar que los requisitos son suficientes para disenar arquitectura o plan.
- Construir lenguaje compartido y detectar decisiones abiertas.

Trigger:

- Proyecto nuevo no trivial.
- Cambio con impacto en dominio, arquitectura, PLC/robot/vision/datos.
- Requisitos ambiguos o sin criterios de aceptacion.

Inputs:

- Idea inicial o `PROJECT_DISCOVERY.md`.
- Contexto del repo/proyecto.
- Restricciones del usuario.
- Glosario/CONTEXT/ADRs existentes si existen.

Outputs:

- Requisitos aclarados.
- Preguntas resueltas.
- Ambiguedades restantes.
- Terminos de dominio candidatos.
- ADRs propuestos si hay decisiones dificiles.
- Decision: PASS o FAIL.

PASS:

- Objetivo, alcance, usuarios, restricciones y criterios de aceptacion estan claros.
- Decisiones bloqueantes estan resueltas o enviadas al Decision Readiness Gate.
- Existe output documental suficiente para arquitectura.

FAIL:

- Faltan criterios de aceptacion.
- El alcance mezcla subsistemas independientes sin separacion.
- Hay decisiones tecnicas bloqueantes sin informacion.
- El vocabulario de dominio es confuso o contradictorio.

Acciones correctivas:

- Ejecutar mas discovery.
- Dividir el proyecto.
- Pedir datos al usuario.
- Crear lista de decisiones pendientes.

Responsable:

- Engineering Architect.
- Participan Technical Documentation Engineer y agente de dominio si aplica.

Cuando NO usar:

- Tarea pequena, local y claramente especificada.
- Correccion mecanica con test/bug reproducible.
- Cambio documental menor sin ambiguedad.

### 5.2 Gate 2 - Decision Readiness

Base: gate propio. `decision-mapping` fue rechazado porque no se localizo como skill real.

Objetivo:

- Determinar si hay decisiones tecnicas pendientes y si existe informacion suficiente para resolverlas.

Trigger:

- Requirements Quality detecta decisiones abiertas.
- Hay multiples alternativas arquitectonicas viables.
- Existen dependencias entre decisiones.
- La incertidumbre tecnica podria requerir prototipo.

Inputs:

- Requisitos validados.
- Riesgos identificados.
- Restricciones tecnicas.
- Opciones conocidas.
- Evidencia disponible.

Outputs:

- `Decision Map` dentro del documento de arquitectura o plan.
- Lista de decisiones con: pregunta, opciones, informacion necesaria, dependencias, criterio de resolucion, owner.
- Recomendacion de prototipo, investigacion o ADR.

PASS:

- Las decisiones bloqueantes estan resueltas o tienen plan de resolucion.
- Se sabe que decisiones pueden diferirse.
- Las dependencias entre decisiones estan claras.

FAIL:

- Hay decisiones bloqueantes sin owner.
- Faltan datos necesarios.
- Se intenta disenar arquitectura sobre suposiciones criticas no verificadas.

Acciones correctivas:

- Ejecutar investigacion dirigida.
- Ejecutar `prototype` si hay incertidumbre tecnica.
- Consultar al usuario.
- Crear ADR cuando se tome una decision relevante.

Responsable:

- Engineering Architect.
- Participan Software, Industrial Automation, Robotics o QA segun el tipo de decision.

Cuando NO usar:

- La solucion es obvia, reversible y de bajo riesgo.
- Ya existe ADR aplicable.
- El trabajo es puramente mecanico.

### 5.3 Gate 3 - Implementation Review

Base: `code-review` de mattpocock, mapeada desde `review`.

Objetivo:

- Revisar implementacion contra especificacion, requisitos, arquitectura y standards.
- Separar dos ejes: Standards y Spec.

Trigger:

- Fin de una tarea mediana/grande.
- Antes de merge/PR.
- Antes de declarar completa una implementacion.
- Tras cambios en PLC/robot/API/comunicaciones con riesgo operativo.

Inputs:

- Diff o cambios producidos.
- Spec/PRD/plan/requisitos.
- Standards del repo o modulo.
- ADRs aplicables.
- Resultados de tests.

Outputs:

- Findings por severidad.
- Eje Standards: incumplimientos de convenciones, diseno, mantenibilidad.
- Eje Spec: requisitos faltantes, scope creep, comportamiento incorrecto.
- Decision: PASS o FAIL.

PASS:

- No hay findings criticos ni importantes sin resolver.
- El diff implementa los requisitos aplicables.
- Los standards relevantes se cumplen o hay justificacion documentada.

FAIL:

- Falta algun requisito importante.
- Hay desviacion de arquitectura sin ADR.
- Hay problemas criticos de seguridad, integracion, testabilidad o mantenibilidad.
- No hay spec verificable para comparar.

Acciones correctivas:

- Corregir findings criticos/importantes.
- Actualizar spec si el requisito cambio.
- Crear ADR si se acepta una desviacion.
- Repetir review.

Responsable:

- QA & Debug Engineer lidera.
- Engineering Architect decide trade-offs.
- Technical Documentation Engineer valida docs/ADRs.

Cuando NO usar:

- No hay implementacion/diff.
- Cambio trivial ya cubierto por verificacion automatica y bajo riesgo.
- Fase actual solo esta creando arquitectura, no codigo.

### 5.4 Gate 4 - Final Verification

Base: `verification-before-completion`.

Objetivo:

- Evitar declarar un proyecto terminado sin evidencia fresca.

Trigger:

- Antes de cerrar tarea/proyecto.
- Antes de entregar artefactos finales.
- Antes de afirmar "terminado", "funciona", "tests pasan" o equivalente.

Inputs:

- Requisitos y criterios de aceptacion.
- Plan y tasks.
- Resultados de tests/verificaciones.
- Review findings.
- Documentacion requerida.
- Riesgos pendientes.

Outputs:

- Evidencia fresca: comandos, checks, inspecciones, resultados.
- Lista de criterios PASS/FAIL.
- Riesgos residuales.
- Decision final.

PASS:

- Cada criterio de aceptacion tiene evidencia.
- Tests/checks relevantes fueron ejecutados recientemente.
- Reviews criticas estan resueltas.
- Documentacion minima esta actualizada.

FAIL:

- Hay claims sin evidencia.
- Tests no ejecutados o incompletos.
- Riesgos criticos pendientes.
- Documentacion o criterios de aceptacion faltan.

Acciones correctivas:

- Ejecutar verificaciones faltantes.
- Corregir fallos.
- Documentar limitaciones.
- Reabrir review o debugging si procede.

Responsable:

- QA & Debug Engineer.
- Engineering Architect aprueba entrega.
- Technical Documentation Engineer verifica documentos.

Cuando NO usar:

- Nunca se omite antes de declarar completitud.
- Para microtareas conversacionales sin artefacto, basta una verificacion proporcional.

## 6. Project Modules

Los modulos se activan por proyecto, tecnologia, riesgo o fase. Ninguno debe estar activo por defecto si no aplica.

### 6.1 software-development

Activar cuando:

- Hay codigo backend, CLI, servicios, librerias o integraciones.

Skills bajo demanda:

- Custom skills: `industrial-python-engineering`, `industrial-communications-design`, `vision-ai-integration`, `machine-diagnostics`, `industrial-documentation`, `industrial-project-verification`.
- `writing-plans`
- `systematic-debugging`
- `test-driven-development`
- `api-design` si hay APIs
- `architecture-decision-records`
- `code-review`

No usar cuando:

- El trabajo es solo documentacion industrial sin software.

### 6.2 industrial-automation

Activar cuando:

- Hay PLC, IEC 61131-3, maquinas de estados, alarmas, modos, HMI, I/O o comunicaciones industriales.

Skills bajo demanda:

- Custom skills: `industrial-project-discovery`, `plc-software-architecture`, `industrial-communications-design`, `machine-diagnostics`, `industrial-documentation`, `industrial-project-verification`.
- `systematic-debugging` para fallos.
- ADRs para decisiones de arquitectura.

No usar cuando:

- El proyecto no toca automatizacion, control o integracion industrial.

### 6.3 robotics

Activar cuando:

- Hay robot industrial, ROS 2, celula robotizada, vision-robot, herramientas, perifericos o seguridad robotica.

Skills bajo demanda:

- Custom skills: `robotics-cell-integration`, `industrial-communications-design`, `vision-ai-integration`, `machine-diagnostics`, `industrial-documentation`, `industrial-project-verification`.
- `prototype` para incertidumbre de estado/flujo.
- ADRs.

No usar cuando:

- El robot no forma parte del sistema o solo se menciona como contexto no operativo.

### 6.4 artificial-intelligence

Activar cuando:

- Hay modelos, agentes, pipelines de IA, evals, prompts, razonamiento o aprendizaje.

Skills bajo demanda:

- Custom skills: `vision-ai-integration`, `industrial-python-engineering`, `industrial-communications-design`, `machine-diagnostics`, `industrial-documentation`, `industrial-project-verification`.
- `agentic-engineering`
- `agent-harness-construction`
- `agent-eval` experimental
- `skill-stocktake` para skills propias
- `continuous-learning-v2` solo experimental y aprobado

No usar cuando:

- La IA no afecta diseno, validacion ni operacion.

### 6.5 computer-vision

Activar cuando:

- Hay camaras, inspeccion, clasificacion, calibracion, iluminacion, dataset o inferencia visual.

Skills bajo demanda:

- Custom skills: `vision-ai-integration`, `robotics-cell-integration`, `industrial-python-engineering`, `industrial-communications-design`, `machine-diagnostics`, `industrial-project-verification`.
- `prototype` si se necesita validar pipeline o UI.
- `systematic-debugging` para fallos de integracion.

No usar cuando:

- Vision solo aparece como requisito futuro no abordado en la fase.

### 6.6 data-engineering

Activar cuando:

- Hay adquisicion, procesamiento, almacenamiento, historizacion, ETL, telemetria o analytics.

Skills bajo demanda:

- Custom skills: `industrial-python-engineering`, `industrial-communications-design`, `machine-diagnostics`, `industrial-documentation`, `industrial-project-verification`.
- `api-design` si hay contratos de datos/API.
- `writing-plans`
- ADRs.

No usar cuando:

- Los datos no salen del equipo/local o no hay persistencia/analisis.

### 6.7 web-development

Activar cuando:

- Hay UI web, dashboards, APIs web, frontend/backend o experiencia de usuario.

Skills bajo demanda:

- Custom skills: `industrial-python-engineering` cuando Python aplique, `industrial-communications-design`, `machine-diagnostics`, `industrial-documentation`, `industrial-project-verification`.
- `api-design`
- `prototype` para exploracion UI.
- `test-driven-development`
- `code-review`

No usar cuando:

- No hay interfaz web ni backend web.

### 6.8 git-parallel-delivery

Activar cuando:

- Hay trabajo paralelo, multiples agentes, ramas o PRs.

Skills bajo demanda:

- `using-git-worktrees`
- `subagent-driven-development`
- `executing-plans`
- `finishing-a-development-branch`

No usar cuando:

- Repo no tiene commits base.
- `gh` remoto es necesario pero no esta autenticado.
- El entorno/harness ya gestiona worktrees y no se ha detectado correctamente.

## 7. Optional Skill Library

La biblioteca opcional evita cargar contexto innecesario.

Mecanismo propuesto:

1. Mantener un catalogo local `library/optional-skills/` en fases posteriores.
2. Cada entrada debe tener: nombre, origen, trigger, coste, inputs, outputs, no-usar-cuando, solapamientos.
3. Usar el patron de `agent-sort`: DAILY vs LIBRARY, pero adaptado a ROBER:
   - `CORE`: reglas compactas en `AGENTS.md`.
   - `GATE`: invocacion en punto de control.
   - `MODULE`: activacion por proyecto/fase.
   - `LIBRARY`: busqueda manual bajo demanda.
   - `EXPERIMENTAL`: requiere aprobacion.
4. Usar `skill-stocktake` periodicamente para revisar calidad, frescura y duplicidad, no como skill activa diaria.

Skills en biblioteca inicial:

- `brainstorming`
- `executing-plans`
- `requesting-code-review`
- `agent-harness-construction`
- `agent-eval`
- `domain-modeling`
- `codebase-design`
- `research`
- `writing-skills`

No usar biblioteca opcional cuando:

- Ya hay gate o modulo activo que cubre el problema.
- La skill no tiene output verificable.
- La skill introduce side effects no autorizados.
- La skill contradice instrucciones del usuario o `AGENTS.md`.

## 8. Custom Industrial Skills

Las 9 custom skills industriales conforman la capa 4. Estan implementadas (Fases 7A-7D) con contratos en `skills/*/SKILL.md`.

### 8.1 industrial-project-discovery

Rol:

- Transformar idea inicial industrial en `PROJECT_DISCOVERY.md`.

Encaje:

- Antes del Requirements Quality Gate.

No duplicar:

- No debe hacer review final.
- No debe generar arquitectura completa.
- No debe reemplazar `grill-with-docs`; le entrega material.

### 8.2 plc-software-architecture

Rol:

- Disenar estructura PLC, FBs, estados, alarmas, modos, diagnostico, simulacion y tests.

Encaje:

- Modulo industrial-automation tras requirements y decision readiness.

No duplicar:

- No debe disenar robot completo.
- No debe disenar protocolos salvo interfaces necesarias.

### 8.3 industrial-communications-design

Rol:

- Disenar OPC UA, MQTT, Modbus TCP, Profinet, EtherNet/IP, REST u otros protocolos.

Encaje:

- Modulos industrial-automation, robotics, artificial-intelligence, computer-vision, data-engineering, web-development, software-development.

No duplicar:

- No debe ser API design generico; debe cubrir tiempos, watchdogs, reconexion, productores/consumidores y fallos industriales.

### 8.4 robotics-cell-integration

Rol:

- Integrar robot, PLC, seguridad, vision, herramientas, perifericos, estados y recuperacion.

Encaje:

- Modulos robotics, computer-vision.

No duplicar:

- No debe disenar PLC interno salvo contrato/secuencia de integracion.

### 8.5 vision-ai-integration

Rol:

- Integrar vision artificial o IA en sistema industrial: trigger, resultado, confianza, fallback, degradado, trazabilidad, versionado y verificacion.

Encaje:

- Modulos computer-vision, robotics, artificial-intelligence, software-development.

No duplicar:

- No debe entrenar modelos ni seleccionarlos sin evidencia; define el contrato de integracion, no el modelo.

### 8.6 industrial-python-engineering

Rol:

- Ingenieria de software Python industrial: arquitectura de aplicacion, estructura, config, logging, excepciones, typing, testing, packaging, despliegue, observabilidad, concurrencia, serializacion, simulacion, rollback, stale data y comportamiento ante fallos de subsistemas externos. Los estandares son parte del diseno, no el proposito completo.

Encaje:

- Modulos software-development, artificial-intelligence, computer-vision, data-engineering, web-development.

No duplicar:

- No reemplaza `api-design`; lo complementa si hay API.

### 8.7 machine-diagnostics

Rol:

- Proceso de diagnostico: sintoma, datos, senales, hipotesis, pruebas, causa raiz, correccion, verificacion, prevencion.

Encaje:

- Industrial debugging y soporte operativo.

No duplicar:

- No reemplaza `systematic-debugging`; lo especializa para maquinas/senales/proceso.

### 8.8 industrial-documentation

Rol:

- Documentacion tecnica industrial para desarrolladores, mantenimiento, operadores y arquitectura.

Encaje:

- Durante y despues de arquitectura/implementacion.

No duplicar:

- No reemplaza herramientas de documentos/PDF; define contenido, estructura y criterios.

### 8.9 industrial-project-verification

Rol:

- Verificar requisitos, implementacion, tests, integracion, errores, docs, aceptacion y riesgos.

Encaje:

- Complementa Final Verification Gate.

No duplicar:

- `verification-before-completion` exige evidencia general; esta skill define checklist industrial especifico.

## 9. Arquitectura de agentes

Los agentes se disenaran en Fase 6. En esta fase se definen limites.

### 9.1 Engineering Architect

Mision:

- Coordinar arquitectura, seleccionar modulos/agentes/skills, ejecutar gates y mantener coherencia.

Limites:

- No debe implementar todo personalmente.
- No debe saltarse gates en proyectos medianos/grandes.

Inputs:

- Discovery, requisitos, riesgos, auditorias, ADRs.

Outputs:

- Arquitectura, decision map, plan de modulos/agentes/skills, ADRs propuestos.

Participa en:

- Todos los gates.

### 9.2 Industrial Automation Engineer

Mision:

- PLC, estados, modos, alarmas, I/O, diagnostico y comunicaciones industriales.

Limites:

- No lidera arquitectura software general salvo interfaces industriales.

Outputs:

- PLC architecture, secuencias, interfaces, criterios de simulacion/test.

Participa en:

- Requirements, Decision Readiness, Implementation Review y Industrial Verification.

### 9.3 Robotics Engineer

Mision:

- Robotica industrial, ROS 2, integracion robot-PLC, herramientas, trayectorias, vision y celulas.

Limites:

- No disena PLC interno ni backend salvo contratos necesarios.

Outputs:

- Robot cell architecture, estado robotico, senales, recuperacion.

### 9.4 Software Engineer

Mision:

- Python, C++, C#, backend, APIs, bases de datos e integracion.

Limites:

- No decide seguridad industrial ni robotica sin especialistas.

Outputs:

- Software architecture, API/data contracts, implementation plan.

### 9.5 QA & Debug Engineer

Mision:

- Testing, debugging sistematico, verificaciones, acceptance criteria y causa raiz.

Limites:

- No cambia arquitectura sin Engineering Architect.

Outputs:

- Test plan, debug reports, review findings, verification report.

### 9.6 Technical Documentation Engineer

Mision:

- README, documentacion tecnica, ADRs, manuales, diagramas, troubleshooting.

Limites:

- No inventa decisiones tecnicas; documenta decisiones aprobadas.

Outputs:

- Docs actualizadas, ADRs, glosario, guia de operacion/mantenimiento.

## 10. Mecanismo de seleccion

Flujo obligatorio de seleccion:

```text
PROJECT
  -> RISK/COMPLEXITY ANALYSIS
  -> MODULE SELECTION
  -> AGENT SELECTION
  -> SKILL SELECTION
  -> GATES
  -> EXECUTION
```

### 10.1 Project

Capturar:

- Objetivo.
- Dominio.
- Artefactos esperados.
- Tecnologias conocidas.
- Restricciones.

### 10.2 Risk/Complexity Analysis

Clasificar:

- Pequeno: bajo riesgo, 1 modulo, sin integracion critica.
- Mediano: varios componentes, tests/documentacion necesarios, decisiones limitadas.
- Grande: multiagente, industrial/robot/vision/datos, riesgos de integracion o seguridad.

Evaluar:

- Criticidad industrial.
- Incertidumbre tecnica.
- Numero de subsistemas.
- Necesidad de trazabilidad.
- Necesidad de trabajo paralelo.

### 10.3 Module Selection

Seleccionar solo modulos que correspondan a tecnologia y riesgo.

### 10.4 Agent Selection

Seleccionar agentes por responsabilidad, no por disponibilidad.

Regla:

- Engineering Architect coordina.
- Especialistas entran solo si su dominio esta activo.
- QA entra cuando hay implementacion, debug o verificacion.
- Documentation entra cuando hay outputs duraderos.

### 10.5 Skill Selection

Seleccionar skills por trigger y output.

Preguntas:

- Que problema concreto resuelve?
- Que input consume?
- Que output produce?
- Que coste de contexto tiene?
- Que solapamiento introduce?
- Hay una opcion mas ligera?

### 10.6 Gates

Aplicar gates proporcionales:

- Pequeno: Final Verification minimo; Requirements solo si hay ambiguedad.
- Mediano: Requirements, Implementation Review, Final Verification.
- Grande: los cuatro gates.

### 10.7 Execution

Ejecutar con plan proporcional. No usar subagentes ni worktrees salvo que haya tareas delegables o paralelo real.

## 11. Politica de precedencia

Orden de precedencia:

```text
SAFETY/USER INSTRUCTIONS
  -> ROOT AGENTS.md
  -> PROJECT MODULE
  -> ACTIVE AGENT
  -> ACTIVE SKILL
  -> TASK-SPECIFIC INSTRUCTIONS
```

Reglas:

- Las instrucciones de seguridad y del usuario siempre ganan.
- `AGENTS.md` raiz define constitucion operativa.
- Un modulo no puede contradecir `AGENTS.md`; solo especializa.
- Un agente no puede invadir responsabilidades de otro sin delegacion explicita.
- Una skill no puede saltarse gates o modificar configuracion global sin permiso.
- Instrucciones de tarea pueden acotar alcance, pero no relajar seguridad, verificacion o precedencia.

Si hay conflicto:

1. Identificar las instrucciones en conflicto.
2. Aplicar precedencia.
3. Si sigue ambiguo, detenerse y pedir decision al usuario.
4. Registrar decision como ADR si afecta arquitectura futura.

## 12. Flujos por complejidad

### 12.1 Proyecto pequeno

Ejemplos:

- Script simple.
- Ajuste documental.
- Bug local reproducible.

Flujo:

1. Confirmar objetivo y criterio de done.
2. Seleccionar modulo minimo.
3. Plan corto.
4. Ejecutar.
5. Verificacion proporcional.
6. Documentar solo si el cambio deja conocimiento duradero.

Gates:

- Final Verification siempre proporcional.
- Requirements Quality solo si hay ambiguedad.
- Implementation Review solo si hay diff con riesgo.
- Decision Readiness normalmente no.

No usar:

- `grill-with-docs` por defecto.
- `subagent-driven-development`.
- `to-prd/to-issues`.
- `improve-codebase-architecture`.

### 12.2 Proyecto mediano

Ejemplos:

- Nueva API.
- Modulo Python industrial.
- Integracion PLC-app con alcance acotado.

Flujo:

1. Discovery ligero o requirements.
2. Requirements Quality Gate.
3. Decision Readiness si hay alternativas.
4. Arquitectura breve + ADRs necesarios.
5. Plan de implementacion.
6. Seleccion de agentes 1-3.
7. Implementacion.
8. Tests/debug.
9. Implementation Review.
10. Final Verification.
11. Documentacion necesaria.

Gates:

- Requirements Quality.
- Implementation Review.
- Final Verification.
- Decision Readiness condicionado a incertidumbre.

No usar:

- `continuous-learning-v2`.
- `agent-eval`.
- Worktrees salvo paralelo real.

### 12.3 Proyecto grande

Ejemplos:

- Celula robotizada con vision, PLC, Python y datos.
- Plataforma industrial multi-componente.
- Migracion arquitectonica amplia.

Flujo:

1. `industrial-project-discovery`.
2. Requirements Quality Gate con `grill-with-docs`.
3. Decision Readiness Gate.
4. Investigacion/prototipo si hay incertidumbre.
5. Arquitectura por capas.
6. ADRs.
7. Plan de implementacion.
8. PRD/issues si se necesita division formal.
9. Seleccion de agentes.
10. Seleccion de skills.
11. Worktrees/subagentes si hay paralelo real.
12. Implementacion por incrementos.
13. Tests, simulacion y debugging.
14. Implementation Review.
15. Industrial Project Verification.
16. Final Verification.
17. Documentacion y lecciones aprendidas.

Gates:

- Los cuatro gates obligatorios.

No usar:

- Prototipo como codigo de produccion.
- Aprendizaje continuo automatico sin aprobacion.
- Skills no auditadas.

## 13. Politicas de no uso

No usar una skill cuando:

- Su trigger no aplica.
- Su output no tiene consumidor.
- Duplica un gate activo.
- Tiene coste alto para una tarea pequena.
- Requiere herramientas no disponibles.
- Tiene side effects no autorizados.

No usar un gate cuando:

- No hay artefacto que evaluar, excepto Final Verification antes de claims.
- La fase no corresponde al gate.
- El proyecto es pequeno y el gate seria ceremonia sin reducir riesgo.

No usar un modulo cuando:

- La tecnologia/dominio no aplica.
- Solo aparece como contexto futuro.
- Activarlo cargaria instrucciones irrelevantes.

No usar un agente cuando:

- Su dominio no esta activo.
- Su responsabilidad ya esta cubierta por otro agente seleccionado.
- No hay output claro que producir.

## 14. ADR policy

En esta fase no se crean ADRs separados para evitar construir estructura antes de Fase 3.

ADRs recomendados para fases posteriores:

- ADR-0001: Arquitectura por cinco capas.
- ADR-0002: Global Core minimo y biblioteca opcional.
- ADR-0003: Decision Readiness Gate propio.
- ADR-0004: Politica de precedencia.
- ADR-0005: Separacion entre verification general e industrial verification.

Crear ADR solo cuando:

- La decision sea dificil de revertir.
- Existan alternativas reales.
- Un futuro agente podria reabrir la decision sin contexto.

## 15. Coherencia contra SKILLS_AUDIT.md

Checklist:

- Ausencia de duplicidades evidentes: PASS. `brainstorming` no se combina con `grill-with-docs` en core; `requesting-code-review` no compite con `code-review`; `test-driven-development` no se duplica con matt `tdd`.
- Global Core minimo: PASS. Solo principios de `agentic-engineering`, `writing-plans`, `systematic-debugging`.
- Gates con responsabilidades separadas: PASS. Requirements, decisions, implementation review y final verification tienen inputs/outputs distintos.
- Modulos activables: PASS. Cada modulo define cuando activar y cuando no.
- Agentes con limites claros: PASS. Se definen misiones y limites sin crear archivos definitivos.
- Custom industrial skills ubicadas: PASS. Se asignan a capa 4 y a modulos/gates. Implementadas en Fases 7A-7D.
- Politica de precedencia definida: PASS.
- Workflows proporcionales: PASS. Pequeno, mediano y grande no ejecutan el mismo flujo completo.

## 16. Riesgos y decisiones pendientes

> Nota (Fase 9A): Esta seccion refleja el estado al final de Fase 2. Los
> riesgos marcados como resueltos se actualizan a continuacion.

Riesgos:

- `gh` sigue sin autenticacion valida; flujos PR/remoto deben esperar.
- ~~Repo sin commits; worktrees y branch finishing no deben activarse aun.~~ Resuelto: el repo tiene historial de commits desde Fase 3.
- Python/Node globales no son fiables; futuras herramientas deben documentar runtimes.
- ~~Decision Readiness Gate aun debe implementarse como artefacto propio en Fase 5.~~ Resuelto: implementado en Fase 5 con `gates/decision-readiness/GATE.md`.
- Falta definir formato exacto de ADR, templates y rutas finales. Parcialmente resuelto: ADRs se usan via `architecture-decision-records`; templates no se han creado (pendiente).

Decisiones pendientes:

- Formato final de `AGENTS.md`.
- Ubicacion final de gates, agentes, modulos, templates y custom skills.
- Si se adoptara algun instalador o solo referencias documentadas.
- Si `continuous-learning-v2` tendra piloto controlado en Fase 12.

## 17. Estado final de Fase 2

> Nota (Fase 9A): Esta seccion preserva el estado historico al final de Fase 2.
> El estado actual del stack es: 4 gates, 6 agentes, 9 skills y 8 modulos
> implementados (Fases 3-8). Ver `README.md` y `STACK_COHERENCE_AUDIT.md`
> para el estado vigente.

Archivos creados:

- `ARCHITECTURE.md`

Archivos modificados:

- Ninguno adicional.

Instalaciones realizadas:

- Ninguna.

Configuracion global modificada:

- Ninguna.

Siguiente fase propuesta:

- Fase 3 - Creacion del repositorio base.

Detener aqui y esperar autorizacion antes de continuar.
