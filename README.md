# ROBER ENGINEERING STACK v1.0

ROBER ENGINEERING STACK es un sistema de ingenieria reutilizable para trabajar con agentes de programacion en proyectos de software, automatizacion industrial, PLC, robotica, vision artificial, inteligencia artificial, integracion de sistemas y datos.

Su objetivo es evitar un conjunto caotico de instrucciones, skills y agentes. El stack prioriza una arquitectura modular, verificable y mantenible: pocas reglas globales, gates claros, modulos activables y skills bajo demanda.

## Problemas que resuelve

- Convertir ideas industriales o software en requisitos tecnicos verificables.
- Seleccionar agentes, modulos y skills segun riesgo y complejidad.
- Evitar duplicidades entre discovery, planificacion, ADRs, review y verificacion.
- Mantener separadas las capacidades globales, gates, modulos, skills industriales y biblioteca opcional.
- Impedir declarar proyectos terminados sin evidencia.

## Dominios soportados

- Software engineering.
- Automatizacion industrial y PLC.
- Robotica industrial y ROS 2.
- Vision artificial.
- Inteligencia artificial y sistemas agenticos.
- Comunicaciones industriales y APIs.
- Data engineering e integracion de sistemas.

## Filosofia de diseno

El stack sigue una politica de carga minima de contexto. Las reglas permanentes deben ser breves y estables; las skills, gates y modulos se activan solo cuando aportan un output claro.

Principios base:

- Analizar antes de implementar.
- Investigar antes de instalar.
- Verificar antes de declarar completitud.
- Mantener el Global Core pequeno.
- Usar workflows proporcionales al tamano y riesgo del proyecto.
- Documentar decisiones arquitectonicas relevantes.

## Arquitectura de cinco capas

1. **Global Core** minimo ([AGENTS.md](AGENTS.md)).
2. **Engineering Gates** -- 4 gates de calidad y verificacion.
3. **Project Modules** -- 8 modulos activables por dominio.
4. **Custom Industrial Skills** -- 9 skills industriales bajo demanda.
5. **Optional Skill Library** -- skills externas de referencia.

La arquitectura completa esta definida en
[ARCHITECTURE.md](ARCHITECTURE.md).

## Engineering Gates (4)

Los gates son puntos de control que evaluan artefactos y bloquean el avance
hasta que se cumple un criterio. No son inspecciones opcionales.

| Gate | Proposito | Owner | Artefacto |
|---|---|---|---|
| [Requirements Quality](gates/requirements-quality/GATE.md) | Validar requisitos antes de disenar | Engineering Architect | `REQUIREMENTS_GATE_REPORT.md` |
| [Decision Readiness](gates/decision-readiness/GATE.md) | Resolver decisiones blocking antes de arquitectura | Engineering Architect | `DECISION_MAP.md` |
| [Implementation Review](gates/implementation-review/GATE.md) | Revisar implementacion contra SPEC y STANDARDS | QA & Debug Engineer | `IMPLEMENTATION_REVIEW.md` |
| [Final Verification](gates/final-verification/GATE.md) | Impedir declarar completitud sin fresh evidence | QA & Debug Engineer | `FINAL_VERIFICATION_REPORT.md` |

Ver [gates/README.md](gates/README.md) para detalle de activacion, flujo y
proporcionalidad.

## Specialized Agents (6)

Los agentes son responsables de dominio. No son tareas, no son prompts. Cada
agente tiene mision, limites, inputs, outputs, skills policy, gate
participation y escalation rules.

| Agente | Dominio | Lidera gates |
|---|---|---|
| [Engineering Architect](agents/engineering-architect/AGENT.md) | Coordinacion transversal | RQ, DR |
| [Industrial Automation Engineer](agents/industrial-automation-engineer/AGENT.md) | PLC, automatizacion | -- |
| [Robotics Engineer](agents/robotics-engineer/AGENT.md) | Robotica, integracion robot | -- |
| [Software Engineer](agents/software-engineer/AGENT.md) | Software, datos, Python | -- |
| [QA & Debug Engineer](agents/qa-debug-engineer/AGENT.md) | Calidad, debugging, verificacion | IR, FV |
| [Technical Documentation Engineer](agents/technical-documentation-engineer/AGENT.md) | Documentacion, ADRs, glosario | -- |

Ver [agents/README.md](agents/README.md) para detalle de misiones, limites y
handoffs.

## Custom Industrial Skills (9)

Las skills son capacidades activables bajo demanda que cubren necesidades
especificas de ingenieria industrial. No son agentes, no son gates. Tienen
trigger, input, output, consumer y stop condition.

| # | Skill | Fase | Artefacto |
|---|---|---|---|
| 1 | [industrial-project-discovery](skills/industrial-project-discovery/SKILL.md) | 7A | `PROJECT_DISCOVERY.md` |
| 2 | [plc-software-architecture](skills/plc-software-architecture/SKILL.md) | 7A | `PLC_ARCHITECTURE.md` |
| 3 | [industrial-communications-design](skills/industrial-communications-design/SKILL.md) | 7B | `INDUSTRIAL_COMMUNICATIONS_DESIGN.md` |
| 4 | [robotics-cell-integration](skills/robotics-cell-integration/SKILL.md) | 7B | `ROBOTICS_CELL_INTEGRATION.md` |
| 5 | [vision-ai-integration](skills/vision-ai-integration/SKILL.md) | 7B | `VISION_AI_INTEGRATION.md` |
| 6 | [industrial-python-engineering](skills/industrial-python-engineering/SKILL.md) | 7C | `INDUSTRIAL_PYTHON_ENGINEERING.md` |
| 7 | [machine-diagnostics](skills/machine-diagnostics/SKILL.md) | 7C | `MACHINE_DIAGNOSTICS.md` |
| 8 | [industrial-documentation](skills/industrial-documentation/SKILL.md) | 7D | `INDUSTRIAL_DOCUMENTATION.md` |
| 9 | [industrial-project-verification](skills/industrial-project-verification/SKILL.md) | 7D | `INDUSTRIAL_PROJECT_VERIFICATION.md` |

Ver [skills/README.md](skills/README.md) para detalle de activacion, ownership
y relacion con gates y agentes.

## Seleccion proporcional

No todo proyecto necesita todo. La seleccion sigue este flujo:

```text
PROYECTO
  -> RIESGO / COMPLEJIDAD
  -> MODULO
  -> AGENTE
  -> SKILL
  -> GATE
  -> EJECUCION
```

- **Proyectos pequenos**: Global Core + gate proporcional. Sin modulos ni
  skills.
- **Proyectos medianos**: Global Core + 1-2 modulos + agentes relevantes +
  gates RQ/IR.
- **Proyectos grandes**: Global Core + modulos + agentes + skills + gates
  completos + ADRs.

## Relacion entre Agent, Gate, Skill y Module

- **Agent**: responsable de dominio. Recomienda y activa skills. Participa en
  gates. Produce artefactos.
- **Gate**: punto de control. Evalua artefactos. Bloquea o autoriza avance.
  No disena ni implementa.
- **Skill**: procedimiento activable. Produce artefactos que gates consumen.
  No reemplaza gates. No toma decisiones arquitectonicas.
- **Module**: dominio de proyecto. Determina que agentes y skills son
  relevantes. Ver `modules/README.md`.

## Flujo operativo de alto nivel

1. `industrial-project-discovery` (si hace falta) -> `PROJECT_DISCOVERY.md`.
2. Requirements Quality Gate -> `REQUIREMENTS_GATE_REPORT.md`.
3. Decision Readiness Gate (si hay decisiones blocking) ->
   `DECISION_MAP.md`.
4. Arquitectura de dominio (skills segun modulo activo).
5. ADRs para decisiones dificiles de revertir.
6. Plan de implementacion.
7. Implementacion por incrementos.
8. Implementation Review Gate -> `IMPLEMENTATION_REVIEW.md`.
9. Industrial Project Verification (si hace falta) ->
   `INDUSTRIAL_PROJECT_VERIFICATION.md`.
10. Final Verification Gate -> `FINAL_VERIFICATION_REPORT.md`.
11. Documentacion y lecciones aprendidas.

No todos los pasos aplican a todos los proyectos. La proporcionalidad decide.

## Estructura actual del repositorio

```text
.
├── AGENTS.md                    # Global Core (constitucion)
├── ARCHITECTURE.md              # Diseno arquitectonico completo
├── README.md                    # Este archivo
├── ENVIRONMENT_AUDIT.md         # Auditoria del entorno (Fase 0)
├── SKILLS_AUDIT.md              # Auditoria de skills (Fase 1)
├── STACK_COHERENCE_AUDIT.md     # Auditoria de coherencia (Fase 7F)
├── STACK_OPERATIONAL_VALIDATION.md  # Validacion operacional (Fase 9B)
├── RELEASE_READINESS.md         # Evaluacion de release readiness (Fase 10)
├── PILOT_PROJECT_PROPOSAL.md    # Propuesta del piloto (Fase 11A)
├── REQUIREMENTS_GATE_REPORT.md  # Requirements Quality Gate del piloto
├── INDUSTRIAL_COMMUNICATIONS_DESIGN.md  # Diseno de interfaz OT-pipeline
├── MACHINE_DIAGNOSTICS.md       # Taxonomia de diagnostico del piloto
├── INDUSTRIAL_PYTHON_ENGINEERING.md     # Diseno Python del piloto
├── IMPLEMENTATION_REVIEW.md     # Implementation Review Gate del piloto
├── agents/                      # 6 Specialized Agents
│   ├── README.md
│   ├── engineering-architect/AGENT.md
│   ├── industrial-automation-engineer/AGENT.md
│   ├── robotics-engineer/AGENT.md
│   ├── software-engineer/AGENT.md
│   ├── qa-debug-engineer/AGENT.md
│   └── technical-documentation-engineer/AGENT.md
├── gates/                       # 4 Engineering Gates
│   ├── README.md
│   ├── requirements-quality/GATE.md
│   ├── decision-readiness/GATE.md
│   ├── implementation-review/GATE.md
│   └── final-verification/GATE.md
├── modules/                     # 8 Project Modules
│   ├── README.md
│   ├── software-development/MODULE.md
│   ├── industrial-automation/MODULE.md
│   ├── robotics/MODULE.md
│   ├── artificial-intelligence/MODULE.md
│   ├── computer-vision/MODULE.md
│   ├── data-engineering/MODULE.md
│   ├── web-development/MODULE.md
│   └── git-parallel-delivery/MODULE.md
├── skills/                      # 9 Custom Industrial Skills
│   ├── README.md
│   ├── industrial-project-discovery/SKILL.md
│   ├── plc-software-architecture/SKILL.md
│   ├── industrial-communications-design/SKILL.md
│   ├── robotics-cell-integration/SKILL.md
│   ├── vision-ai-integration/SKILL.md
│   ├── industrial-python-engineering/SKILL.md
│   ├── machine-diagnostics/SKILL.md
│   ├── industrial-documentation/SKILL.md
│   └── industrial-project-verification/SKILL.md
├── pilot/                       # Implementacion del piloto (Fase 11B)
│   ├── __init__.py
│   ├── cli.py
│   ├── diagnostics.py
│   ├── exceptions.py
│   ├── ingestion.py
│   ├── models.py
│   ├── persistence.py
│   ├── telemetry_source.py
│   ├── validator.py
│   ├── watchdog.py
│   └── utils/
│       ├── __init__.py
│       └── clock.py
├── tests/                       # Tests del piloto (68 casos)
│   ├── __init__.py
│   ├── test_telemetry_source.py
│   ├── test_ingestion_valid.py
│   ├── test_ingestion_invalid.py
│   ├── test_diagnostics_thresholds.py
│   ├── test_diagnostics_no_alarm.py
│   └── test_cli_end_to_end.py
└── docs/                        # Documentacion complementaria
    ├── README.md
    └── decisions/README.md
```

## Estado del roadmap

Fases completadas:

- Fase 0: auditoria del entorno.
- Fase 1: investigacion y auditoria de skills.
- Fase 2: diseno de arquitectura.
- Fase 3: creacion del repositorio base.
- Fase 4: creacion de `AGENTS.md` (Global Core).
- Fase 5: creacion de Engineering Gates (4 gates).
- Fase 6: creacion de Specialized Agents (6 agentes).
- Fase 7: creacion de Custom Industrial Skills (9 skills).
- Fase 8: creacion de Project Modules (8 modulos).
- Fase 9: reconciliacion y validacion operacional.
- Fase 10: sincronizacion de contratos y release readiness.

Fase 11 -- Proyecto piloto: *Industrial Machine Telemetry Ingestion &
Diagnostics Pipeline*. En curso.

- Fase 11A -- Discovery & Pilot Proposal: completada.
- Fase 11B -- Requirements & Technical Design: completada.
- Fase 11C -- Implementation & Tests: completada (68 tests passing).
- Fase 11D -- Implementation Review: completada (PASS).
- Fase 11E -- Final Verification: pendiente.
- Fase 11F -- Pilot Closure & Lessons Learned: pendiente.

Estado actual: Implementation Review PASS -- Final Verification pendiente.

Fases pendientes:

- Fase 12: evaluacion y mejora.

## Como empezar a explorar

1. [AGENTS.md](AGENTS.md) -- reglas globales y politicas del stack.
2. [ARCHITECTURE.md](ARCHITECTURE.md) -- diseno completo de capas, gates,
   agentes, skills y flujos.
3. [gates/README.md](gates/README.md) -- Engineering Gates.
4. [agents/README.md](agents/README.md) -- Specialized Agents.
5. [skills/README.md](skills/README.md) -- Custom Industrial Skills.
6. [modules/README.md](modules/README.md) -- Project Modules.
7. [SKILLS_AUDIT.md](SKILLS_AUDIT.md) -- auditoria historica de skills.
8. [PILOT_PROJECT_PROPOSAL.md](PILOT_PROJECT_PROPOSAL.md) -- propuesta del
   piloto.
9. [IMPLEMENTATION_REVIEW.md](IMPLEMENTATION_REVIEW.md) -- Implementation
   Review Gate del piloto.

## Politica de estructura progresiva

El repositorio se crea de forma progresiva. Una carpeta debe existir cuando
haya un artefacto real que almacenar.

Se evita crear:

- Carpetas vacias.
- Placeholders innecesarios.
- `.gitkeep` indiscriminados.
- Documentacion ficticia.
