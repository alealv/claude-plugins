# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`claude-tools` is a Python CLI installer for Claude Code configurations. It provides an interactive terminal UI for discovering and installing commands, skills, agents, and hooks into Claude Code projects.

## Development Commands

### Setup and Installation
```bash
just setup              # Install all dependencies
just install-hooks      # Install pre-commit hooks
```

### Testing
```bash
just test              # Run all tests
just test-cov          # Run tests with coverage (opens htmlcov/index.html)
just test-file FILE    # Run specific test file
just test-pattern STR  # Run tests matching pattern
uv run pytest tests/test_installer.py::test_function_name  # Run single test
```

### Code Quality
```bash
just fmt              # Format code with Ruff
just lint             # Lint and auto-fix with Ruff
just types            # Type check with ty
just quality          # Run all quality checks (format + lint + types)
just check            # Quality checks + tests
```

### Building and Publishing
```bash
just clean            # Remove generated files and caches
just build            # Build wheel and sdist
just build wheel      # Build wheel only
just publish test     # Upload to TestPyPI
just publish          # Upload to PyPI
```

### Documentation
```bash
just docs             # Build docs
just docs serve       # Serve docs locally at http://localhost:8000
just docs deploy      # Deploy to GitHub Pages
```

## Architecture

### Module Structure

**Entry Points:**
- `src/claude_tools/__init__.py` - Package entry with `main()` function
- `src/claude_tools/__main__.py` - Enables `python -m claude_tools`
- CLI command: `claude-tools` (defined in pyproject.toml)

**Core Modules:**
- `cli.py` - Command-line interface, terminal setup, keyboard input handling
- `installer.py` - Core installation logic, file copying, settings merging
- `ui.py` - Interactive terminal UI with Rich library
- `debug.py` - Debug utilities and version information

### Key Data Flow

1. **CLI Parsing** → Validate project path
2. **Item Discovery** → Scan repo for commands/skills/agents/hooks
3. **Interactive UI** → User selects items via keyboard navigation
4. **Installation** → Copy selected items to `.claude/` directory
5. **Hook Merging** → Merge hook settings into `.claude/settings.json`

### Configuration Type Handling

**Commands & Agents** (`.md` files):
- Discovered as individual markdown files in `commands/` or `agents/`
- Installed as: `.claude/commands/name.md` or `.claude/agents/name.md`

**Skills** (directories):
- Discovered as directories containing `SKILL.md`
- Installed as: `.claude/skills/skill-name/` (entire directory copied)

**Hooks** (directories with special handling):
- Discovered as directories in `hooks/`
- Installed to: `.claude/hooks/hook-name/`
- **Critical**: Also merges `settings.json` from hook into `.claude/settings.json`
- Merge strategy: Per-event merging, preserves existing handlers

## UI Navigation System

The installer uses a three-level focus system:

**Focus States:**
1. `Focus.LIST` - Navigate items in current tab
2. `Focus.CANCEL` - Cancel button
3. `Focus.OK` - OK button

**Key Bindings:**
- `Tab` - Cycle focus: LIST → CANCEL → OK → LIST
- `←` `→` or `h` `l` - When in LIST: switch tabs; When on buttons: navigate between Cancel/OK
- `↑` `↓` or `k` `j` - Navigate items in list
- `Space` or `x` - Toggle selection
- `Enter` - Confirm current focus (only works on OK button to proceed)
- `Esc` or `q` - Cancel and exit

**Important**: The Tab key cycles through focus states, NOT tabs. Use arrow keys to switch between COMMANDS/SKILLS/AGENTS/HOOKS tabs.

## Testing Architecture

Tests use pytest with the following structure:
- `tests/test_installer.py` - Installer logic tests
- `tests/test_ui.py` - UI state and rendering tests
- `tests/test_cli.py` - CLI argument parsing tests
- `tests/conftest.py` - Shared fixtures

Run individual tests:
```bash
uv run pytest tests/test_installer.py::TestInstaller::test_method_name -v
```

## Settings Merge Logic

Hook installation involves special settings merge logic in `Installer.merge_hook_settings()`:

1. Each hook directory may contain `settings.json`
2. Settings define hook handlers for events (Stop, PreToolUse, etc.)
3. During installation, hook settings are merged into `.claude/settings.json`
4. Merge preserves existing hooks while adding new ones
5. Per-event arrays are combined (no duplicates based on command path)

## Package Management

This project uses **uv** (not pip) for dependency management:
- `pyproject.toml` - Project metadata and dependencies
- `uv.lock` - Locked dependency versions (not committed in .gitignore but generated)
- Always use `uv run` prefix for Python commands: `uv run pytest`, `uv run python`

## Common Patterns

**Running the installer locally during development:**
```bash
uv run python -m claude_tools /path/to/test/project
```

**Testing UI changes:**
The UI uses Rich library with console rendering. Test with actual terminal:
```bash
uv run python -m claude_tools .
```

**Adding a new configuration type:**
1. Add to `ConfigType` enum in `installer.py`
2. Implement discovery logic in `Installer.get_available_items()`
3. Add to `InstallUI.TABS` list in `ui.py`
4. Handle special installation logic in `cli.py` if needed (like hook merging)

## Commit Workflow

**Important**: Always commit meaningful changes. This repository includes an auto-commit agent for intelligent commit message generation.

### Using the Auto-Commit Agent

The `agents/auto-commit.md` agent analyzes changes and creates conventional commit messages:

```bash
# Agent is available at: agents/auto-commit.md
# Model: Haiku (for efficiency)
# Tools: Bash, Read, Grep
```

**Agent Workflow:**
1. Analyzes `git status` and `git diff` to understand changes
2. Determines conventional commit type (feat, fix, refactor, docs, test, etc.)
3. Identifies scope from affected components/directories
4. Generates specific, descriptive commit message
5. Stages and commits changes

**Conventional Commit Types:**
- `feat` - New feature or functionality
- `fix` - Bug fix or correction
- `refactor` - Code restructuring without behavior change
- `docs` - Documentation changes
- `test` - Adding or modifying tests
- `build` - Build system or dependency changes
- `chore` - Maintenance tasks, cleanup
- `perf` - Performance improvements
- `style` - Code style/formatting (no logic change)

**Message Format:**
```
<type>(<scope>): <description>

[optional body]
```

**Examples:**
```bash
feat(ui): change Tab key to cycle focus instead of tabs
fix(installer): handle missing settings.json gracefully
docs(CLAUDE.md): add commit workflow guidelines
refactor(cli): simplify keyboard input handling
test(ui): add focus navigation tests
```

**Key Guidelines:**
- Use imperative mood: "add feature" not "added feature"
- Be specific: "add JWT token refresh" not "add new functionality"
- Keep description under 50 characters
- Use lowercase for descriptions
- Scope should reflect primary affected component (ui, installer, cli, docs, etc.)

### When to Commit

Commit after:
- Completing a logical unit of work
- Fixing a bug
- Adding a feature or functionality
- Refactoring code
- Updating documentation
- Making meaningful changes to tests

Do not commit:
- Work-in-progress half-implemented features (unless explicitly requested)
- Multiple unrelated changes together (ask user if separate commits are needed)

## Version Management

Version is dynamically determined via `scripts/get_version.py` using git tags and commit info. Do not manually edit version numbers.
