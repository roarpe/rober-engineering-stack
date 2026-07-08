# Module -- web-development

## Name

web-development

## Purpose

Seleccionar y componer agentes, skills y gates relevantes para proyectos web:
frontend, backend web, APIs, dashboards, interfaces de operacion o ingenieria
y aplicaciones web industriales.

## Activation Triggers

- Hay frontend, UI o experiencia de usuario que disenar.
- Hay backend web, APIs web o servicios web.
- Hay dashboards o interfaces de operacion/ingenieria.
- Hay aplicaciones web industriales (HMI web, SCADA web, monitoreo).

## When Not To Activate

- No hay interfaz web ni backend web.
- Web solo aparece como contexto futuro no abordado.
- El proyecto es puramente PLC o robotica sin componente web.
- El cambio es documental menor sin contenido web.

## Primary Agents

- **Software Engineer**: frontend, backend web, APIs, dashboards,
  integracion.

## Optional Agents

- **Engineering Architect**: cuando hay multiples dominios o riesgo
  arquitectonico.
- **Industrial Automation Engineer**: cuando hay HMI/SCADA o interfaces OT.
- **QA & Debug Engineer**: cuando hay implementacion que verificar.
- **Technical Documentation Engineer**: cuando hay outputs duraderos.

## Relevant Skills

Custom Industrial Skills (activar por trigger, no automaticamente):

- `industrial-python-engineering`: cuando hay Python en backend web
  industrial.
- `industrial-communications-design`: cuando hay comunicaciones con PLC o
  servicios industriales.
- `machine-diagnostics`: cuando hay diagnostico que involucra interfaz web.
- `industrial-documentation`: cuando hay estrategia documental industrial.
- `industrial-project-verification`: cuando hay verificacion transversal.

Optional Library Skills (segun ARCHITECTURE.md 6.7):

- `api-design`, `prototype` para exploracion UI, `test-driven-development`,
  `code-review`.

## Gates Policy

- **Requirements Quality**: cuando hay ambiguedad o proyecto mediano/grande.
- **Decision Readiness**: condicionado a decisiones de arquitectura web.
- **Implementation Review**: cuando hay codigo web que revisar.
- **Final Verification**: siempre proporcional, antes de claims.
- Ningun gate se omite por riesgo en proyecto grande.

## Typical Inputs

- Requisitos de UI/UX o API web.
- Arquitectura o plan del proyecto.
- Interfaces con PLC, datos, software.
- ADRs aplicables.

## Typical Outputs

- Web architecture (frontend, backend, APIs).
- API contracts web.
- UI design o dashboard design.
- Criterios de test web.

## Cross-Domain Interfaces

- **Software**: APIs, servicios, integracion.
- **Datos**: consumo de pipelines, telemetria, analytics.
- **PLC/OT**: HMI web, SCADA web, monitoreo.
- **IA**: visualizacion de resultados de inferencia.

## Risk Signals

- Interfaz web sin requisitos de usabilidad para operadores.
- Seguridad web no considerada (auth, CORS, input validation).
- Real-time no evaluado para requisitos de monitoreo.
- API web sin versionado ni contrato.
- Frontend acoplado a backend sin separacion de capas.

## Scaling Policy

- **Small**: SE solo, skills por trigger, FV proporcional.
- **Medium**: SE + QA, RQ + IR + FV, interfaces definidas, ADRs necesarios.
- **Large/High-Risk**: EA coordina + SE + IAE + QA + TDE, los cuatro gates,
  trazabilidad, verificacion transversal.

## Composition Rules

- No asumir automaticamente que toda interfaz industrial debe ser web.
- No requiere `software-development` por defecto: backend web, APIs web y
  servicios web estan dentro de su dominio. `software-development` es
  complementario cuando hay trabajo software transversal no cubierto.
- Cuando se compone con `data-engineering`, los contratos de datos los define
  SE (data); el modulo web consume.
- Cuando se compone con `industrial-automation`, las interfaces HMI/SCADA
  requieren contrato explicito con PLC. `industrial-communications-design` se
  activa una sola vez.
- Cuando se compone con `software-development`,
  `industrial-python-engineering` se activa una sola vez si Python aplica.
- Las skills compartidas se activan una sola vez por necesidad.

## Handoff Expectations

- Handoff a QA & Debug Engineer para verificacion web.
- Handoff a Technical Documentation Engineer para documentacion.
- Handoff a Engineering Architect para decisiones transversales.
- Todo handoff incluye artefacto, estado, evidencia, decisiones, riesgos,
  siguiente owner.

## Done Criteria

- Web architecture coherente con requisitos.
- API contracts web definidos y versionados.
- UI/dashboard design alineado con usuarios.
- Gates aplicados segun proporcionalidad.
- Handoffs completados.
