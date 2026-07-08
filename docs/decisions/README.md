# Architecture Decision Records

Este directorio almacenara ADRs en fases posteriores.

Un ADR es un registro breve de una decision arquitectonica importante. Debe explicar el contexto, la decision tomada, las alternativas consideradas y sus consecuencias.

## Cuando crear un ADR

Crear un ADR cuando:

- La decision sea dificil o costosa de revertir.
- Existan alternativas reales.
- Afecte a arquitectura, flujo de trabajo, agentes, gates, skills o estructura del repositorio.
- Un futuro agente podria reabrir la decision sin contexto.
- La decision cambie una regla operativa del stack.

## Cuando NO crear un ADR

No crear un ADR cuando:

- La decision sea trivial o facilmente reversible.
- Solo documente una tarea temporal.
- Repita contenido ya definido en `ARCHITECTURE.md`.
- No exista una alternativa tecnica razonable.
- El cambio sea puramente editorial.

## Estado

Los ADRs definitivos se crearan en fases posteriores. No existen ADR-0001, ADR-0002 ni registros numerados todavia.
