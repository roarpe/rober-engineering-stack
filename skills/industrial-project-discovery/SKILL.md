# Skill -- industrial-project-discovery

## Name

industrial-project-discovery

## Purpose

Transformar una idea, necesidad o problema industrial insuficientemente definido
en un conjunto estructurado de informacion que pueda consumir Requirements
Quality Gate. Recopilar y estructurar informacion, no evaluar su suficiencia.

## Activation Triggers

- Idea o necesidad industrial sin estructura suficiente.
- Problema operativo sin objetivo verificable definido.
- Proyecto nuevo donde se desconocen equipos, procesos, stakeholders o
  restricciones.
- Requirements Quality Gate devuelve FAIL por falta de informacion.

## When Not To Use

- El proyecto ya tiene requisitos validados y no han cambiado.
- La tarea es pequena, local y claramente especificada.
- El cambio es documental menor sin ambiguedad.
- Ya existe un `PROJECT_DISCOVERY.md` valido y actualizado.
- Se necesita arquitectura, no discovery (usar `plc-software-architecture` u
  otra skill de arquitectura).

## Primary Owner

Engineering Architect

## Participants

- Industrial Automation Engineer (aporta contexto de PLC/automatizacion).
- Robotics Engineer (aporta contexto de robotica).
- Software Engineer (aporta contexto de software/datos).
- Technical Documentation Engineer (aporta glosario y terminos).
- Usuario (fuente de informacion operativa y restricciones).

## Required Inputs

- Idea inicial o descripcion del problema.
- Contexto del repo/proyecto.
- Informacion disponible del usuario (proceso, equipos, entorno).
- Glosarios, CONTEXT o ADRs existentes si existen.

## Procedure

1. Identificar el objetivo del proyecto o cambio en una frase.
2. Describir el problema operativo que motiva el proyecto.
3. Describir el proceso fisico de alto nivel cuando aplique.
4. Identificar stakeholders y usuarios.
5. Identificar modos de operacion y secuencia funcional de alto nivel.
6. Listar equipos involucrados: PLC, robots, vision, software, datos.
7. Identificar interfaces, senales y comunicaciones conocidas.
8. Listar restricciones tecnicas, operativas, de plazos y de entorno.
9. Describir entorno de ejecucion, disponibilidad y mantenimiento.
10. Identificar requisitos de diagnostico y recuperacion ante fallos.
11. Identificar criterios de aceptacion conocidos.
12. Listar riesgos, incertidumbres y decisiones abiertas.
13. Clasificar cada item como FACT, ASSUMPTION, UNKNOWN, CONSTRAINT o
    DECISION NEEDED.
14. Producir el artefacto de salida.

### Clasificacion de informacion

- **FACT**: informacion verificada con evidencia.
- **ASSUMPTION**: suposicion sin verificar, marcada para validacion.
- **UNKNOWN**: informacion faltante que se necesita.
- **CONSTRAINT**: restriccion confirmada que limita el diseno.
- **DECISION NEEDED**: decision tecnica abierta que debe resolverse.

## Required Outputs

Artefacto: `PROJECT_DISCOVERY.md`

Contenido obligatorio:

- Objetivo del proyecto (frase verificable cuando sea posible).
- Problema operativo.
- Proceso fisico de alto nivel (si aplica).
- Stakeholders y usuarios.
- Modos de operacion y secuencia funcional de alto nivel (si aplica).
- Equipos involucrados (PLC, robots, vision, software, datos).
- Interfaces, senales y comunicaciones conocidas.
- Restricciones (tecnicas, operativas, plazos, entorno).
- Entorno de ejecucion, disponibilidad, mantenimiento.
- Requisitos de diagnostico y recuperacion.
- Criterios de aceptacion conocidos.
- Riesgos e incertidumbres.
- Decisiones abiertas.
- Clasificacion FACT/ASSUMPTION/UNKNOWN/CONSTRAINT/DECISION NEEDED por item.

## Consumer

Requirements Quality Gate

## Stop Condition

La skill se detiene cuando existe informacion suficiente para que Requirements
Quality Gate pueda evaluar la calidad de los requisitos. No es necesario que
todas las incertidumbres hayan desaparecido ni que todas las decisiones esten
resueltas. El proposito es entregar material estructurado, no un proyecto
completo.

## Gates Interaction

- **Antes de**: Requirements Quality Gate. La skill produce el insumo que el
  gate evalua.
- **No reemplaza**: Requirements Quality Gate. Discovery recopila y estructura;
  el gate evalua suficiencia y coherencia.
- **No ejecuta**: Implementation Review, Final Verification ni ningun otro
  gate.
- Si Requirements Quality devuelve FAIL, puede reactivarse para recopilar
  informacion adicional.

## Agent Interaction

- **Activada por**: Engineering Architect (owner).
- **Contribuyen**: especialistas de dominio segun tecnologia involucrada.
- **Handoff a**: Engineering Architect para entregar a Requirements Quality
  Gate.
- La skill no toma decisiones arquitectonicas. Las decisiones abiertas se
  registran como DECISION NEEDED para que Decision Readiness Gate las procese.

## Evidence Required

- `PROJECT_DISCOVERY.md` con todos los campos obligatorios.
- Clasificacion FACT/ASSUMPTION/UNKNOWN/CONSTRAINT/DECISION NEEDED por item.
- Las ASSUMPTIONs deben estar marcadas para validacion.
- Las UNKNOWNs deben identificar que informacion falta y donde obtenerla.

## Failure Modes

- Informacion insuficiente para que Requirements Quality evalue requisitos.
- Mezcla de discovery con arquitectura (la skill no debe disenar soluciones).
- ASSUMPTIONs presentadas como FACTs sin evidencia.
- Omision de restricciones criticas del entorno operativo.
- Scope creep: intentar resolver decisiones tecnicas en lugar de registrarlas.

## Escalation Rules

- Falta de informacion del usuario -> escalar al usuario con preguntas
  concretas.
- Conflicto entre requisitos de diferentes stakeholders -> escalar a
  Engineering Architect.
- Decision tecnica que requiere investigacion -> registrar como DECISION NEEDED
  y derivar a Decision Readiness Gate.
- Incertidumbre tecnica critica -> registrar como UNKNOWN y escalar a
  especialista de dominio.

## Done Criteria

- `PROJECT_DISCOVERY.md` completo con todos los campos obligatorios.
- Cada item clasificado como FACT, ASSUMPTION, UNKNOWN, CONSTRAINT o DECISION
  NEEDED.
- Objetivo del proyecto expresado en al menos una frase.
- Restricciones listadas.
- Decisiones abiertas registradas sin intentar resolverlas.
- Artefacto entregado a Engineering Architect para handoff a Requirements
  Quality Gate.
