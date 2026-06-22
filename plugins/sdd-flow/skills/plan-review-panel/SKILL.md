---
name: plan-review-panel
description: Use when a plan, spec, or design needs an independent review gate before building — and you're about to assess it yourself in a single pass. Triggers: "is this plan ready", "review before we build", a GO/NO-GO on a plan, spec-driven-development Phase 2, approving "start building".
---

# Plan Review Panel

## Overview

A plan review is **not** one agent reading the plan once. It is a **panel of independent reviewers** that must **converge** on the same verdict for the same unchanged plan. Your job is to **orchestrate the panel** — not to be the reviewer.

**Core principle: independent reviewers, adaptive cross-tool, converge on the same version — or escalate.**

## The failure this prevents

Left alone, an agent reviews the plan itself, in a single pass, with one mind, and writes the verdict. That misses what an independent second perspective — especially a *different model* — would catch. The moment you start critiquing the plan yourself, stop: assemble the panel instead.

## Step 1 — Assemble the panel (adaptive cross-tool)

- **Always:** run **≥2 independent reviewers with DISTINCT lenses** so they can't echo each other — e.g. **correctness**, **security/abuse**, **simplicity/over-engineering**, **constitution-alignment**. **Each reviewer is a separate subagent with its own clean context** (dispatch one per lens — see `superpowers:dispatching-parallel-agents`), so "blind to the others" is real. One agent role-playing every lens in a single context is *not* a panel — it's the single-mind failure this skill exists to prevent.
- **Cross-tool, if available:** detect a second model — `command -v codex` (or another installed agent CLI). If present, add it as a genuinely independent reviewer by invoking the model **directly** (e.g. `codex exec "<review prompt>"`), not through a wrapper/rescue agent that may silently evaluate with the host model instead. A different model family is the only way to get *real* convergence rather than a same-model echo — if you can't confirm the second model actually ran, treat it as the host-only floor and say so.
- **Floor (degrade gracefully):** if no second tool is installed, run host-only with the distinct lenses above — and **say so explicitly** in the output ("cross-tool reviewer unavailable; host-only panel"). Never silently skip the cross-tool; never hard-fail because a tool is missing.

## Step 2 — Fan out

Give every reviewer the same plan and the same ask: independent findings + a GO/NO-GO, each objection marked blocking / non-blocking. Reviewers must not see each other's output.

## Step 3 — Consolidate

Merge and dedupe findings. Track each objection: who raised it, blocking?, status (open / resolved / accepted-with-reason). Any objection a reviewer marks **blocking** holds the verdict at NO-GO until it's resolved.

## Step 4 — Converge (the loop)

- On NO-GO: the blocking objections go back to the plan's author to fix or explicitly accept.
- Re-run the panel on the **revised version** — the exact version every reviewer now sees.
- **Success only when the reviewers converge to GO on the same unchanged version.**
- **Stop conditions:** if reviewers oscillate (the same disagreement repeats with no new evidence) or you hit the max-round budget, **stop and escalate to a human** with the open tradeoff stated. Never spin.

## Output

One consolidated verdict: **GO / NO-GO**, the **objection log** (reviewer → objection → blocking? → status), and **which configuration ran** (cross-tool, or host-only floor).

## Red flags — you're not running a panel

- You critiqued the plan yourself and wrote the verdict from one perspective.
- You never checked whether a second model/tool was available.
- One reviewer, or several with the same generic lens.
- You declared GO without every reviewer seeing the final, unchanged version.
- Cross-tool was unavailable and your output didn't say so.
