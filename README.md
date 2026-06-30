# claude-plugins

Personal collection of Claude Code plugins for development workflows, task automation, and specialized tooling — installable via Claude Code's native `/plugin` system.

## Installation

Add the marketplace once:

```
/plugin marketplace add alealv/claude-plugins
```

Then install any plugin by name (the marketplace is registered as `alealv-plugins`):

```
/plugin install sdd-flow@alealv-plugins
/plugin install knowledge-arch@alealv-plugins
/plugin install git-isolated-commit@alealv-plugins
/plugin install justfile-expert@alealv-plugins
/plugin install zellij-tools@alealv-plugins
```

## Available Plugins

| Plugin | Type | Description |
|--------|------|-------------|
| **justfile-expert** | Skill | Expert guidance for the Just task runner and justfiles |
| **zellij-tools** | Skill | Remote-control Zellij terminal multiplexer sessions for interactive CLIs and parallel workflows |
| **knowledge-arch** | Skills + Command + Hook | Scaffold & audit a layered agent-knowledge architecture across repos |
| **git-isolated-commit** | Skill | Commit in-progress changes to a target branch via a throwaway git worktree |
| **sdd-flow** | Skills | Loop-native spec-driven development: a 3-phase wizard (spec → plan + review → TDD) with human gates |

## Plugin Details

### justfile-expert

Expertise in the Just task runner: recipe syntax, attributes, groups, modules, cross-platform patterns, and troubleshooting. Includes a comprehensive reference document for advanced features.

### zellij-tools

Remote-control Zellij terminal multiplexer sessions for interactive CLIs, parallel workflows, and long-running processes. Includes helper scripts for waiting on output patterns and finding sessions.

### knowledge-arch

Scaffold and audit a **layered agent-knowledge architecture** in any repo: graph-first code structure (Graphify), Diátaxis docs, a lean `AGENTS.md` (+ `CLAUDE.md` → `@AGENTS.md` wrapper), path-scoped `.claude/rules/`, `.claude/skills/` for procedures, machine-local auto-memory, and a versioned constitution — with size caps, "required rules in committed files (not memory)", and Codex parity via nested `AGENTS.md`. Ships the `setup-knowledge-arch` and `audit-knowledge-arch` skills, a `/audit-knowledge-arch` command, and a silent SessionStart drift nudge. Reuses Spec Kit (`/speckit.constitution`) and Graphify rather than reimplementing them. Full model: `plugins/knowledge-arch/reference/methodology.md`.

### git-isolated-commit

Commit in-progress changes to a target branch via a throwaway git worktree — safe when a parallel agent has hopped `HEAD` or the working tree is dirty. Ships the `isolated-worktree-commit` skill.

### sdd-flow

Loop-native **spec-driven development**, run as a *wizard of loops*: each phase is an autonomous loop that converges on its own, then stops at a human approval gate before the next.

```
Constitution (precondition) → SPEC →[gate]→ PLAN + review →[gate]→ TDD IMPLEMENT →[gate]
```

- **Phase 1 · SPEC** — brainstorm + validate against sources + adversarially sharpen, into a `spec.md` with measurable acceptance criteria.
- **Phase 2 · PLAN** — clarify/plan/tasks/analyze (Spec Kit), one architecture challenge, then an independent **cross-tool** reviewer pass (Claude + Codex when available) that must converge on GO. `GOAL.md` (the completion contract) crystallizes here.
- **Phase 3 · IMPLEMENT** — runs autonomously against `GOAL.md`: TDD per slice, an independent checker, commit on green; done only when every outcome is proved with evidence.

Every loop carries a stop-condition invariant (done-check + iteration budget + stall → escalate). Ships three skills — `sdd-flow` (the orchestrator), `grilling` (one-question-at-a-time adversarial design interview), and `plan-review-panel` (adaptive cross-tool reviewer convergence). Reuses `superpowers:*`, `deep-research`, and Spec Kit rather than reimplementing them. Full design: `specs/sdd-flow/spec.md`.

## Repository

Plugin sources live under `plugins/<name>/`; the catalog is `.claude-plugin/marketplace.json`. Agent/contributor guidance is in `AGENTS.md` (`CLAUDE.md` is a symlink to it).

## License

See [LICENSE](LICENSE) for details.
