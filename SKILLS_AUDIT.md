# ROBER ENGINEERING STACK v1.0 - Skills Audit

Fecha: 2026-07-07  
Fase: 1 - Investigacion y auditoria de skills  
Estado: completada sin instalaciones

## 1. Alcance y base usada

Esta auditoria toma `ENVIRONMENT_AUDIT.md` como estado base. No se modifico configuracion global, no se instalaron skills y no se corrigieron problemas de entorno detectados en Fase 0.

Fuentes inspeccionadas:

- obra / Superpowers: `https://github.com/obra/superpowers`
- affaan-m / ECC: `https://github.com/affaan-m/ECC`
- mattpocock / Skills: `https://github.com/mattpocock/skills`
- Cache local Codex SkillsMP: `C:\Users\roarpe\.codex\cache\remote_plugin_catalog\e3a4a3e6779d096c.json`

Limitaciones:

- `gh` esta instalado pero no autenticado; se uso web y cache local en lugar de GitHub CLI.
- Algunas skills del MASTER PROMPT no existen con ese nombre exacto en los repos actuales inspeccionados.
- No se clono ningun repositorio y no se instalo ningun paquete.

## 2. Evidencia de origen

### obra - Superpowers

Repositorio original: `https://github.com/obra/superpowers`

Evidencia inspeccionada:

- El README describe Superpowers como una metodologia de desarrollo basada en skills componibles para agentes, con flujo de brainstorming, planificacion, TDD, debugging, revision y finalizacion.
- El README lista el Basic Workflow: `brainstorming`, `using-git-worktrees`, `writing-plans`, `subagent-driven-development` o `executing-plans`, `test-driven-development`, `requesting-code-review`, `finishing-a-development-branch`.
- La carpeta `skills/` contiene actualmente: `brainstorming`, `dispatching-parallel-agents`, `executing-plans`, `finishing-a-development-branch`, `receiving-code-review`, `requesting-code-review`, `subagent-driven-development`, `systematic-debugging`, `test-driven-development`, `using-git-worktrees`, `using-superpowers`, `verification-before-completion`, `writing-plans`, `writing-skills`.
- La cache local de SkillsMP contiene el plugin `superpowers`, version `6.1.1`, website `https://github.com/obra/superpowers`, developer `Jesse Vincent`, y descripcion de workflow.

Notas:

- `maintaining-documentation` y `writing-clearly-and-concisely` no se encontraron como skills actuales en `obra/superpowers/skills`.
- `brainstorming` exige aprobacion del diseno antes de implementar y escribe specs en `docs/superpowers/specs/`.
- `test-driven-development` impone TDD estricto y excepciones solo con consentimiento humano.
- `verification-before-completion` impone evidencia fresca antes de declarar exito.

### affaan-m - ECC

Repositorio original: `https://github.com/affaan-m/ECC`

Evidencia inspeccionada:

- El README define ECC como un sistema de optimizacion de harness de agentes con skills, instincts, memoria, seguridad, learning continuo y desarrollo research-first.
- El README indica que ECC 2.0.0 contiene una superficie amplia: cientos de skills, agentes y command shims.
- La carpeta `skills/` incluye las candidatas: `continuous-learning-v2`, `agentic-engineering`, `agent-sort`, `agent-harness-construction`, `agent-eval`, `skill-stocktake`, `api-design`, `architecture-decision-records`.

Notas:

- ECC es potente pero grande. Adoptar demasiado ECC como core global contradice el objetivo del stack de mantener pocas instrucciones activas.
- `continuous-learning-v2` usa hooks y almacenamiento externo para observaciones/instincts; es valioso pero tiene impacto operativo alto.
- `agent-sort` y `skill-stocktake` son especialmente relevantes para controlar ruido, duplicidad y carga contextual.

### mattpocock - Skills

Repositorio original: `https://github.com/mattpocock/skills`

Evidencia inspeccionada:

- El README describe "Skills for Real Engineers" y afirma que son pequenas, adaptables y componibles.
- La seccion Engineering distingue skills user-invoked y model-invoked.
- Skills relevantes encontradas:
  - `grill-with-docs`
  - `prototype`
  - `improve-codebase-architecture`
  - `code-review`
  - `to-prd`
  - `to-issues`
  - `domain-modeling`
  - `codebase-design`
- El nombre `review` del MASTER PROMPT corresponde funcionalmente a `code-review`.
- El nombre `prd-to-issues` corresponde mejor a la combinacion `to-prd` + `to-issues`, no a una skill unica con ese nombre.
- `decision-mapping` no se encontro en el repo actual; la funcionalidad parcial mas cercana es `grilling` + `domain-modeling` + ADRs, pero no es equivalente.

## 3. Clasificacion recomendada

Categorias usadas:

- `GLOBAL CORE`: activa en casi todos los proyectos.
- `ENGINEERING GATE`: se activa en puntos concretos del flujo.
- `PROJECT MODULE`: se activa por tipo/fase de proyecto.
- `OPTIONAL LIBRARY`: disponible bajo demanda, no activa por defecto.
- `EXPERIMENTAL`: prometedora pero requiere piloto/control.
- `REJECTED`: no adoptar ahora.

Recomendacion central: el Global Core debe ser pequeno. Para v1.0 se recomienda no cargar paquetes completos como core global. En su lugar, definir gates y modulos que invoquen skills concretas cuando correspondan.

## 4. Matriz de decision

| Skill candidata | Creador | Repo origen | Proposito | Clasificacion | Coste contexto | Compatibilidad | Solapamientos/conflictos | Decision tecnica |
|---|---|---|---|---|---:|---|---|---|
| brainstorming | obra | obra/superpowers | Convertir idea en diseno/spec antes de implementar | OPTIONAL LIBRARY | Alto | Alta | Solapa con `grill-with-docs` y discovery industrial | No Global Core. Usar como alternativa creativa cuando no se use discovery/grilling. |
| writing-plans | obra | obra/superpowers | Crear plan de implementacion exacto y verificable | GLOBAL CORE | Medio | Alta | Solapa parcialmente con `to-issues`; puede ser demasiado prescriptiva | Adoptar el principio, no necesariamente rutas `docs/superpowers`. |
| executing-plans | obra | obra/superpowers | Ejecutar planes con checkpoints | OPTIONAL LIBRARY | Medio | Alta | Solapa con subagent-driven-development | Mantener como fallback si no hay subagentes o si el plan es lineal. |
| subagent-driven-development | obra | obra/superpowers | Ejecutar tareas con subagentes frescos y revisiones por tarea | PROJECT MODULE | Alto | Media-Alta | Requiere subagentes; puede entrar en conflicto con fases que piden detenerse | Usar solo en proyectos con plan aprobado y trabajo paralelo claro. |
| systematic-debugging | obra | obra/superpowers | Debugging con causa raiz antes de fixes | GLOBAL CORE | Medio | Alta | Solapa con `diagnosing-bugs` de mattpocock | Adoptar como disciplina base; evitar duplicar con diagnosing-bugs en core. |
| test-driven-development | obra | obra/superpowers | TDD red-green-refactor estricto | PROJECT MODULE | Medio | Alta | Solapa con `tdd` de mattpocock; puede ser excesivo para prototipos/PLC docs | Activar por modulo de software; no forzar en prototipos ni docs. |
| verification-before-completion | obra | obra/superpowers | Exigir evidencia fresca antes de afirmar completitud | ENGINEERING GATE | Bajo | Alta | Solapa con custom `industrial-project-verification` | Adoptar como Final Verification Gate generico. |
| requesting-code-review | obra | obra/superpowers | Solicitar review con contexto acotado | OPTIONAL LIBRARY | Medio | Media | Solapa con matt `code-review`; depende de subagentes | No usar como gate principal si se adopta `code-review`. |
| maintaining-documentation | obra | No encontrada en repo actual | Supuesta disciplina documental | REJECTED | Desconocido | Desconocida | Solapa con custom `industrial-documentation` | Rechazar hasta localizar fuente real. |
| using-git-worktrees | obra | obra/superpowers | Aislar trabajo en worktrees | PROJECT MODULE | Medio | Media | Puede chocar con workspace gestionado por Codex o sandbox | Usar solo cuando haya trabajo paralelo y despues de detectar aislamiento. |
| finishing-a-development-branch | obra | obra/superpowers | Cierre de rama con tests, merge/PR/cleanup | OPTIONAL LIBRARY | Medio | Media | Requiere Git/gh sano; gh token invalido ahora | Mantener para fase Git/PR, no core inicial. |
| writing-clearly-and-concisely | obra | No encontrada en repo actual | Escritura clara | REJECTED | Desconocido | Desconocida | Solapa con reglas de documentacion propias | Rechazar hasta localizar fuente real. |
| continuous-learning-v2 | affaan-m | affaan-m/ECC | Aprendizaje por hooks, instincts y scoping por proyecto | EXPERIMENTAL | Alto | Baja-Media | Puede modificar conocimiento operativo; riesgo de contaminacion si mal configurado | No instalar en v1 core. Evaluar despues de piloto y con aprobacion explicita. |
| agentic-engineering | affaan-m | affaan-m/ECC | Decomposicion, eval-first, model routing y control de costes | GLOBAL CORE | Bajo | Alta | Solapa con workflow propio; complementa gates | Adoptar como principio sintetizado en AGENTS.md, no como paquete amplio. |
| agent-sort | affaan-m | affaan-m/ECC | Clasificar superficies DAILY vs LIBRARY con evidencia de repo | ENGINEERING GATE | Medio | Alta | Solapa con esta auditoria y `skill-stocktake` | Adoptar como gate de seleccion de skills/modulos, bajo demanda. |
| agent-harness-construction | affaan-m | affaan-m/ECC | Disenar herramientas, observaciones y recuperacion de agentes | OPTIONAL LIBRARY | Bajo-Medio | Alta | Solapa con arquitectura de agentes | Usar cuando se disenen herramientas/agentes propios, no en proyectos normales. |
| agent-eval | affaan-m | affaan-m/ECC | Comparar agentes con tareas reproducibles | EXPERIMENTAL | Medio | Media | Requiere CLI externo/repos; puede distraer del stack inicial | Mantener para Fase 12 o evaluacion avanzada. |
| skill-stocktake | affaan-m | affaan-m/ECC | Auditar skills por calidad, solape, frescura y uso | ENGINEERING GATE | Medio-Alto | Media | Solapa con `agent-sort`; orientada a rutas `.claude` | Adoptar como auditoria periodica, no como core activo. |
| api-design | affaan-m | affaan-m/ECC | Patrones REST API: recursos, errores, paginacion, versionado | PROJECT MODULE | Medio | Alta | Solapa con standards backend propios | Usar en modulos software/web/data con APIs. |
| architecture-decision-records | affaan-m | affaan-m/ECC | Capturar ADRs estructurados | PROJECT MODULE | Bajo-Medio | Alta | Solapa con `domain-modeling` ADRs de matt | Adoptar como modulo/documentacion; definir formato unico en Fase 2. |
| grill-with-docs | mattpocock | mattpocock/skills | Entrevista + docs: domain model, ADRs, glossary | ENGINEERING GATE | Medio | Alta | Solapa con `brainstorming` y discovery industrial | Adoptar como Requirements Quality Gate, invocado manualmente. |
| decision-mapping | mattpocock | No encontrada en repo actual | Mapa de decisiones pendientes | REJECTED | Desconocido | Desconocida | Parcialmente cubierto por `grilling`, ADRs y custom gates | Rechazar hasta localizar fuente real; disenar gate propio si es necesario. |
| review | mattpocock | Alias probable: `code-review` | Review de diff contra standards y spec | ENGINEERING GATE | Medio-Alto | Alta | Solapa con obra `requesting-code-review`; requiere subagentes para paralelismo ideal | Adoptar `code-review` como Implementation Review Gate. |
| prototype | mattpocock | mattpocock/skills | Prototipo desechable para responder preguntas de diseno | PROJECT MODULE | Medio | Alta | Conflicto con TDD si se trata como produccion | Adoptar con politica clara: throwaway, sin convertir automaticamente en produccion. |
| prd-to-issues | mattpocock | Alias: `to-prd` + `to-issues` | PRD y division en issues verticales | PROJECT MODULE | Medio | Media | Solapa con `writing-plans`; depende de issue tracker | Adoptar como modulo opcional para proyectos que requieran backlog formal. |
| improve-codebase-architecture | mattpocock | mattpocock/skills | Detectar oportunidades de profundizar arquitectura | PROJECT MODULE | Alto | Media | Produce HTML con CDN; puede abrir GUI; solapa con arquitectura propia | Usar bajo demanda en repos con codigo existente, no en core. |

## 5. Recomendaciones principales

### 5.1 Global Core propuesto

No instalar aun. Para Fase 2, disenar el core con estas capacidades como principios o skills invocables:

- `agentic-engineering`: por su bajo coste y utilidad transversal para decomposicion, eval-first y control de coste.
- `writing-plans`: para convertir arquitectura/spec en tareas verificables.
- `systematic-debugging`: disciplina universal para bugs, fallos de tests e integraciones.

No incluir en Global Core:

- `brainstorming`, porque es potente pero agresivo: exige diseno y aprobacion para cualquier trabajo creativo y solapa con `industrial-project-discovery` y `grill-with-docs`.
- `test-driven-development`, porque debe activarse por modulo/proyecto; no todo artefacto industrial o documental requiere TDD.
- `subagent-driven-development`, porque depende de trabajo dividido y de disponibilidad de subagentes.
- `continuous-learning-v2`, porque modifica aprendizaje operativo mediante hooks y requiere gobernanza.

### 5.2 Engineering Gates propuestos

GATE 1 - Requirements Quality:

- Skill candidata: `grill-with-docs`
- Justificacion: fuerza entrevista, shared language, ADRs y glossary; encaja con `industrial-project-discovery`.
- Riesgo: puede ser demasiado conversacional; debe tener trigger claro y output esperado.

GATE 2 - Decision Readiness:

- Skill candidata original `decision-mapping`: no encontrada.
- Recomendacion: crear gate propio en Fase 5 inspirado en el MASTER PROMPT, usando ADRs y una matriz de decisiones.
- Skills auxiliares: `grilling`, `domain-modeling`, `architecture-decision-records`.

GATE 3 - Implementation Review:

- Skill candidata: `code-review` de mattpocock, mapeada desde `review`.
- Justificacion: separa standards y spec, evitando que un eje oculte al otro.
- Riesgo: idealmente requiere subagentes; si no hay, ejecutar secuencialmente.

GATE 4 - Final Verification:

- Skill candidata: `verification-before-completion`.
- Justificacion: pequena, clara, evidencia antes de afirmar estado.
- Riesgo: no sustituye verificaciones industriales especificas; debe complementarse con custom `industrial-project-verification`.

### 5.3 Project Modules propuestos

- `prototype`: modulo para incertidumbre tecnica, no produccion.
- `to-prd` + `to-issues`: modulo para backlog formal y trabajo distribuido.
- `using-git-worktrees`: modulo para trabajo paralelo, con deteccion de aislamiento.
- `finishing-a-development-branch`: modulo Git/PR, condicionado a resolver autenticacion de `gh`.
- `api-design`: modulo software/web/data.
- `architecture-decision-records`: modulo transversal de arquitectura/documentacion.
- `improve-codebase-architecture`: modulo para repos existentes con deuda o friccion arquitectonica.

### 5.4 Optional Library

Mantener como biblioteca, no core:

- `brainstorming`
- `executing-plans`
- `requesting-code-review`
- `agent-harness-construction`
- `agent-eval`
- skills no candidatas pero cercanas: matt `domain-modeling`, `codebase-design`, `research`, obra `writing-skills`

### 5.5 Experimental

- `continuous-learning-v2`: requiere piloto, revision de hooks, rutas de datos y politica de promocion de conocimiento.
- `agent-eval`: util para comparar agentes en Fase 12, no para construir v1 base.

### 5.6 Rejected por ahora

- `decision-mapping`: no localizada en `mattpocock/skills`; no adoptar por nombre.
- `maintaining-documentation`: no localizada en `obra/superpowers`; cubrir con custom `industrial-documentation`.
- `writing-clearly-and-concisely`: no localizada en `obra/superpowers`; cubrir con criterios documentales propios.

## 6. Duplicidades, solapamientos y conflictos

### Requirements y discovery

- `brainstorming` y `grill-with-docs` resuelven alineacion inicial.
- Para ROBER ENGINEERING STACK, `industrial-project-discovery` debe producir `PROJECT_DISCOVERY.md`; despues `grill-with-docs` puede actuar como gate.
- Decision: no cargar ambas como core. Usar `grill-with-docs` como gate y dejar `brainstorming` como biblioteca opcional.

### Planning y backlog

- `writing-plans` produce planes detallados con pasos, archivos, tests y commits.
- `to-prd` y `to-issues` producen PRD e issues verticales en tracker.
- Decision: `writing-plans` para ejecucion tecnica; `to-prd/to-issues` solo cuando se necesite backlog formal o trabajo AFK distribuido.

### TDD

- Obra `test-driven-development` y matt `tdd` cubren el mismo principio.
- Decision: elegir un unico estilo en Fase 2. Recomendacion inicial: usar obra `test-driven-development` como referencia generica, y no instalar matt `tdd` salvo que se adopte todo el ecosistema matt.

### Debugging

- Obra `systematic-debugging` y matt `diagnosing-bugs` solapan.
- Decision: usar obra `systematic-debugging` como core por ser explicita en causa raiz y verificacion; mantener matt `diagnosing-bugs` fuera del set candidato.

### Review

- Obra `requesting-code-review` se centra en solicitar review con subagente.
- Matt `code-review` estructura dos ejes: standards y spec.
- Decision: usar matt `code-review` como gate de implementation review; dejar obra `requesting-code-review` como patron opcional para subagent workflows.

### ADR y domain model

- ECC `architecture-decision-records` y matt `domain-modeling`/`grill-with-docs` pueden escribir ADRs.
- Decision: en Fase 2 definir un formato unico de ADR y una sola ubicacion. Las skills externas no deben crear formatos paralelos.

### Continuous learning

- ECC `continuous-learning-v2` podria evolucionar instrucciones automaticamente.
- Conflicto con MASTER PROMPT: no contaminar conocimiento global ni modificar reglas por una sola experiencia.
- Decision: experimental. Solo usar tras definir politica de aprobacion manual.

### Git worktrees

- Obra `using-git-worktrees` y `finishing-a-development-branch` son utiles pero operativos.
- Conflictos con entorno: repo sin commits, Git global con warning de ignore, `gh` token invalido, Codex puede gestionar worktrees nativamente.
- Decision: no activar hasta Fase 3+ y no usar sin detectar aislamiento.

### Context cost

- Coste alto: `subagent-driven-development`, `improve-codebase-architecture`, `continuous-learning-v2`, `skill-stocktake`.
- Coste medio: `brainstorming`, `writing-plans`, `test-driven-development`, `code-review`, `to-prd/to-issues`, `agent-sort`.
- Coste bajo: `verification-before-completion`, `agentic-engineering`, `architecture-decision-records` si se mantiene breve.

Regla recomendada: ninguna skill de coste alto debe ser global.

## 7. Riesgos especificos para ROBER ENGINEERING STACK

| Riesgo | Fuente | Impacto | Mitigacion |
|---|---|---:|---|
| Core demasiado grande | Superpowers + ECC + matt completos | Alto | Seleccionar skills concretas, no paquetes completos |
| Flujos que no se detienen | `subagent-driven-development` | Alto | Activar solo despues de plan aprobado y fase habilitada |
| Aprendizaje no gobernado | `continuous-learning-v2` | Alto | Requerir aprobacion humana y scoping por proyecto |
| Formatos documentales divergentes | ADRs de ECC + matt + custom docs | Medio | Definir formato unico en Fase 2 |
| Dependencia de issue tracker | `to-prd`, `to-issues`, `code-review` spec lookup | Medio | Permitir fallback a archivos locales en `docs/` |
| Dependencia de browser/CDN | `improve-codebase-architecture` | Medio | Mantener opcional; no usar en entornos offline |
| Worktree no controlado | `using-git-worktrees` | Medio | Detectar aislamiento y pedir consentimiento |
| Nombres no encontrados | `decision-mapping`, `maintaining-documentation`, `writing-clearly-and-concisely` | Medio | No adoptar por nombre; crear equivalents propios si son necesarios |

## 8. Decision de no instalacion

No se recomienda instalar nada todavia.

Motivos:

1. Fase 1 es auditoria, no adopcion.
2. El repo aun no tiene arquitectura ni `AGENTS.md` raiz.
3. Varias skills tienen side effects esperados sobre docs, worktrees, hooks o issue trackers.
4. El entorno GitHub no esta listo para flujos remotos (`gh` token invalido).
5. El objetivo del stack exige separar core, gates, modulos, custom industrial skills y biblioteca opcional.

## 9. Plan recomendado para Fase 2

En Fase 2, disenar `ARCHITECTURE.md` con:

1. Core pequeno basado en principios: `agentic-engineering`, `writing-plans`, `systematic-debugging`.
2. Gates explicitos:
   - Requirements Quality: `grill-with-docs`
   - Decision Readiness: gate propio, porque `decision-mapping` no fue localizado
   - Implementation Review: `code-review`
   - Final Verification: `verification-before-completion`
3. Modulos activables por tipo de proyecto:
   - software/web/API: `api-design`, TDD, `to-prd/to-issues`
   - arquitectura existente: `improve-codebase-architecture`
   - incertidumbre tecnica: `prototype`
   - paralelo/Git: `using-git-worktrees`, `finishing-a-development-branch`
4. Politica de biblioteca opcional usando conceptos de `agent-sort` y `skill-stocktake`.
5. Politica de aprendizaje continuo alineada con el MASTER PROMPT antes de tocar `continuous-learning-v2`.

## 10. Verificaciones ejecutadas

Comprobaciones locales:

- Lectura de `ENVIRONMENT_AUDIT.md`.
- `git status --short`.
- Busqueda en cache local Codex SkillsMP.
- Busqueda local de metadatos de skills y plugins.

Comprobaciones web:

- Inspeccion de `https://github.com/obra/superpowers`.
- Inspeccion de raw `SKILL.md` de skills clave de obra.
- Inspeccion de `https://github.com/affaan-m/ECC`.
- Inspeccion de raw `SKILL.md` de skills clave de ECC.
- Inspeccion de `https://github.com/mattpocock/skills`.
- Inspeccion de raw `SKILL.md` de skills clave de mattpocock.

## 11. Estado final de Fase 1

Fase 1 completada.

Archivos creados:

- `SKILLS_AUDIT.md`

Archivos modificados:

- Ninguno adicional.

Instalaciones realizadas:

- Ninguna.

Configuracion global modificada:

- Ninguna.

Siguiente fase propuesta:

- Fase 2 - Diseno de arquitectura.

Detener aqui y esperar autorizacion antes de continuar.

---

## Evolucion arquitectonica posterior a la auditoria

Esta seccion documenta decisiones arquitectonicas posteriores a la Fase 1. No
altera las conclusiones historicas de la auditoria original.

- La auditoria original (Fase 1) evaluo la arquitectura inicial de 8 Custom
  Industrial Skills.
- Durante la Fase 7B se incorporo oficialmente una novena skill:
  `vision-ai-integration`, con su contrato completo en
  `skills/vision-ai-integration/SKILL.md`.
- `robot-cell-integration` fue renombrada oficialmente a
  `robotics-cell-integration` durante la Fase 7B. El nombre canonico es
  `robotics-cell-integration`.
- Estas son evoluciones arquitectonicas posteriores, no hallazgos retroactivos
  de la auditoria original.
- `vision-ai-integration` debera validarse mediante las fases posteriores de
  testing (Fase 10) y piloto (Fase 11) igual que el resto del stack.
