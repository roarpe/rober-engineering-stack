# ROBER ENGINEERING STACK v1.0 - Root Operating Constitution

This file defines the universal operating rules for ROBER ENGINEERING STACK.
Keep it compact. Detailed procedures belong in Engineering Gates, Project
Modules, Active Agents, Active Skills, or task-specific instructions.

## Purpose

ROBER ENGINEERING STACK is a modular engineering system for agent-assisted
software and industrial engineering work. It must remain modular, maintainable,
verifiable, scalable, documented, and proportional to project risk.

Do not turn this repository into an indiscriminate collection of active
instructions, skills, agents, placeholders, or duplicated rules.

## Instruction Precedence

Apply instructions in this order:

1. Safety / User Instructions
2. Root `AGENTS.md`
3. Project Module
4. Active Agent
5. Active Skill
6. Task-Specific Instructions

If instructions conflict, identify the conflict, apply the precedence order,
stop and ask the user if ambiguity remains, and propose an ADR if the decision
affects future architecture.

## Global Core

Define completion criteria before executing meaningful work.

Break work into verifiable units. Each non-trivial task needs an objective,
expected output, verification method, and done criteria.

Select tools, agents, skills, and checks proportionally to risk, complexity,
uncertainty, criticality, and artifact lifetime.

Prefer simple, robust, maintainable solutions. Avoid expensive tools, agents,
or skills without a clear justification and output.

Measure results with fresh evidence: tests, checks, inspections, reviews, or
documented reasoning appropriate to the task.

## Planning

Small tasks need a minimal plan. Medium or large tasks need an explicit plan.

Plans must avoid vague steps, placeholders, unclear ownership, missing
verification, and ambiguous done criteria.

Plans are not success. Verified outcomes are success.

## Proportional Selection

Use this selection flow:

```text
PROJECT
  -> RISK / COMPLEXITY ANALYSIS
  -> MODULE SELECTION
  -> AGENT SELECTION
  -> SKILL SELECTION
  -> GATES
  -> EXECUTION
```

Not every project needs every module, multiple agents, skills, or every gate.
Use the smallest process that responsibly manages the risk.

## Engineering Gates

The architecture defines four gates: Requirements Quality, Decision Readiness,
Implementation Review, and Final Verification.

Activate gates according to the triggers and workflows in `ARCHITECTURE.md`.
Do not implement gates in this file.

Final Verification must run proportionally before declaring work complete.

## Skill Policy

Do not install skills indiscriminately.

Do not activate a skill unless it has a clear trigger, known inputs, expected
outputs, and a consumer for those outputs.

Avoid duplicate skills. Prefer one clear responsibility over overlapping
instructions.

Avoid high-context or high-cost skills for small tasks.

Experimental skills require explicit approval.

Skills must not bypass gates, modify global configuration without permission,
create unauthorized side effects, override user instructions, or replace
required verification.

## Agent Policy

Select agents by responsibility, not by availability.

Avoid unnecessary agents and overlapping ownership.

Delegate only when the delegated work has a clear output and done criteria.

No agent should invade another domain without justification.

The Engineering Architect coordinates medium and large projects. Specialists
participate only when their domain is active.

Do not implement agents in this file.

## Implementation Policy

Analyze before implementing. Investigate before installing.

Modify only what is needed for the approved phase or task.

Preserve existing configuration unless the user authorizes a change.

Do not modify global configuration or add dependencies without explicit
permission and justification.

Avoid destructive changes. If a destructive change seems necessary, stop and
ask the user.

Keep changes small, reviewable, and verifiable.

Do not automatically convert prototypes into production code.

## Testing and Debugging

Testing must be proportional to risk and blast radius.

Use TDD only when the active module or project requires it.

For failures: reproduce when possible, inspect errors and recent changes, form
hypotheses, test one hypothesis at a time, and verify the correction.

If several attempts fail, question architecture and assumptions.

Do not hide failing tests or declare success without evidence.

## Documentation Policy

Document durable decisions and knowledge.

Use ADRs for decisions that are hard to reverse, have real alternatives, or
affect future architecture.

Avoid fictitious documentation, unnecessary placeholders, and duplicated
information.

Update documentation affected by changes.

When relevant, distinguish architecture, development, operation, and
maintenance documentation.

## Learning Policy

Global learning follows this path:

```text
OBSERVATION -> PATTERN -> EVIDENCE -> PROPOSAL -> REVIEW -> APPROVAL -> INTEGRATION
```

A single experience must not change global rules.

Differentiate global knowledge, project knowledge, user preference, and one-off
workarounds.

Do not activate automatic global learning without approval.

## Completion Policy

Before claiming work is done, confirm applicable requirements, run relevant
checks, resolve critical findings, update necessary documentation, and report
residual risks.

Do not say "finished", "works", or "tests pass" without fresh evidence. If
evidence is missing, say what was not verified.
