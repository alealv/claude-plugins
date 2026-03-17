# CLAUDE.md

## Overview

`claude-plugins` is a Claude Code plugin marketplace — a personal collection of plugins (commands, skills, agents, hooks, and MCP configs) installable via Claude Code's native `/plugin` system.

## Repository Structure

```
.claude-plugin/marketplace.json  # Marketplace catalog ($schema-validated)
plugins/
  justfile-expert/               # Just task runner guidance (skill + references)
  zellij-tools/                  # Zellij terminal multiplexer control (skill + shell tools)
```

Each plugin contains `.claude-plugin/plugin.json` (required manifest) and one or more of:

- `commands/*.md` — Slash commands
- `skills/<name>/SKILL.md` — Packaged expertise (+ optional `references/`)
- `agents/*.md` — Subagent definitions
- `hooks/hooks.json` — Event-based automation (PreToolUse, PostToolUse, Stop)
- `.mcp.json` — Bundled MCP server configuration

## Adding a New Plugin

1. Create `plugins/<plugin-name>/`
2. Add `.claude-plugin/plugin.json` with name, version, description, author
3. Add component directories (commands, skills, agents, hooks, .mcp.json)
4. Add entry to `.claude-plugin/marketplace.json` plugins array
5. Commit and push

## Plugin Conventions

- **Commands** use frontmatter: `description`, `argument-hint`, `allowed-tools`
- **Skills** use SKILL.md with frontmatter: `name`, `description`
- Keep SKILL.md under 500 lines; use `references/` for detailed docs
- Plugin names are kebab-case
- No build system or dependencies — plugins are pure Markdown/shell/JS

## Gotchas

- Some plugins bundle shell scripts (`zellij-tools/tools/`) alongside their SKILL.md
- Marketplace entry `tags` field maps to the official schema; avoid using `keywords`
