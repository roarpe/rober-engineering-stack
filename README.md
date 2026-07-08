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

1. Global Core minimo.
2. Engineering Gates.
3. Project Modules.
4. Custom Industrial Skills.
5. Optional Skill Library.

La arquitectura completa esta definida en [ARCHITECTURE.md](ARCHITECTURE.md).

## Estado actual

Fases completadas:

- Fase 0: auditoria del entorno.
- Fase 1: investigacion y auditoria de skills.
- Fase 2: diseno de arquitectura.
- Fase 3: creacion del repositorio base, en curso.

Artefactos principales:

- [ENVIRONMENT_AUDIT.md](ENVIRONMENT_AUDIT.md)
- [SKILLS_AUDIT.md](SKILLS_AUDIT.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)
- [docs/README.md](docs/README.md)

## Roadmap por fases

1. Fase 0 - Auditoria del entorno.
2. Fase 1 - Investigacion y auditoria de skills.
3. Fase 2 - Diseno de arquitectura.
4. Fase 3 - Creacion del repositorio base.
5. Fase 4 - Creacion de `AGENTS.md`.
6. Fase 5 - Creacion de Engineering Gates.
7. Fase 6 - Creacion de agentes.
8. Fase 7 - Creacion de las 8 custom industrial skills.
9. Fase 8 - Creacion de modulos.
10. Fase 9 - Creacion de templates.
11. Fase 10 - Testing del sistema.
12. Fase 11 - Proyecto piloto.
13. Fase 12 - Evaluacion y mejora.

## Politica de estructura progresiva

El repositorio se crea de forma progresiva. Una carpeta debe existir cuando haya un artefacto real que almacenar.

Se evita crear:

- Carpetas vacias.
- Placeholders innecesarios.
- `.gitkeep` indiscriminados.
- Documentacion ficticia.

Las carpetas de agentes, gates, skills, modulos, templates, ejemplos, scripts y tests se incorporaran cuando sus fases correspondientes creen contenido real.
