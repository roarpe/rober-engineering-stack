# Engineering Gates

## Que es un Engineering Gate

Un Engineering Gate es un contrato operativo de control de calidad en un punto
concreto del flujo de trabajo. No es un agente, no es un modulo, no es una skill
permanente. Es un verificador con responsabilidad unica que produce un artefacto
de salida y una decision binaria: PASS o FAIL.

Los gates se activan proporcionalmente al riesgo, complejidad y fase del
proyecto. No todos los proyectos ejecutan todos los gates.

## Los cuatro gates

1. **Requirements Quality** -- Comprueba si existe informacion suficiente para
   pasar de idea/discovery a decisiones y arquitectura.

2. **Decision Readiness** -- Determina si las decisiones tecnicas bloqueantes
   estan resueltas o tienen un mecanismo claro de resolucion.

3. **Implementation Review** -- Revisa la implementacion en dos ejes separados:
   SPEC (requisitos, alcance, comportamiento) y STANDARDS (arquitectura,
   convenciones, mantenibilidad).

4. **Final Verification** -- Impide claims de completitud sin evidencia fresca.
   Siempre se aplica proporcionalmente antes de declarar trabajo terminado.

## Cuando se activan

La activacion sigue el flujo de seleccion definido en `AGENTS.md` y
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

Proporcionalidad por tamano de proyecto:

- **Pequeno**: Final Verification siempre (proporcional). Requirements Quality
  solo si hay ambiguedad. Implementation Review solo si hay diff con riesgo.
  Decision Readiness normalmente no.
- **Mediano**: Requirements Quality, Implementation Review, Final Verification.
  Decision Readiness condicionado a incertidumbre.
- **Grande**: los cuatro gates obligatorios.

## Como se relacionan

```text
Requirements Quality
  -> Decision Readiness (cuando aplique)
  -> Implementacion
  -> Implementation Review
  -> Final Verification
```

- Requirements Quality puede pasar directamente a arquitectura/planificacion si
  no hay decisiones abiertas, o derivar al Decision Readiness Gate si las hay.
- Decision Readiness recibe decisiones abiertas y devuelve un mapa de
  decisiones resuelto o con plan de resolucion.
- Implementation Review recibe el diff/implementacion y devuelve findings
  clasificados.
- Final Verification recibe todos los artefactos previos y exige evidencia
  fresca antes de aprobar cierre.

Final Verification nunca se omite antes de claims de completitud. Para
microtareas sin artefacto, basta una verificacion proporcional.

## Propiedad de artefactos

Cada gate produce un artefacto de salida con owner definido:

| Gate | Artefacto | Owner |
|---|---|---|
| Requirements Quality | `REQUIREMENTS_GATE_REPORT.md` | Engineering Architect |
| Decision Readiness | `DECISION_MAP.md` | Engineering Architect |
| Implementation Review | `IMPLEMENTATION_REVIEW.md` | QA & Debug Engineer |
| Final Verification | `FINAL_VERIFICATION_REPORT.md` | QA & Debug Engineer |

Los templates de estos artefactos se crearan en una fase posterior. Esta fase
define unicamente el contrato de output de cada gate.

## Referencias

- `AGENTS.md` -- Engineering Gates (seccion de constitucion).
- `ARCHITECTURE.md` -- Seccion 5: Engineering Gates (diseno arquitectonico).
- `ARCHITECTURE.md` -- Seccion 10.6: Gates (activacion proporcional).
- `ARCHITECTURE.md` -- Seccion 12: Flujos por complejidad.
