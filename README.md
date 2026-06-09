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

## Plugin Details

### justfile-expert

Expertise in the Just task runner: recipe syntax, attributes, groups, modules, cross-platform patterns, and troubleshooting. Includes a comprehensive reference document for advanced features.

### zellij-tools

Remote control Zellij terminal multiplexer sessions for interactive CLIs, parallel workflows, and long-running processes. Includes helper scripts for waiting on output patterns and finding sessions.

### knowledge-arch

Scaffold and audit a **layered agent-knowledge architecture** in any repo: graph-first code structure (Graphify), Diátaxis docs, a lean `AGENTS.md` (+ `CLAUDE.md` → `@AGENTS.md` wrapper), path-scoped `.claude/rules/`, `.claude/skills/` for procedures, machine-local auto-memory, and a versioned constitution — with size caps, "required rules in committed files (not memory)", and Codex parity via nested `AGENTS.md`. Ships the `setup-knowledge-arch` and `audit-knowledge-arch` skills, a `/audit-knowledge-arch` command, and a silent SessionStart drift nudge. Reuses Spec Kit (`/speckit.constitution`) and Graphify rather than reimplementing them. The full model is in `plugins/knowledge-arch/reference/methodology.md`.

## License

See [LICENSE](LICENSE) for details.
