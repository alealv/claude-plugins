# Knowledge Architecture — the methodology

The canonical layered model. Both skills (`setup-knowledge-arch`, `audit-knowledge-arch`)
and the SessionStart hook reference this file — it is the single source of truth for the
methodology. Distilled from the Claude Code + OpenAI Codex memory/doc models that
converged in 2026, the agents.md standard, and graph-first code-intelligence practice.

## The core idea

**One home per knowledge type. Required rules live in committed files; machine-written
memory is a recall layer, not a source of truth.** This is the model Claude Code and Codex
(its 2026 "Memories" feature) both landed on.

## Where each kind of knowledge lives

| Knowledge | Home | Loads when | Why |
|-----------|------|-----------|-----|
| **Code structure / call-graph / blast-radius** | A knowledge graph (e.g. **Graphify**: `query`/`explain`/`path`/`affected`, + MCP) | on demand | AST-derived, always fresh, ~70x cheaper than reading files. **Never hand-maintain architecture prose** that duplicates it — it goes stale. |
| **How / why** (runbooks, ADRs, reference) | `docs/` (e.g. mkdocs, Diataxis) | on read/search | Human + agent reference. |
| **Always-apply rules, commands, safety, routing** | **`AGENTS.md`** (+ `CLAUDE.md` → `@AGENTS.md` wrapper) | every session | The cross-tool agent contract. Keep it lean (<150-200 lines / well under Codex's 32 KiB cap). |
| **Path-scoped gotchas** | `.claude/rules/*.md` with `paths:` frontmatter | when editing matching files | Conditional load = zero cost on unrelated work. Claude-only. |
| **Multi-step procedures** | **skills** (`.claude/skills/<name>/SKILL.md`) | on demand / when relevant | Recoveries & workflows. Not CLAUDE.md, not memory. |
| **Principles / non-negotiables** | a versioned `constitution.md` (e.g. Spec Kit `.specify/memory/constitution.md`) | referenced | Governance, amendment-tracked (SemVer). |
| **Cross-session operational lessons** | machine-local auto-memory (`MEMORY.md` index + topic files) | index every session | Recall layer the agent writes itself. **Not** a source of truth. |

## The rules

1. **Graph-first.** For "how does X work / what calls Y / blast-radius of Z", query the
   code graph. Don't restate code structure in prose anywhere — regenerate the graph instead.
2. **One source per fact.** Each fact lives in exactly one layer; every other place points
   to it. No duplication across docs / AGENTS / rules / memory.
3. **Required rules in committed files.** Anything that must always apply lives in
   `AGENTS.md` / docs / constitution — never only in machine-memory.
4. **Procedures are skills.** A multi-step procedure is a skill, not a CLAUDE.md section
   and not a memory topic file.
5. **Size caps (loading discipline):**
   - `AGENTS.md` / `CLAUDE.md`: target **< 200 lines** (community sweet spot ~150). Both
     load in full every session; `@import` does NOT save budget.
   - `AGENTS.md` combined with nested files: **< 32 KiB** (Codex truncates from the bottom).
   - auto-memory `MEMORY.md`: only the **first 200 lines / 25 KB** load each session —
     keep under ~24 KB or bottom entries drop silently. Index = terse one-line hooks;
     detail in topic files (loaded on demand).
6. **CLAUDE.md is a thin `@AGENTS.md` wrapper.** Claude reads `CLAUDE.md`, not `AGENTS.md`;
   the `@AGENTS.md` import (or a symlink) is the officially-recommended bridge so Claude and
   the agents.md ecosystem read one source. Add Claude-only notes below the import.
7. **Codex parity.** `.claude/rules/` is Claude-only. Codex reads **nested `AGENTS.md`**
   (root → cwd, deeper wins). Mirror the critical path-scoped rules as per-directory
   `AGENTS.md` files so Codex gets the same guidance.
8. **Enforcement vs context.** CLAUDE.md/AGENTS.md are *context*, not enforcement. A rule
   that must run at a fixed point (e.g. before commit) belongs in a **hook**, not prose.

## What this plugin does NOT own (adopt, don't rebuild)

- **Constitution layer** → Spec Kit `/speckit.constitution` (versioned principles).
- **Code layer** → Graphify (or another knowledge-graph tool).
- **CLAUDE.md upkeep** → optionally the `claude-md-management` plugin.

This plugin owns the **connective tissue** — the layered model, the size-cap discipline,
the Codex parity, and the audit — that no single built-in covers as of mid-2026.
