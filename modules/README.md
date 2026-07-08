# Project Modules

## Que es un Project Module

Un Project Module es un mecanismo de seleccion y composicion proporcional de
Gates, Agents y Skills ya existentes. No es un agente, no es una skill, no es
un gate, no es un workflow rigido. Su funcion es responder:

- Que dominios participan en un proyecto.
- Que agentes son relevantes.
- Que skills pueden activarse.
- Que gates deben considerarse.
- Que artefactos pueden producirse.
- Que interfaces entre dominios requieren atencion.
- Que riesgos justifican ampliar o reducir el stack activo.

## Que no es un Project Module

- No es un agente: no tiene mission, no toma decisiones tecnicas.
- No es una skill: no tiene procedure, no produce artefactos.
- No es un gate: no evalua, no decide PASS/FAIL.
- No es un workflow: no prescribe orden exacto de ejecucion.
- No duplica contratos: referencia agentes, skills y gates existentes.

## Principio fundamental

Un modulo selecciona y compone. No ejecuta por si mismo. No posee artefactos
tecnicos. No sustituye agentes, skills o gates. El ownership permanece en el
agente, gate o skill correspondiente.

## Los ocho modulos

| Modulo | Dominio | Primary Agent |
|---|---|---|
| software-development | Software, APIs, backend, integracion | Software Engineer |
| industrial-automation | PLC, automatizacion, comunicaciones OT | Industrial Automation Engineer |
| robotics | Robotica, integracion robot-PLC, celulas | Robotics Engineer |
| artificial-intelligence | IA aplicada, inferencia, modelos | Software Engineer |
| computer-vision | Vision, inspeccion, metrologia | Software Engineer o Robotics Engineer |
| data-engineering | Datos, pipelines, analytics | Software Engineer |
| web-development | Web, dashboards, APIs web | Software Engineer |
| git-parallel-delivery | Trabajo paralelo, worktrees, integracion | Engineering Architect |

## Seleccion

La seleccion de modulos sigue el flujo definido en `AGENTS.md` y
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

- Seleccionar solo modulos cuyo dominio esta activo.
- Un modulo no se activa si su tecnologia no aplica o solo aparece como
  contexto futuro.
- La activacion de un modulo no activa automaticamente todas sus skills.
- Un modulo especializado cubre su dominio sin requerir automaticamente un
  modulo mas general. `software-development` es complementario: no se activa
  por defecto cuando `web-development` o `data-engineering` cubren el dominio.
- `computer-vision` puede operar solo incluso con inferencia visual; se activa
  `artificial-intelligence` solo cuando hay responsabilidades de IA
  independientes o significativas.

## Composicion

Un proyecto puede activar varios modulos. Cuando varios modulos estan activos:

- Cada dominio conserva su ownership.
- Engineering Architect coordina dependencias transversales cuando sea
  necesario.
- Las interfaces entre dominios usan contracts explicitos.
- Las skills compartidas se activan una sola vez por necesidad, no una vez por
  modulo.
- Los gates evaluan el proyecto o artefacto relevante, no cada modulo
  mecanicamente.
- Se evita duplicacion de documentacion y artefactos.

### Ejemplo de composicion multimodulo

Celula robotizada con PLC + robot + vision + software:

```text
industrial-automation + robotics + computer-vision + software-development
```

Esto NO significa activar automaticamente todas las skills de los cuatro
modulos. Significa que los agentes relevantes (IAE, RE, SE, EA) participan, y
las skills se activan por trigger concreto.

## Proporcionalidad

Cada modulo define comportamiento para Small, Medium y Large/High-Risk:

- **Small**: minimo contexto, minimo agentes, skills solo por trigger, gates
  proporcionales.
- **Medium**: coordinacion explicita, interfaces definidas, agentes
  especializados relevantes, gates RQ/IR normalmente aplicables.
- **Large/High-Risk**: Engineering Architect, multiples agentes, decisiones
  explicitas, skills segun necesidad, gates completos, trazabilidad,
  verificacion transversal.

## Ownership

El ownership de artefactos permanece en agentes, gates y skills. Un modulo no
es owner de ningun artefacto tecnico. Un modulo solo indica que agentes, skills
y gates son relevantes para su dominio.

## Relacion con agentes, skills y gates

- **Agentes**: el modulo indica que agentes son primary y optional. Los agentes
  se activan segun su propio contrato (AGENT.md), no por el modulo.
- **Skills**: el modulo indica que skills son relevantes. Las skills se activan
  por trigger (SKILL.md), no por el modulo.
- **Gates**: el modulo indica que gates son typically required, conditional o
  potentially unnecessary. Los gates se activan segun proporcionalidad
  (GATE.md), no por el modulo.

## Context Cost

Los modulos reducen coste contextual. Al activar solo los modulos relevantes,
se evita cargar agentes, skills, gates y procedimientos de dominios que no
aplican al proyecto.

## Referencias

- `AGENTS.md` -- Constitucion operativa, seleccion proporcional.
- `ARCHITECTURE.md` -- Seccion 6: Project Modules (definicion arquitectonica).
- `ARCHITECTURE.md` -- Seccion 10: Mecanismo de seleccion.
- `gates/README.md` -- Engineering Gates.
- `agents/README.md` -- Specialized Agents.
- `skills/README.md` -- Custom Industrial Skills.
