---
name: sdd-flow
description: Use when building a feature properly from scratch and you might otherwise jump straight to code — when the user wants a spec, a reviewed plan, and tests before implementation, or says "spec-driven development", "use SDD", "run the SDD workflow", or "build this properly".
---

# SDD-Flow — spec-driven development orchestrator

## Overview

Drives a feature through three phases — **SPEC → PLAN → IMPLEMENT** — as a *wizard of loops*: each phase is an autonomous loop that converges on its own, then **STOPS at a human gate** (approve / modify / refine) before the next begins. You **orchestrate and reuse** the named sub-skills — you never skip a phase, collapse the phases into one pass, or reimplement a sub-skill you could invoke.

**Core principle: one phase at a time, autonomy inside each, a human gate between each, reuse don't reinvent.**

## Operating rules

- **Artifact paths (fixed):** constitution → `.specify/memory/constitution.md`; per-feature artifacts → `specs/<feature>/spec.md`, `plan.md`, `tasks.md`, `GOAL.md`. Use these exact paths; don't invent new ones.
- **Spec Kit:** run it via its CLI (`specify`) and `/speckit.*` commands when available. **If Spec Kit isn't installed and can't be**, don't stall — write `spec.md` / `plan.md` / `tasks.md` by hand at the paths above and do `analyze` as a consistency-checklist pass.
- **Missing sub-skill or tool:** if any REQUIRED sub-skill (`grilling`, `plan-review-panel`, `to-issues`, `deep-research`, `superpowers:*`, `loop`) or external tool (`codex`, `specify`) is unavailable, **do its work inline and state the degradation explicitly** — never stall, never silently skip.
- **Gate mechanics:** at every `GATE`, present the artifact, ask one explicit **approve / modify / refine** question, then **END YOUR TURN and wait**. Resume only on the human's next message. Treat silence or ambiguity as NO-GO — never self-approve a gate.

## Precondition — Constitution (required, do this first)

A project constitution is the supreme set of principles every later artifact is checked against. If `.specify/memory/constitution.md` is missing: **STOP and offer to generate it** via `/speckit.constitution` (run `specify init` to install Spec Kit first if needed). Never start feature work without it.

## Invariant — applies to every phase loop

1. **Done-check** (verifiable), **max-iterations budget**, and **stall detection** — same finding twice without new evidence, or no progress → **stop and defer to the human**. Never spin.
2. **Validate before presenting:** every new decision (feature, architecture, library) is checked against official docs + community + best-practice *before* you surface it. Never hand the human raw questions — bring **problems with proposed resolutions**.

## Phase 1 — SPEC  ·  gate: approve the spec

Loop until the spec is sharp:
- **REQUIRED SUB-SKILL: superpowers:brainstorming** — design the spec with the human, one question at a time, no code.
- **REQUIRED SUB-SKILL: deep-research** — validate risky or novel decisions against official sources.
- **REQUIRED SUB-SKILL: grilling** — adversarially sharpen until no high-impact objection remains.

Write `spec.md` (at `specs/<feature>/spec.md`, via `/speckit.specify` when available), with **measurable acceptance criteria**.

**GATE:** present the sharpened spec; human approves / modifies / refines. Refine → re-loop. Only an approval advances to Phase 2.

## Phase 2 — PLAN  ·  gate: approve "start building"

Loop using the Spec Kit machinery: `/speckit.clarify` → `/speckit.checklist` → `/speckit.plan` → `/speckit.tasks` (seed vertical slices with **REQUIRED SUB-SKILL: to-issues**) → `/speckit.analyze` (mechanical consistency: spec ↔ plan ↔ tasks ↔ constitution; iterate until clean).
- Any novel tech/architecture/library decision here also gets validated against sources first (**REQUIRED SUB-SKILL: deep-research**) — source-validation is cross-cutting, not Phase-1-only.
- The **one** architecture challenge: **REQUIRED SUB-SKILL: grilling** on "why this design — is there a better alternative the sources support?"
- **REQUIRED SUB-SKILL: plan-review-panel** — independent, adaptive cross-tool review; succeed only when reviewers converge to GO on the **same unchanged version**.

`GOAL.md` **crystallizes here**: the spec's measurable criteria + the plan's test/evaluation method = the completion contract Phase 3 runs against.

**GATE:** human approves "start building". Refine → re-loop.

## Phase 3 — IMPLEMENT  ·  gate: approve destructive / production actions

Run autonomously against `GOAL.md` as a **self-paced goal loop** until the done-check passes (the `loop` skill *with no interval* — not an interval scheduler; or just iterate the slice loop directly). For each vertical slice:
- **REQUIRED SUB-SKILL: superpowers:test-driven-development** — failing test → implement (maker).
- **Independent verify** (checker): dispatch a **separate subagent** to prove the test holds via revert/mutation (`verify` / `code-review`), not just that it's green — self-checking your own slice defeats the point.
- On repeated failure: **REQUIRED SUB-SKILL: superpowers:systematic-debugging** (bounded — ~5 attempts, then escalate).
- Green → commit → update `GOAL.md` (each outcome proved / weak / missing) → next slice.

**Done-check (THE GOAL):** every slice green **AND** every `GOAL.md` outcome proved with evidence. Blocked / stalled / budget exhausted → human.

**GATE:** approve anything destructive or production-facing.

## Red flags — you're not running the pipeline

- You wrote code before a constitution **and** an approved spec exist.
- You produced spec + plan + code in one pass without stopping at the gates.
- You reviewed the plan yourself instead of invoking `plan-review-panel`.
- You reimplemented brainstorming / grilling / tdd instead of invoking them.
- A phase loop has no done-check or no stop condition.
- You advanced past a gate the human didn't approve.
