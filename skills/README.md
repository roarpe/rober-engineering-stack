# Custom Industrial Skills

## Que son las Custom Industrial Skills

Las Custom Industrial Skills son capacidades activables bajo demanda que
cubren necesidades especificas de ingenieria industrial no resueltas por skills
externas generales. No son agentes, no son modulos, no son gates. Son
herramientas de procedimiento que un agente activa cuando su dominio lo
requiere.

## Por que son activables bajo demanda

- No todo proyecto necesita toda skill.
- Una skill se activa solo cuando hay un trigger claro, un input definido, un
  output esperado y un consumer identificado.
- Las skills no son reglas globales. No modifican configuracion ni crean
  dependencias permanentes.
- Las skills no pueden saltarse gates.

## Relacion con agentes, gates y modulos

- **Agentes**: recomiendan y activan skills segun su dominio. El agente sigue
  siendo responsable del output; la skill es el procedimiento.
- **Gates**: las skills producen artefactos que los gates consumen. Una skill
  no reemplaza un gate; le entrega material.
- **Modulos**: determinan que skills son relevantes para el proyecto. Un modulo
  activo habilita skills de su dominio.

## Skills previstas (9)

| # | Skill | Estado | Dominio |
|---|---|---|---|
| 1 | `industrial-project-discovery` | Implementada (Fase 7A) | Discovery pre-requisitos |
| 2 | `plc-software-architecture` | Implementada (Fase 7A) | Arquitectura PLC |
| 3 | `industrial-communications-design` | Implementada (Fase 7B) | Comunicaciones industriales |
| 4 | `robotics-cell-integration` | Implementada (Fase 7B) | Integracion robotica |
| 5 | `vision-ai-integration` | Implementada (Fase 7B) | Integracion vision/IA |
| 6 | `industrial-python-engineering` | Implementada (Fase 7C) | Estándares Python industriales |
| 7 | `machine-diagnostics` | Implementada (Fase 7C) | Diagnostico industrial |
| 8 | `industrial-documentation` | Implementada (Fase 7D) | Documentacion industrial |
| 9 | `industrial-project-verification` | Implementada (Fase 7D) | Verificacion industrial |

## Referencias

- `AGENTS.md` -- Skill Policy (constitucion).
- `ARCHITECTURE.md` -- Seccion 8: Custom Industrial Skills.
- `SKILLS_AUDIT.md` -- Auditoria y justificacion de skills custom.
- `gates/README.md` -- Engineering Gates.
- `agents/README.md` -- Specialized Agents.
