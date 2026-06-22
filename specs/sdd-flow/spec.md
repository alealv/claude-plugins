# SDD-Flow — loop-native spec-driven development orchestrator

> **Status:** spec / design v2 (2026-06-22). Rewritten **from scratch, tool-agnostic** — first we design the *ideal* pipeline (phases, artifact contracts, where humans gate vs where loops run autonomously), and only afterward map each piece to reusable skills. The previous draft was contaminated by the tools; this one inverts the order.
> **Scope note:** this describes *what the pipeline must be and do* first; the concrete skill mapping is at the end ("Skill / tool mapping", resolved 2026-06-22). We **write 3 skills** (`sdd-flow`, `plan-review-panel`, `grilling`) and **reuse** the rest (`deep-research`, `tdd`, `to-issues`, `loop`, `systematic-debugging`, Spec Kit, …).

## Goal

A single human-invoked orchestrator that runs the maintainer's spec-driven-development (SDD) workflow as a **loop-native pipeline**: idea → measurable contract → adversarially-sharpened spec → reviewed plan + tasks → TDD slice-by-slice implementation, where the definition of done is *evidence that every required outcome is proved*. It runs of its own accord between **human gates**, and stops at exactly the points where a person must decide, approve, or break a tie.

## Why

Every feature runs the same intricate, *iterative* sequence by hand. It is not linear — it is **nested loops**: refine the spec against its own contradictions, iterate plan ↔ review until independent reviewers converge, iterate implement ↔ tests until green-with-evidence. That intricacy is the whole reason it deserves a dedicated orchestrator instead of manual chaining. Modern agent practice (mid-2026) is unanimous that the unit of work is the **loop with a verifiable done-check**, not the one-shot prompt — and that every loop needs an anti-spin stop. This design encodes that.

## Two orthogonal axes (read this before the phases)

The previous draft confused "user-invoked vs model-invoked" (a skill-packaging detail) with the thing that actually structures the pipeline. There are **two independent axes**:

1. **Scope — per-project vs per-feature.** The **Constitution** (project principles, non-negotiables, tech constraints) is authored **once per project** and is the supreme document every later artifact is checked against. The **four phases** run **once per feature**. The Constitution sits *above* the phases as a persistent input and gate; it is not a phase.
2. **Control — "a wizard of loops".** The pipeline is a **wizard**: a fixed sequence of phases with a **human approval gate at every phase boundary**. But each phase is itself an **autonomous internal loop** — the model runs it to convergence on its own, then presents a *fully-reasoned* result and waits. Autonomy lives **inside** each phase; human judgment lives **between** phases. The human always **approves / modifies / refines**; a refine re-runs that phase's loop; an accept advances to the next phase. The sole exception is the final phase (implement): once the goal is locked it runs autonomously to done.

→ Consequence: `sdd-flow` is **one** human-invoked entry point. Within a phase it acts of its own accord (validating, exploring options, converging); at each boundary it halts with a complete proposal for the human to ratify. The gates are the design, not a limitation. Whatever skill-packaging rule applies later ("a user-invoked skill never invokes another user-invoked skill") falls out of this for free — the only human-invoked things are the entry and the boundary gates.

### Cross-cutting discipline (inside every phase loop)

Whenever anything **new** enters the design — a feature the user wants, an architecture, a library, a decision — the loop MUST **validate it against official documentation, community practice, and current best-practices**, exploring **multiple options**, *before* surfacing it. The phase never returns raw questions to the human: it returns **problems already identified, a proposed resolution for each, and a summary of what the sources/community say**. The human then rules per-item or refines the artifact → the loop re-runs. (Distinct from the architecture *challenge*, which is a single dedicated point — see Phase PLAN.)

## Artifact contracts (what Spec Kit contributes)

Spec Kit's real value is not its scripts — it is the **discipline of separated artifacts**, each with a strict job, plus a cross-artifact consistency gate. We adopt the contracts, tool-agnostically:

| Artifact | Scope | Must contain | Must NOT contain |
|----------|-------|--------------|------------------|
| **`constitution.md`** | per-project | Governing principles, non-negotiables, tech/style constraints, testing philosophy, the bar for "done". | Feature specifics. |
| **`spec.md`** | per-feature | The WHAT and WHY: user-facing behavior, scope (in/out), **measurable acceptance criteria**, edge cases. | The HOW (no stack, no architecture). |
| **`plan.md`** | per-feature | The HOW: architecture, data model, contracts/interfaces, tech choices — each **traceable to a Constitution principle**. | New requirements not in the spec. |
| **`tasks.md`** | per-feature | Ordered, dependency-aware, **vertical slices**, each with its own acceptance check and test intent. | Vague tasks without a done-check. |
| **`analyze` report** | per-feature | Cross-artifact consistency verdict: spec ↔ plan ↔ tasks ↔ constitution; every gap labeled. | Subjective design opinion (that is the reviewer panel's job). |
| **`GOAL.md`** | per-feature | The **completion contract**: every required outcome, each marked proved / weak / missing, with the evidence that proves it; iteration budget; approval boundaries. | Anything unverifiable. |

Two artifacts deserve emphasis because they are the load-bearing additions over plain Spec Kit:

- **`GOAL.md` = completion contract** (Loop Library #15 + Goal Forge #47), and it belongs to **implementation**. It is **not** written upfront — the goal only becomes fully *known* once the spec's measurable criteria **and** the plan's test/evaluation method exist. So `GOAL.md` **crystallizes at the PLAN→IMPLEMENT boundary** and is then the single source of truth the IMPLEMENT phase runs against (via the native goal/loop machinery) until every outcome is proved.
- **`analyze` and the architecture challenge are two different things.** `analyze` is **mechanical**: are spec ↔ plan ↔ tasks ↔ constitution internally consistent? The **architecture challenge** is **judgment at one dedicated point**: "why this implementation/architecture — is there a better alternative the sources support?" Both live inside the PLAN phase loop.

## The three phases (per-feature) — a wizard of loops

Each phase is an autonomous internal loop; `▸ GATE` marks the human approve/modify/refine boundary between phases.

```
┌─ CONSTITUTION (per-project, REQUIRED precondition) ── supreme input to every phase ─┐
│     if missing → sdd-flow halts and offers to generate it before any feature work    │
│                                                                                     │
│  PHASE 1 — SPEC                       [Goal Forge #47 + Devil's-Advocate #32]       │
│     LOOP: draft spec.md → for each new feature/decision, validate vs official       │
│        docs + community + best-practices, explore multiple options → converge       │
│     presents: spec.md (measurable acceptance criteria) + every problem found,       │
│        each with a proposed resolution + what the sources say                       │
│     DONE: no open ambiguity, criteria verifiable, sources cited                     │
│     STOP: same objection twice w/o new evidence → surface to human                  │
│     ▸ GATE: human approves / modifies / refines spec  (refine → re-loop)            │
│                                                                                     │
│  PHASE 2 — PLAN   [Prepare #48 + Multi-LLM #33 + Groundtruth #38]                   │
│     LOOP: clarify → checklist (quality gate) → plan.md → tasks.md (vertical          │
│        slices) → analyze (mechanical: spec↔plan↔tasks↔constitution) → if gaps,       │
│        iterate to fix all                                                            │
│        ▸ the ONE architecture challenge: "why this design — better alternative?"     │
│        ▸ adaptive cross-tool reviewer convergence (host always + other tool if        │
│          enabled; approve same unchanged version)                                    │
│     presents: plan + tasks + analyze verdict + summary of decisions taken & why     │
│     >>> GOAL.md crystallizes here (spec criteria + test/eval method = the goal) <<<  │
│     DONE: analyze clean, reviewers converged, all decisions justified               │
│     STOP: oscillation / max-rounds → human breaks the tie                           │
│     ▸ GATE: human approves "start building"  (refine → re-loop)                     │
│                                                                                     │
│  PHASE 3 — IMPLEMENT   [Builder-Reviewer #14 + Completion-Contract #15 +            │
│     runs autonomously against GOAL.md (native goal/loop):   Quality-Streak #28]     │
│     for each vertical slice:                                                        │
│        failing test → build (maker) → independent verify (checker: revert/          │
│           mutation proves the test) → green → commit → next slice                    │
│        on repeated failure → bounded diagnosis sub-loop                             │
│        update GOAL.md: mark each outcome proved / weak / missing                     │
│     DONE (THE GOAL): every slice green AND every GOAL.md outcome proved w/ evidence  │
│     STOP: blocked / stalled / budget exhausted → human                             │
│     ▸ GATE: human approves anything destructive / production-facing                 │
└───────────────────────────────────────────────────────────────────────────────────┘
```

### Reviewer convergence — adaptive cross-tool (PHASE 2 pre-check)

Before PHASE 2 returns the plan to the human, it runs an **independent reviewer pre-check** so the human is the *second* filter, not the first. The panel is **adaptive and best-effort**, using only the tools currently enabled:

- **Always** review on the **host** the orchestrator runs in — Claude → Claude reviewer subagents; Codex → Codex reviewers.
- **If the other tool is available**, add it as a genuinely independent reviewer: running in Claude → *also* run Codex; running in Codex → *also* run Claude. This is the only configuration that delivers true Multi-LLM Convergence (#33) — two **different model families** must approve the **same unchanged version**, halting on oscillation.
- **If the other tool is not enabled/installed**, degrade gracefully to **host-only**, using **distinct review lenses** (e.g. correctness / simplicity / Constitution-alignment) rather than redundant generic reviewers — never an echo, never a hard failure for a missing tool.

→ Cross-tool is the *target* (Clodex-style independence, #12 + #33); host-only-with-lenses is the *floor*. The orchestrator detects what is enabled and picks the strongest available configuration automatically.

## Stop-condition invariant (non-negotiable, every loop)

Every autonomous loop MUST carry all three: **(1)** a verifiable **done-check**, **(2)** a **max-iterations budget**, **(3)** **stall detection** — same finding twice without new evidence, or no progress → **defer to a human** rather than spin. This is the single most repeated pattern across all 50 Loop-Library entries; it is baked into all three phases above.

## Design sources (Loop Library + Spec Kit → our elements)

| Our element | Loop Library | Spec Kit |
|-------------|--------------|----------|
| Constitution as supreme gate | — | `/constitution` + `/analyze` alignment |
| P1 spec + source-validation | Goal Forge #47, Devil's-Advocate #32 | `/specify` |
| P1 cross-cutting validation | Groundtruth #38 (evidence-based) | — |
| P2 clarify/plan/tasks | Prepare-a-New-Project #48 | `/clarify`, `/plan`, `/tasks` |
| P2 analyze gate | Groundtruth #38 | `/analyze` |
| P2 architecture challenge | Devil's-Advocate #32 (one point) | — |
| P2 reviewer convergence (adaptive cross-tool) | Multi-LLM Convergence #33, Clodex #12 | (none — our addition) |
| P2→P3 GOAL crystallizes | Completion-Contract #15, Goal Forge #47 | — |
| P3 build/verify | Builder-Reviewer #14, Harness #13, Quality-Streak #28 | `/implement` |
| P3 diagnosis sub-loop | Ticket-to-PR #10 | — |
| stop invariant | ubiquitous (#11, #32, #33, #15, …) | — |

## Open decisions (to resolve as we refine)

- ~~Constitution lifecycle in a repo that has none~~ — **RESOLVED (verified vs Spec Kit + community, 2026-06-22):** `constitution.md` is a **required precondition** (matches Spec Kit, where it is the first step and the supreme gate `analyze` enforces as `MUST`→CRITICAL). If missing, `sdd-flow` **halts and offers to generate it** (one-time, per-project) before any feature work — precondition with an escape hatch, never silent opt-out.
- ~~`GOAL.md` ↔ native `/goal`~~ — **RESOLVED:** `GOAL.md` is the Phase 3 done-check, a plain **versioned file** (not tied to any native `/goal` command, which isn't reliably present), driven by the installed `loop` skill as a self-paced goal loop.
- ~~Reviewer independence in Phase 2~~ — **RESOLVED:** adaptive cross-tool pre-check (host always + other tool if enabled, host-only-with-lenses as floor). See "Reviewer convergence" above.
- ~~`analyze` strength~~ — **RESOLVED:** we **install Spec Kit** in the repo, so `analyze` is **mechanical** — the real `.specify/scripts` cross-check, not a checklist-prompt.
- ~~Slice granularity in Phase 3~~ — **RESOLVED:** `tasks.md` defines the vertical slices (Spec Kit `tasks`, optionally seeded by `to-issues`); no separate re-slice step at implementation time.

## Skill / tool mapping (RESOLVED 2026-06-22)

The pipeline shape (locked above) drove these choices — never the reverse. Inventory was taken against the *actual* environment, not assumed.

### What we WRITE (3 deliverables → ship to claude-tools)

| Skill | Invocation | What it is |
|-------|-----------|-----------|
| **`sdd-flow`** | user-invoked (orchestrator) | The wizard-of-loops: 3 phases, their boundary gates, the Constitution precondition, the Spec-Kit-or-replicate bridge, GOAL.md as the implement done-check. The only human-invoked entry. |
| **`plan-review-panel`** | model-invoked (discipline) | The Phase 2 **adaptive cross-tool** reviewer: host reviewers always + Codex (or Claude) if enabled; converge on the same unchanged version; host-only-with-lenses as floor. |
| **`grilling`** | model-invoked (discipline) | Custom adversarial-interview skill, **written from scratch** based on mattpocock's `grilling` + Loop-Library **Devil's-Advocate #32** (critic argues the design is wrong; objections logged; resolve or accept-explicitly; stop on same-issue-2×). Drives Phase 1 sharpening and the Phase 2 architecture challenge. |

### What we REUSE (installed — verified present)

| Pipeline element | Skill | Source |
|------------------|-------|--------|
| Constitution (precondition) | **`/speckit.constitution`** → `.specify/memory/constitution.md` | Spec Kit (install). `knowledge-arch` already delegates to this same file. |
| P1 spec authoring | `to-prd` / `brainstorming` | personal / Superpowers |
| P1 cross-cutting source validation | `deep-research` | plugin |
| P2 clarify/checklist/plan/tasks/analyze | Spec Kit (`.specify/scripts` — **install**) | Spec Kit |
| P2 task / vertical slices | `to-issues` (seeds `tasks.md`) | personal |
| P2 architecture challenge | `grilling` (our new skill) + `improve-codebase-architecture` | ours / personal |
| P3 TDD maker | `tdd` | personal + plugin |
| P3 goal/loop done-check | `loop` (drives `GOAL.md`) | plugin |
| P3 builder→reviewer / verify | `verify`, `code-review`, `subagent-driven-development` | plugin |
| P3 diagnosis sub-loop | `systematic-debugging` (substitutes mattpocock `diagnosing-bugs`) | plugin |
| P3 isolation | `using-git-worktrees` | plugin |

### Key decisions (resolved via grilling + source-validation)

- **Install Spec Kit** in the repo (`specify init`) → real `.specify/scripts` + templates; `analyze` is mechanical, not a prompt. Constitution = `/speckit.constitution` (the file `analyze` enforces, and the one `knowledge-arch` delegates to — one file, no conflict).
- **Cross-tool reviewer is real here:** `codex` is installed (`/opt/homebrew/bin/codex`), so Phase 2 gets genuine Multi-LLM convergence, not a Claude echo.
- **`grilling` is ours to write**, fusing mattpocock's interview discipline with Devil's-Advocate #32 — used in both Phase 1 (sharpen spec) and Phase 2 (architecture challenge).

## Sources

- Loop Library — named loop patterns + stop conditions (https://signals.forwardfuture.ai/loop-library/), reviewed in full (50 loops); 8 are load-bearing here (#10, #13, #14, #15, #28, #32, #33, #38, #47, #48).
- Spec Kit — artifact separation and cross-artifact consistency discipline. **Verified 2026-06-22** against the official repo + community: current workflow is `constitution → specify → clarify → checklist → plan → tasks → analyze → implement` (`/checklist` added ~June 2026, v0.10.0); constitution is the required first step and the supreme gate `analyze` enforces (`MUST`→CRITICAL). Sources: github/spec-kit, github.github.com/spec-kit, Microsoft Developer blog, community deep-dives.
- Loop engineering / goal+loop / maker-checker best practice, mid-2026.
