# Specialized Agents

## Que es un agente especializado

Un agente especializado es un contrato operativo de responsabilidad, delegacion
y handoff. No es una skill, no es un modulo, no es un gate. Cada agente tiene un
dominio principal delimitado, responsabilidades explicitas y non-responsibilities
que evitan que se convierta en omnisciente.

## Por que no todos los proyectos necesitan todos los agentes

La seleccion de agentes sigue el flujo definido en `AGENTS.md` y
`ARCHITECTURE.md`:

```text
PROJECT
  -> RISK / COMPLEXITY ANALYSIS
  -> MODULE SELECTION
  -> AGENT SELECTION
  -> SKILL SELECTION
  -> GATES
  -> EXECUTION
```

- **Proyectos pequenos**: normalmente 1 agente o ninguno (ejecucion directa con
  verificacion proporcional).
- **Proyectos medianos**: 1-3 agentes segun dominio.
- **Proyectos grandes**: Engineering Architect coordina + especialistas segun
  dominio + QA & Debug + Technical Documentation.

Regla: seleccionar agentes por responsabilidad, no por disponibilidad. Un agente
entra solo si su dominio esta activo y tiene un output claro que producir.

## Los seis agentes

| Agente | Dominio principal |
|---|---|
| Engineering Architect | Coordinacion tecnica, coherencia global, gates |
| Industrial Automation Engineer | PLC, automatizacion, comunicaciones industriales |
| Robotics Engineer | Robotica, integracion robot-PLC, trayectorias |
| Software Engineer | Software, APIs, backend, integracion |
| QA & Debug Engineer | Testing, debugging, verificacion, evidencia |
| Technical Documentation Engineer | Documentacion, ADRs, glosarios, manuales |

## Seleccion proporcional

Engineering Architect coordina proyectos medianos y grandes. Los especialistas
participan solo cuando su dominio esta activo. QA & Debug entra cuando hay
implementacion, debug o verificacion. Technical Documentation entra cuando hay
outputs duraderos.

## Artifact Ownership

Todo artefacto relevante debe tener:

- **Owner**: responsable de coherencia, integracion, mantenimiento y handoff.
- **Contributors** (opcionales): aportan contenido parcial.
- **Reviewer** (cuando aplique): verifica calidad del artefacto.
- **Consumer/Handoff target**: quien recibe el artefacto.

El owner responde de coherencia e integra contribuciones, pero no necesariamente
crea todo el contenido personalmente. Se evita ownership compartido ambiguo: si
un artefacto cruza dominios, un owner principal y contributors claramente
identificados.

## Delegation Contract

Toda delegacion debe definir:

- Task (tarea concreta).
- Context (por que se delega).
- Required Inputs (que necesita el delegado).
- Expected Output (que debe producir).
- Constraints (limites y restricciones).
- Verification Method (como se verifica el output).
- Done Criteria (criterio de completitud).
- Handoff Target (a quien se entrega).

Un agente no debe delegar una tarea sin output verificable.

## Handoff Contract

Todo handoff relevante debe incluir:

- Artefacto producido.
- Estado (draft/reviewed/approved).
- Evidencia (tests, checks, inspecciones).
- Decisiones tomadas.
- Decisiones pendientes.
- Riesgos.
- Siguiente owner.

Se evitan handoffs conversacionales ambiguos. Todo handoff debe ser trazable.

## Escalation Policy

Escalar cuando:

- Una decision cruza dominios.
- Existe conflicto entre especialistas.
- Falta evidencia.
- El riesgo supera el dominio del agente.
- Una desviacion afecta arquitectura.
- Existe incertidumbre critica.
- Se requiere decision del usuario.

Escalation targets:

- Arquitectura/transversal -> Engineering Architect.
- Verificacion/calidad -> QA & Debug Engineer.
- Dominio especializado -> especialista correspondiente.
- Requisito externo/preferencia -> usuario.

## Relacion con gates, modulos y skills

- **Gates**: los agentes participan en gates segun su rol. Engineering Architect
  lidera Requirements Quality y Decision Readiness. QA & Debug Engineer lidera
  Implementation Review y Final Verification. Los especialistas participan segun
  dominio. Ningun agente puede autoaprobar su propio Final Verification.
- **Modulos**: los agentes se activan segun los modulos seleccionados para el
  proyecto. Un modulo define que skills y agentes son relevantes.
- **Skills**: cada agente puede recomendar skills bajo demanda. Toda skill
  activada debe tener trigger, input, output, consumer y stop condition. Los
  agentes no pueden usar skills para saltarse gates.

## Referencias

- `AGENTS.md` -- Agent Policy (constitucion).
- `ARCHITECTURE.md` -- Seccion 9: Arquitectura de agentes.
- `ARCHITECTURE.md` -- Seccion 10.4: Agent Selection.
- `gates/README.md` -- Engineering Gates.
