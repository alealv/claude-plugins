# claude-plugins

Personal collection of Claude Code plugins for development workflows, task automation, and specialized tools.

## Installation

Add this marketplace to Claude Code:

```
/plugin marketplace add aalvarez/claude-plugins
```

Then install individual plugins:

```
/plugin install justfile-expert@claude-plugins
/plugin install zellij-tools@claude-plugins
```

## Available Plugins

| Plugin | Type | Description |
|--------|------|-------------|
| **justfile-expert** | Skill | Expert guidance for Just task runner and justfiles |
| **zellij-tools** | Skill | Remote control Zellij terminal multiplexer sessions for interactive CLIs |
| **knowledge-arch** | Skills + Command + Hook | Scaffold & audit a layered agent-knowledge architecture across repos |
| **git-isolated-commit** | Skill | Commit in-progress changes to a target branch via a throwaway git worktree |
| **sdd-flow** | Skills | Loop-native spec-driven development: a 3-phase wizard (spec → plan+review → TDD) with human gates |

## Plugin Details

### justfile-expert

Expertise in the Just task runner: recipe syntax, attributes, groups, modules, cross-platform patterns, and troubleshooting. Includes a comprehensive reference document for advanced features.

### zellij-tools

Remote control Zellij terminal multiplexer sessions for interactive CLIs, parallel workflows, and long-running processes. Includes helper scripts for waiting on output patterns and finding sessions.

### knowledge-arch

Scaffold and audit a **layered agent-knowledge architecture** in any repo: graph-first code structure (Graphify), Diátaxis docs, a lean `AGENTS.md` (+ `CLAUDE.md` → `@AGENTS.md` wrapper), path-scoped `.claude/rules/`, `.claude/skills/` for procedures, machine-local auto-memory, and a versioned constitution — with size caps, "required rules in committed files (not memory)", and Codex parity via nested `AGENTS.md`. Ships the `setup-knowledge-arch` and `audit-knowledge-arch` skills, a `/audit-knowledge-arch` command, and a silent SessionStart drift nudge. Reuses Spec Kit (`/speckit.constitution`) and Graphify rather than reimplementing them. The full model is in `plugins/knowledge-arch/reference/methodology.md`.

### git-isolated-commit

Commit in-progress changes to a target branch via a throwaway git worktree — safe when a parallel agent has hopped `HEAD` or the working tree is dirty. Ships the `isolated-worktree-commit` skill.

### sdd-flow

Loop-native **spec-driven development** as a *wizard of loops*: each phase is an autonomous loop that converges on its own, then stops at a human approval gate before the next — **SPEC → PLAN+review → TDD IMPLEMENT**, gated by a Constitution precondition and a stop-condition invariant on every loop. Ships three skills: `sdd-flow` (the orchestrator), `grilling` (one-question-at-a-time adversarial design interview), and `plan-review-panel` (independent, adaptive cross-tool reviewer convergence — Claude + Codex when available). Reuses `superpowers:*`, `deep-research`, and Spec Kit rather than reimplementing them. The full design is in `specs/sdd-flow/spec.md`.

## License

See [LICENSE](LICENSE) for details.
