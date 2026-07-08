# Module -- git-parallel-delivery

## Name

git-parallel-delivery

## Purpose

Seleccionar y componer agentes, skills y gates relevantes para trabajo
paralelo: multiples agentes, multiples ramas, worktrees, cambios
desacoplables e integracion coordinada.

## Activation Triggers

- Hay trabajo paralelo con multiples agentes o multiples ramas.
- Hay cambios desacoplables que pueden progresar en paralelo.
- Hay worktrees que gestionar.
- Hay integracion coordinada que planificar.

## When Not To Activate

- Repo no tiene commits base.
- `gh` remoto es necesario pero no esta autenticado.
- El entorno/harness ya gestiona worktrees y no se ha detectado correctamente.
- El proyecto es pequeno con un solo agente y sin paralelo real.
- No hay cambios desacoplables que justifiquen ramas separadas.

## Primary Agents

- **Engineering Architect**: coordinacion de workstreams, boundaries,
  integration order, conflict prevention.

## Optional Agents

- **Especialistas responsables de cada workstream**: segun dominio activo
  (IAE, RE, SE, QA, TDE).
- **QA & Debug Engineer**: verificacion por workstream e integracion.

## Relevant Skills

Este modulo no tiene Custom Industrial Skills propias. Puede recomendar
skills externas de la biblioteca opcional (segun ARCHITECTURE.md 6.8):

- `using-git-worktrees`: cuando hay worktrees que gestionar.
- `subagent-driven-development`: cuando hay tareas delegables en paralelo.
- `executing-plans`: cuando hay planes que ejecutar en paralelo.
- `finishing-a-development-branch`: cuando hay ramas que finalizar.

Solo activar si estan disponibles y justificadas. No activar
automaticamente.

## Gates Policy

- **Implementation Review**: por workstream o integrado, segun riesgo.
- **Final Verification**: siempre, despues de integracion.
- **Requirements Quality**: normalmente no, salvo que el paralelo genere
  ambiguedad.
- **Decision Readiness**: cuando hay decisiones de boundary o integration
  order blocking.
- Ningun gate se omite por riesgo en proyecto grande.
- Este modulo no sustituye Implementation Review ni Final Verification.

## Typical Inputs

- Plan del proyecto con tareas identificadas.
- Workstreams propuestos con boundaries.
- Dependencias entre workstreams.
- Estado del repo (commits, ramas, worktrees).

## Typical Outputs

- Workstream plan (boundaries, ownership, branch policy).
- Integration order.
- Conflict prevention strategy.
- Dependency management plan.

## Cross-Domain Interfaces

- **Todos los dominios activos**: cada workstream puede involucrar cualquier
  dominio. Las interfaces entre workstreams requieren contrato explicito.

## Risk Signals

- Workstreams con dependencias ocultas no declaradas.
- Integration order no definida.
- Worktrees sin cleanup ni policy.
- Conflictos de merge frecuentes sin prevencion.
- Falta de coordinacion entre agentes paralelos.

## Scaling Policy

- **Small**: no activar este modulo. Trabajo secuencial.
- **Medium**: EA coordina 2-3 workstreams, integration order simple, IR + FV.
- **Large/High-Risk**: EA coordina multiples workstreams, boundaries explicitos,
  dependency management, integration order detallado, IR por workstream + FV
  integrado.

## Composition Rules

- Este modulo se compone con cualquier otro modulo activo.
- Cada workstream conserva el ownership de su dominio.
- Engineering Architect coordina dependencias transversales entre workstreams.
- Las skills compartidas entre workstreams se activan una sola vez.
- Los gates evaluan el artefacto relevante, no cada workstream mecanicamente.
- No crear automaticamente ramas o worktrees: planificar primero.
- No sustituir planificacion: el modulo complementa, no reemplaza.

## Handoff Expectations

- Handoff entre workstreams con contrato explicito (artefacto, estado,
  dependencias).
- Handoff a QA & Debug Engineer para verificacion de integracion.
- Handoff a Engineering Architect para decisiones de integration order.
- Todo handoff incluye artefacto, estado, evidencia, decisiones, riesgos,
  siguiente owner.

## Done Criteria

- Workstream plan con boundaries y ownership definidos.
- Integration order establecida.
- Worktrees gestionados con cleanup.
- Conflictos prevenidos o resueltos.
- Gates aplicados (IR + FV minimo).
- Handoffs completados.
