# claude-tools — Agent Guide

Single source of truth for AI coding agents in this repo. `CLAUDE.md` is a symlink to this file, so both Claude Code and AGENTS.md-aware tools read it. Explicit instructions in chat always win.

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

## Authoring skills (test-first)

Authoring skills is the repo's recurring activity — treat it as TDD for documentation (`superpowers:writing-skills`).

- **No skill without a failing baseline first.** Observe a throwaway subagent fail the task *without* the skill (RED), then write the skill, then confirm compliance *with* it (GREEN), then close loopholes (REFACTOR).
- **`description` = triggering conditions only** ("Use when…"); never summarize the workflow — agents follow the summary and skip the skill body.
- **Match the guidance form to the failure:** wrong-shaped output → positive recipe (state what the output *is*); a discipline skipped under pressure → prohibition + rationalization table + red-flags.
- **Orchestrators reuse, don't reinvent:** compose existing skills (e.g. `superpowers:brainstorming`) instead of duplicating them; let the pipeline shape pick the skills, not the reverse.
- Worked example + design & validation log: `specs/sdd-flow/spec.md` (the `sdd-flow` plugin: a 3-phase SDD orchestrator + `grilling` + `plan-review-panel`).

## Gotchas

- **Baseline tests need a no-guidance control.** A primed prompt (handing the agent the answer) or running in the wrong repo makes a baseline pass *falsely* — verify the control actually exhibits the failure before trusting a "skill works" result.
- **`AGENTS.md` is the source of truth; `CLAUDE.md` is a symlink to it** — edit `AGENTS.md`, and never replace the symlink with a regular file (some editors rewrite it).
- Some plugins bundle shell scripts (`zellij-tools/tools/`) alongside their SKILL.md
- Marketplace entry `tags` field maps to the official schema; avoid using `keywords`
