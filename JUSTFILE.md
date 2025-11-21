# Justfile Reference

Complete reference for all recipes in this project's `justfile`.

## Overview

The justfile organizes recipes into logical sections:

1. **Setup & Install** - Project initialization
2. **Dev & Run** - Development and execution
3. **Code Quality** - Formatting, linting, typing
4. **Testing** - Test execution and coverage
5. **Docs** - Documentation building
6. **Build & Publish** - Package distribution
7. **Maintenance** - Cleanup, updates, versioning
8. **Git & CI** - Git hooks and CI pipeline
9. **Info & Debug** - Project information
10. **Aliases** - Quick shortcuts

## Quick Reference

```bash
just              # List all recipes
just RECIPE       # Run a recipe
just RECIPE ARG   # Run recipe with argument
```

## Recipes by Section

### Setup & Install

```bash
just setup              # Install project with all dependency groups
just reinstall          # Clean reinstall (removes uv.lock)
just install-hooks      # Install pre-commit hooks
```

### Dev & Run

```bash
just run PROJECT_PATH   # Run installer with PROJECT_PATH argument
just dev                # Run installer (interactive - prompts for path)
just repl               # Interactive Python REPL
```

### Code Quality

```bash
just fmt                # Format code (Ruff)
just check-fmt          # Check formatting only
just lint               # Lint code (Ruff)
just check-lint         # Check linting only
just types              # Type check code (Mypy)
just quality            # Run all quality checks (fmt, lint, types)
```

### Testing

```bash
just test               # Run all tests
just test-cov           # Run tests with coverage report
just test-file FILE     # Run specific test file
just test-pattern PATTERN # Run tests matching pattern
just test-parallel      # Run tests in parallel (faster)
just test-watch         # Watch mode (auto-run on file changes)
```

### Docs

```bash
just docs-build         # Build documentation (MkDocs)
just docs-serve         # Serve docs locally (http://localhost:8000)
just docs-check         # Check docs with strict mode
just docs-deploy        # Deploy docs to GitHub Pages
```

### Build & Publish

```bash
just build              # Build distribution packages
just build-wheel        # Build wheel only
just build-sdist        # Build sdist only
just publish-test       # Upload to TestPyPI (dry run)
just publish            # Upload to PyPI (production)
```

### Maintenance

```bash
just clean              # Clean all generated files and caches
just update             # Update all dependencies
just check-deps         # Check for outdated dependencies
just version            # Show current version
```

### Git & CI

```bash
just pre-commit         # Run all pre-commit hooks
just pre-commit-staged  # Run pre-commit on staged files
just check              # Run quality checks + tests
just ci                 # Full CI pipeline (clean, setup, check)
just changelog          # Generate changelog
```

### Info & Debug

```bash
just info               # Show project information
just python-versions    # Show available Python versions
just packages           # List installed packages
just env                # Show environment details
just loc                # Count lines of code
just status             # Show git status
just recent LIMIT       # Show recent N commits (default: 10)
```

## Aliases

Short aliases for frequently used recipes:

| Alias | Recipe |
|-------|--------|
| `just f` | `just fmt` |
| `just l` | `just lint` |
| `just t` | `just test` |
| `just ck` | `just check` |
| `just b` | `just build` |
| `just d` | `just docs-build` |
| `just e` | `just env` |

## Common Workflows

### New Developer Setup

```bash
just setup              # Install everything
just install-hooks      # Setup git hooks
just ci                 # Run full CI to verify
```

### Daily Development

```bash
just fmt                # Format code
just lint               # Lint code
just test               # Run tests
just check              # All checks + tests
```

### Before Committing

```bash
just fmt                # Auto-format
just check              # Run all checks
git add .
git commit -m "..."
```

### Code Review

```bash
just quality            # All code quality checks
just test               # Run tests
```

### Preparing a Release

```bash
just clean              # Clean everything
just ci                 # Full CI pipeline
just build              # Build packages
just publish-test       # Test upload
just publish            # Real upload
```

### Debugging

```bash
just info               # Show project info
just env                # Show environment
just loc                # Count lines of code
just status             # Git status
just recent 20          # Last 20 commits
```

## Advanced Usage

### Dry Run

See what would be executed without running it:

```bash
just --dry-run test
just --dry-run ci
```

### Show Recipe

Display the actual commands for a recipe:

```bash
just --show test
just --show fmt
```

### List Only

Display all recipes without running the default:

```bash
just --list
just --list --unsorted
```

### Check Justfile

Verify justfile syntax:

```bash
just --check
```

### Using Arguments

Some recipes accept arguments:

```bash
just run ~/my-project
just test-file tests/test_installer.py
just test-pattern "keyboard"
just recent 20
```

## Environment Variables

You can set environment variables in a `.env` file:

```bash
# .env
export PYTEST_ADDOPTS="-v"
export PYTHONPATH="."
```

Just will automatically load `.env` at startup.

## UV Integration

All recipes use UV for Python package management:

- `uv sync --all-groups` - Install dependencies
- `uv run COMMAND` - Run commands in UV environment
- `uv pip list` - List installed packages
- `uv python --version` - Check Python version

This ensures:
- Consistent environment across developers
- Lock file reproducibility
- All dependency groups installed
- Proper virtual environment

## Tips & Tricks

1. **List recipes in source order**:
   ```bash
   just --list --unsorted
   ```

2. **Run multiple recipes**:
   ```bash
   just fmt lint test
   ```

3. **Use variables in recipes**:
   ```bash
   # In justfile
   @my-recipe FILE="default.txt":
       echo {{ FILE }}

   # Usage
   just my-recipe
   just my-recipe custom.txt
   ```

4. **Create recipe dependencies**:
   ```bash
   # In justfile
   @build-docs: clean docs-build

   # Just runs: clean, then docs-build
   ```

5. **Shell expansion**:
   ```bash
   # Use backticks for command substitution
   @version:
       @echo "Version: $(uv run python -c 'from claude_tools import __version__; print(__version__)')"
   ```

## Troubleshooting

### Just not found

Install Just:

```bash
brew install just       # macOS
cargo install just      # Other platforms
```

Or download from: https://github.com/casey/just/releases

### UV not found

Install UV:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Recipe fails

Run with verbose output:

```bash
just --verbose recipe-name
```

Or see what would be executed:

```bash
just --show recipe-name
```

### Permission denied

Make sure the justfile is readable:

```bash
chmod 644 justfile
```

### .env not loading

Ensure `.env` exists and has proper format:

```bash
# .env
VAR_NAME=value
```

Just loads `.env` by default. To disable:

```bash
set dotenv-load := false
```

## Best Practices

1. **Use `@` prefix** to suppress recipe name output
2. **Group related recipes** in sections
3. **Keep recipes simple** - complex logic goes in scripts
4. **Document recipes** with comments
5. **Use recipe dependencies** instead of complex logic
6. **Provide aliases** for frequently used recipes
7. **Use meaningful names** (e.g., `test-cov` not `tc`)

## References

- [Just Official Manual](https://just.systems/man/en/)
- [UV Documentation](https://docs.astral.sh/uv/)
- [Project README](./README.md)
- [QUICK_START.md](./QUICK_START.md) - Quick reference
- [JUSTFILE_MIGRATION.md](./JUSTFILE_MIGRATION.md) - Migration guide
