# CLAUDE.md

## Overview

`claude-plugins` is a Claude Code plugin marketplace. It contains a collection of plugins (skills and commands) installable via Claude Code's native `/plugin` system.

## Repository Structure

```
.claude-plugin/marketplace.json    # Marketplace catalog
plugins/
  <plugin-name>/
    .claude-plugin/plugin.json     # Plugin manifest
    commands/*.md                   # Slash commands (optional)
    skills/<name>/SKILL.md         # Skills (optional)
    README.md                      # Plugin documentation
```

## Adding a New Plugin

1. Create `plugins/<plugin-name>/`
2. Add `.claude-plugin/plugin.json` with name, version, description, author
3. Add `commands/` and/or `skills/` directories with content
4. Add entry to `.claude-plugin/marketplace.json` plugins array
5. Commit and push

## Plugin Conventions

- **Commands** use frontmatter: `description`, `argument-hint`, `allowed-tools`
- **Skills** use SKILL.md with frontmatter: `name`, `description`
- Keep SKILL.md under 500 lines; use `references/` for detailed docs
- Plugin names are kebab-case
