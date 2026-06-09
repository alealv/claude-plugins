---
name: setup-knowledge-arch
description: Scaffold or repair a layered agent-knowledge architecture in the current repo — lean AGENTS.md + CLAUDE.md @import wrapper, path-scoped .claude/rules, .claude/skills, a versioned constitution, graph-first code layer (Graphify), nested AGENTS.md for Codex parity, and the MEMORY.md convention. Use when setting up a new project for AI agents, standardizing an existing repo's agent docs, or when the user asks to "set up the knowledge architecture / agent docs / memory + constitution".
---

# Set up the knowledge architecture

Read this plugin's `reference/methodology.md` first — it is the canonical model (the
layer table, the rules, the size caps). Apply it **idempotently**: only create what's
missing, never clobber existing content without showing a diff and confirming.

Work through the layers in order. After each, state what you did (created / already OK /
needs the user's input).

## 0. Survey
- Is this a git repo? What language/build tool (`package.json`, `pyproject.toml`, `go.mod`, Ansible roles, etc.)? Note the test/lint/build commands.
- Inventory what already exists: `AGENTS.md`, `CLAUDE.md`, `.claude/rules/`, `.claude/skills/`, `docs/`, a constitution (`.specify/memory/constitution.md`), a code graph (`graphify-out/`).

## 1. AGENTS.md (the cross-tool contract)
- **Missing** → create a lean one (<200 lines): a 2-line project overview, a commands table (build/test/lint), a short safety/guardrails section, a **Knowledge Architecture** section (copy the layer table from `reference/methodology.md`, adapted), and pointers to `docs/`. No code dumps, no volatile changelog.
- **Present** → check it's <200 lines and has a Knowledge Architecture section + a graph-first line. Offer to trim volatile history (per-feature changelogs) out to `docs/` and add the missing section.

## 2. CLAUDE.md → @AGENTS.md wrapper
- Ensure the FIRST line is `@AGENTS.md`. **Missing** → create `CLAUDE.md` containing `@AGENTS.md` plus any Claude-only notes below it. **Present but not importing** → add the `@AGENTS.md` import; move shared content into AGENTS.md so there's one source.

## 3. .claude/rules/ (path-scoped, Claude-only)
- Create `.claude/rules/` if absent. For each distinct domain with recurring gotchas (e.g. a subsystem, secrets/config, infra), create `<domain>.md` with `paths:` glob frontmatter that points to the canonical `docs/` reference — terse, pointer-based, not a copy. Rules without `paths:` load every session; only use that for truly always-on guidance.

## 4. .claude/skills/ (procedures)
- Ensure `.claude/skills/` exists. Any multi-step recovery/workflow that currently lives in CLAUDE.md or memory should become a skill here (`<name>/SKILL.md` with a clear `description:` trigger). Don't inline procedures in AGENTS.md/CLAUDE.md.

## 5. Constitution (principles) — adopt, don't rebuild
- If Spec Kit is present (`.specify/`), run **`/speckit.constitution`** to create/update a versioned `constitution.md`. Otherwise create `docs/explanation/constitution.md` (or an ADR log) with the project's non-negotiable principles and a SemVer + changelog. Include a **Knowledge Architecture** principle (one home per fact; graph-first; required rules in committed files, not memory).

## 6. Code layer (graph-first) — adopt Graphify
- If `graphify` is available, build the graph (`graphify .`) so code-structure questions are answered by `graphify query/explain/path/affected` instead of prose. Add the **graph-first rule** to AGENTS.md: "for code structure / blast-radius, query the graph; don't hand-maintain architecture prose." If no graph tool, note it as the recommended code layer.

## 7. Codex parity (nested AGENTS.md)
- Codex reads nested `AGENTS.md` (root → cwd), not `.claude/rules/`. For each critical path-scoped rule, offer to create a slim per-directory `AGENTS.md` (e.g. `src/AGENTS.md`, `roles/opnsense/AGENTS.md`) mirroring the rule and pointing to the same `docs/`.

## 8. Memory convention (machine-local)
- Auto-memory is machine-local (`~/.claude/projects/<project>/memory/`), not in the repo. Don't scaffold it in the repo. State the convention: `MEMORY.md` is a terse index (one line per topic, < 24 KB); detail goes in topic files; **procedures become skills, not memory**; required rules go in committed files.

## 9. Verify
- Run the `audit-knowledge-arch` skill to produce a health report (size caps, missing layers, drift). Summarize what was created and what still needs the user's decision.

Keep every artifact lean and pointer-based. The goal is *one home per fact* with the
right load timing — not more prose.
