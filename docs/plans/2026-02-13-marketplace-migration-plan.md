# Marketplace Migration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Convert `claude-tools` from a Python CLI installer to a standard Claude Code plugin marketplace (`claude-plugins`).

**Architecture:** Create a `.claude-plugin/marketplace.json` at the repo root listing 6 plugins under `plugins/`. Each plugin has its own `.claude-plugin/plugin.json` and contains commands and/or skills in standard directories. All existing content is preserved, only restructured.

**Tech Stack:** Claude Code plugin system (marketplace.json, plugin.json, SKILL.md, command .md files)

---

### Task 1: Create marketplace scaffold

**Files:**
- Create: `.claude-plugin/marketplace.json`
- Create: `plugins/` (directory)

**Step 1: Create the marketplace manifest**

Create `.claude-plugin/marketplace.json`:

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "claude-plugins",
  "version": "1.0.0",
  "description": "Personal collection of Claude Code plugins for development workflows, task automation, and specialized tools",
  "owner": {
    "name": "aalvarez"
  },
  "plugins": [
    {
      "name": "commit-commands",
      "description": "Git workflow commands: smart commit, code review, and test generation",
      "version": "1.0.0",
      "source": "./plugins/commit-commands",
      "category": "development",
      "keywords": ["git", "commit", "review", "testing"]
    },
    {
      "name": "justfile-expert",
      "description": "Expert guidance for Just task runner and justfiles",
      "version": "1.0.0",
      "source": "./plugins/justfile-expert",
      "category": "development",
      "keywords": ["just", "justfile", "task-runner", "build"]
    },
    {
      "name": "tmux-tools",
      "description": "Remote control tmux sessions for interactive CLIs",
      "version": "1.0.0",
      "source": "./plugins/tmux-tools",
      "category": "development",
      "keywords": ["tmux", "terminal", "session"]
    },
    {
      "name": "sudolang-prompter",
      "description": "Create efficient LLM prompts using SudoLang pseudolanguage syntax",
      "version": "1.0.0",
      "source": "./plugins/sudolang-prompter",
      "category": "productivity",
      "keywords": ["prompt-engineering", "sudolang", "llm"]
    },
    {
      "name": "web-browser",
      "description": "Browse and interact with web pages via Chrome DevTools Protocol",
      "version": "1.0.0",
      "source": "./plugins/web-browser",
      "category": "development",
      "keywords": ["browser", "chrome", "cdp", "web"]
    },
    {
      "name": "agent-commands",
      "description": "Session handoff, pickup, release, and changelog workflow commands",
      "version": "1.0.0",
      "source": "./plugins/agent-commands",
      "category": "productivity",
      "keywords": ["handoff", "session", "release", "workflow"]
    }
  ]
}
```

**Step 2: Create plugins directory**

```bash
mkdir -p plugins
```

**Step 3: Commit**

```bash
git add .claude-plugin/marketplace.json
git commit -m "feat: add marketplace manifest scaffold"
```

---

### Task 2: Create commit-commands plugin

**Files:**
- Create: `plugins/commit-commands/.claude-plugin/plugin.json`
- Move: `commands/commit.md` → `plugins/commit-commands/commands/commit.md`
- Move: `commands/code-review.md` → `plugins/commit-commands/commands/code-review.md`
- Move: `commands/generate-tests.md` → `plugins/commit-commands/commands/generate-tests.md`

**Step 1: Create plugin directory structure**

```bash
mkdir -p plugins/commit-commands/.claude-plugin
mkdir -p plugins/commit-commands/commands
```

**Step 2: Create plugin.json**

Create `plugins/commit-commands/.claude-plugin/plugin.json`:

```json
{
  "name": "commit-commands",
  "version": "1.0.0",
  "description": "Git workflow commands: smart commit, code review, and test generation",
  "author": {
    "name": "aalvarez"
  }
}
```

**Step 3: Move command files**

```bash
git mv commands/commit.md plugins/commit-commands/commands/commit.md
git mv commands/code-review.md plugins/commit-commands/commands/code-review.md
git mv commands/generate-tests.md plugins/commit-commands/commands/generate-tests.md
```

**Step 4: Commit**

```bash
git add plugins/commit-commands/
git commit -m "feat: create commit-commands plugin"
```

---

### Task 3: Create justfile-expert plugin

**Files:**
- Create: `plugins/justfile-expert/.claude-plugin/plugin.json`
- Move: `skills/justfile-expert/` → `plugins/justfile-expert/skills/justfile-expert/`

**Step 1: Create plugin directory structure**

```bash
mkdir -p plugins/justfile-expert/.claude-plugin
mkdir -p plugins/justfile-expert/skills
```

**Step 2: Create plugin.json**

Create `plugins/justfile-expert/.claude-plugin/plugin.json`:

```json
{
  "name": "justfile-expert",
  "version": "1.0.0",
  "description": "Expert guidance for Just task runner and justfiles",
  "author": {
    "name": "aalvarez"
  }
}
```

**Step 3: Move skill directory**

```bash
git mv skills/justfile-expert plugins/justfile-expert/skills/justfile-expert
```

**Step 4: Commit**

```bash
git add plugins/justfile-expert/
git commit -m "feat: create justfile-expert plugin"
```

---

### Task 4: Create tmux-tools plugin

**Files:**
- Create: `plugins/tmux-tools/.claude-plugin/plugin.json`
- Move: `skills/tmux/` → `plugins/tmux-tools/skills/tmux/`

**Step 1: Create plugin directory structure**

```bash
mkdir -p plugins/tmux-tools/.claude-plugin
mkdir -p plugins/tmux-tools/skills
```

**Step 2: Create plugin.json**

Create `plugins/tmux-tools/.claude-plugin/plugin.json`:

```json
{
  "name": "tmux-tools",
  "version": "1.0.0",
  "description": "Remote control tmux sessions for interactive CLIs",
  "author": {
    "name": "aalvarez"
  }
}
```

**Step 3: Move skill directory**

```bash
git mv skills/tmux plugins/tmux-tools/skills/tmux
```

**Step 4: Commit**

```bash
git add plugins/tmux-tools/
git commit -m "feat: create tmux-tools plugin"
```

---

### Task 5: Create sudolang-prompter plugin

**Files:**
- Create: `plugins/sudolang-prompter/.claude-plugin/plugin.json`
- Move: `skills/sudolang-prompter/` → `plugins/sudolang-prompter/skills/sudolang-prompter/`

**Step 1: Create plugin directory structure**

```bash
mkdir -p plugins/sudolang-prompter/.claude-plugin
mkdir -p plugins/sudolang-prompter/skills
```

**Step 2: Create plugin.json**

Create `plugins/sudolang-prompter/.claude-plugin/plugin.json`:

```json
{
  "name": "sudolang-prompter",
  "version": "1.0.0",
  "description": "Create efficient LLM prompts using SudoLang pseudolanguage syntax",
  "author": {
    "name": "aalvarez"
  }
}
```

**Step 3: Move skill directory**

```bash
git mv skills/sudolang-prompter plugins/sudolang-prompter/skills/sudolang-prompter
```

**Step 4: Commit**

```bash
git add plugins/sudolang-prompter/
git commit -m "feat: create sudolang-prompter plugin"
```

---

### Task 6: Create web-browser plugin

**Files:**
- Create: `plugins/web-browser/.claude-plugin/plugin.json`
- Move: `skills/web-browser/` → `plugins/web-browser/skills/web-browser/`

**Step 1: Create plugin directory structure**

```bash
mkdir -p plugins/web-browser/.claude-plugin
mkdir -p plugins/web-browser/skills
```

**Step 2: Create plugin.json**

Create `plugins/web-browser/.claude-plugin/plugin.json`:

```json
{
  "name": "web-browser",
  "version": "1.0.0",
  "description": "Browse and interact with web pages via Chrome DevTools Protocol",
  "author": {
    "name": "aalvarez"
  }
}
```

**Step 3: Move skill directory**

```bash
git mv skills/web-browser plugins/web-browser/skills/web-browser
```

**Step 4: Commit**

```bash
git add plugins/web-browser/
git commit -m "feat: create web-browser plugin"
```

---

### Task 7: Create agent-commands plugin

The `skills/agent-commands-main/` files are actually commands (they use `$ARGUMENTS`). They need frontmatter added and to be moved into `commands/` format.

**Files:**
- Create: `plugins/agent-commands/.claude-plugin/plugin.json`
- Move+modify: `skills/agent-commands-main/common/handoff.md` → `plugins/agent-commands/commands/handoff.md`
- Move+modify: `skills/agent-commands-main/common/pickup.md` → `plugins/agent-commands/commands/pickup.md`
- Move+modify: `skills/agent-commands-main/specific/make-release.md` → `plugins/agent-commands/commands/make-release.md`
- Move+modify: `skills/agent-commands-main/specific/update-changelog.md` → `plugins/agent-commands/commands/update-changelog.md`

**Step 1: Create plugin directory structure**

```bash
mkdir -p plugins/agent-commands/.claude-plugin
mkdir -p plugins/agent-commands/commands
```

**Step 2: Create plugin.json**

Create `plugins/agent-commands/.claude-plugin/plugin.json`:

```json
{
  "name": "agent-commands",
  "version": "1.0.0",
  "description": "Session handoff, pickup, release, and changelog workflow commands",
  "author": {
    "name": "aalvarez"
  }
}
```

**Step 3: Move command files and add frontmatter**

Move each file and prepend YAML frontmatter:

`plugins/agent-commands/commands/handoff.md` — prepend:
```yaml
---
description: Create a detailed handoff plan for continuing work in a new session
argument-hint: [purpose]
allowed-tools: Read, Grep, Glob, Bash(git:*), Write
---
```

`plugins/agent-commands/commands/pickup.md` — prepend:
```yaml
---
description: Resume work from a previous handoff session
argument-hint: [handoff-filename]
allowed-tools: Read, Bash(ls:*), Bash(grep:*), Bash(echo:*), Glob
---
```

`plugins/agent-commands/commands/make-release.md` — prepend:
```yaml
---
description: Make a versioned release of the repository
argument-hint: [version] | patch | minor | major
allowed-tools: Read, Bash, Edit, Write
---
```

`plugins/agent-commands/commands/update-changelog.md` — prepend:
```yaml
---
description: Update CHANGELOG.md with changes since the last release
argument-hint: [baseline-version]
allowed-tools: Read, Edit, Bash(git:*)
---
```

```bash
git mv skills/agent-commands-main/common/handoff.md plugins/agent-commands/commands/handoff.md
git mv skills/agent-commands-main/common/pickup.md plugins/agent-commands/commands/pickup.md
git mv skills/agent-commands-main/specific/make-release.md plugins/agent-commands/commands/make-release.md
git mv skills/agent-commands-main/specific/update-changelog.md plugins/agent-commands/commands/update-changelog.md
```

Then edit each file to prepend the frontmatter.

**Step 4: Commit**

```bash
git add plugins/agent-commands/
git commit -m "feat: create agent-commands plugin with frontmatter"
```

---

### Task 8: Remove Python CLI and packaging

Remove all Python-specific files that are no longer needed.

**Files to delete:**
- `src/` (entire directory)
- `tests/` (entire directory)
- `pyproject.toml`
- `config/` (entire directory)
- `scripts/` (entire directory)
- `justfile`
- `mkdocs.yml`
- `duties.py`
- `.python-version`
- `uv.lock`
- `.copier-answers.yml`
- `repro_issue.py`
- `debug_width.log`
- `dist/` (build artifacts)
- `site/` (built docs)
- `docs/` (MkDocs sources — keep only `docs/plans/`)
- `.github/workflows/ci.yml`
- `.github/workflows/release.yml`
- `.github/ISSUE_TEMPLATE/` (Python-specific issue templates)
- `.github/pull_request_template.md`
- `.github/FUNDING.yml`
- `specs/` (old spec work)
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `CHANGELOG.md`

**Step 1: Remove old source directories**

```bash
git rm -r src/ tests/ config/ scripts/ docs/.overrides docs/architecture.md docs/changelog.md docs/claude-configuration.md docs/code_of_conduct.md docs/contributing.md docs/credits.md docs/css docs/index.md docs/js docs/license.md docs/reference
git rm -r specs/ .github/ISSUE_TEMPLATE .github/FUNDING.yml .github/pull_request_template.md .github/workflows/
```

**Step 2: Remove old root files**

```bash
git rm pyproject.toml justfile mkdocs.yml duties.py .python-version .copier-answers.yml repro_issue.py debug_width.log CONTRIBUTING.md CODE_OF_CONDUCT.md CHANGELOG.md
```

**Step 3: Remove old content directories**

```bash
git rm -r commands/
git rm -r skills/justfile-expert.skill skills/README.md skills/agent-commands-main/.gitignore hooks/README.md
rmdir skills/agent-commands-main/common skills/agent-commands-main/specific skills/agent-commands-main skills hooks commands 2>/dev/null || true
```

**Step 4: Clean untracked build artifacts**

```bash
rm -rf dist/ site/ .venv/ .pdm-build/ .pytest_cache/ .ruff_cache/ .specify/ uv.lock
```

**Step 5: Commit**

```bash
git add -A
git commit -m "chore: remove Python CLI, tests, and packaging"
```

---

### Task 9: Update .gitignore and repository metadata

**Files:**
- Modify: `.gitignore`
- Create: `README.md` (rewrite)
- Modify: `CLAUDE.md` (rewrite)
- Keep: `LICENSE`

**Step 1: Rewrite .gitignore**

Replace `.gitignore` with marketplace-appropriate content:

```gitignore
# editors
.idea/
.vscode/

# OS
.DS_Store
Thumbs.db

# node (for web-browser plugin)
node_modules/
```

**Step 2: Rewrite README.md**

Replace `README.md` with marketplace documentation:

```markdown
# claude-plugins

Personal collection of Claude Code plugins for development workflows, task automation, and specialized tools.

## Installation

Add this marketplace to Claude Code:

```
/plugin marketplace add aalvarez/claude-plugins
```

Then install individual plugins:

```
/plugin install commit-commands@claude-plugins
/plugin install justfile-expert@claude-plugins
/plugin install tmux-tools@claude-plugins
/plugin install sudolang-prompter@claude-plugins
/plugin install web-browser@claude-plugins
/plugin install agent-commands@claude-plugins
```

## Available Plugins

| Plugin | Type | Description |
|--------|------|-------------|
| **commit-commands** | Commands | Smart commit, code review, and test generation |
| **justfile-expert** | Skill | Expert guidance for Just task runner and justfiles |
| **tmux-tools** | Skill | Remote control tmux sessions for interactive CLIs |
| **sudolang-prompter** | Skill | Create efficient LLM prompts using SudoLang syntax |
| **web-browser** | Skill | Browse and interact with web pages via Chrome DevTools Protocol |
| **agent-commands** | Commands | Session handoff, pickup, release, and changelog workflows |

## Plugin Details

### commit-commands

Three slash commands for git workflows:
- `/commit` - Create well-formatted conventional commits with emoji
- `/code-review` - Comprehensive code quality, security, and architecture review
- `/generate-tests` - Generate test suites with unit, integration, and edge case coverage

### justfile-expert

Expertise in the Just task runner: recipe syntax, attributes, groups, modules, cross-platform patterns, and troubleshooting.

### tmux-tools

Remote control tmux sessions for interactive CLIs (python, gdb, etc.) by sending keystrokes and scraping pane output.

### sudolang-prompter

Build structured LLM prompts using SudoLang pseudolanguage — constraints, state management, pipes, and commands.

### web-browser

Browse the web via Chrome DevTools Protocol: navigate, evaluate JS, take screenshots, and pick elements.

### agent-commands

Session management and release workflows:
- `/handoff` - Create a detailed handoff plan for continuing work in a new session
- `/pickup` - Resume work from a previous handoff
- `/make-release` - Create a versioned release
- `/update-changelog` - Update CHANGELOG.md with recent changes

## License

See [LICENSE](LICENSE) for details.
```

**Step 3: Rewrite CLAUDE.md**

Replace `CLAUDE.md` with marketplace-appropriate instructions:

```markdown
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
```

**Step 4: Commit**

```bash
git add .gitignore README.md CLAUDE.md
git commit -m "docs: rewrite repo metadata for marketplace format"
```

---

### Task 10: Validate marketplace structure

**Step 1: Verify directory structure matches expected layout**

```bash
find . -type f -not -path './.git/*' | sort
```

Expected output should show only:
- `.claude-plugin/marketplace.json`
- `plugins/*/` with their contents
- `README.md`, `CLAUDE.md`, `LICENSE`, `.gitignore`
- `docs/plans/*.md`

**Step 2: Validate JSON files parse correctly**

```bash
python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))"
for d in plugins/*; do python3 -c "import json; json.load(open('$d/.claude-plugin/plugin.json'))"; done
```

**Step 3: Verify all skill directories have SKILL.md**

```bash
for d in plugins/*/skills/*/; do
  [ -f "$d/SKILL.md" ] && echo "OK: $d" || echo "MISSING: $d"
done
```

**Step 4: Verify all command files have frontmatter**

```bash
for f in plugins/*/commands/*.md; do
  head -1 "$f" | grep -q "^---" && echo "OK: $f" || echo "MISSING FRONTMATTER: $f"
done
```

**Step 5: Test with Claude Code plugin validator (if available)**

```bash
claude plugin validate . 2>/dev/null || echo "Validator not available, manual checks passed"
```

**Step 6: Commit any fixes if needed**
