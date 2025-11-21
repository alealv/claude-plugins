# Just command runner for claude-tools
# https://just.systems - A command runner with simple syntax
# Configured for UV package manager: https://docs.astral.sh/uv/

set shell := ["bash", "-c"]
set dotenv-load := true

# Show common recipes and usage tips
default:
    @echo "claude-tools - Interactive installer for Claude configurations"
    @echo ""
    @echo "📚 Common Commands:"
    @echo "  just setup          Install dependencies"
    @echo "  just dev            Run interactive installer"
    @echo "  just test           Run all tests"
    @echo "  just fmt            Format code"
    @echo "  just quality        All code quality checks"
    @echo "  just ci             Full CI pipeline (clean, setup, check)"
    @echo ""
    @echo "📖 All available recipes:"
    @echo "  just --list         Show all recipes (grouped by category)"
    @echo "  just --show RECIPE  Show recipe contents"
    @echo ""
    @echo "🚀 Guided Help:"
    @echo "  just help           Show available workflows"
    @echo "  just help setup     Setup workflow guide"
    @echo "  just help dev       Development workflow guide"
    @echo "  just help test      Testing workflow guide"
    @echo "  just help release   Release workflow guide"

# ============================================================================
# SETUP & INSTALL
# ============================================================================

# Install project with all dependency groups
@setup:
    uv sync --all-groups

# Clean reinstall (removes uv.lock)
@reinstall:
    rm -f uv.lock
    uv sync --all-groups

# Install pre-commit hooks
@install-hooks:
    uv run pre-commit install

# ============================================================================
# DEV & RUN
# ============================================================================

# Run installer with PROJECT_PATH argument
@run PROJECT_PATH:
    uv run python -m claude_tools {{ PROJECT_PATH }}

# Run installer (interactive - prompts for path)
@dev:
    uv run python -m claude_tools

# Interactive Python REPL
@repl:
    uv run python

# ============================================================================
# CODE QUALITY
# ============================================================================

# Format code (Ruff)
@fmt:
    uv run ruff format src tests

# Check formatting only
@check-fmt:
    uv run ruff format --check src tests

# Lint code (Ruff)
@lint:
    uv run ruff check --fix src tests

# Check linting only
@check-lint:
    uv run ruff check src tests

# Type check code (Mypy)
@types:
    uv run mypy src

# Run all quality checks
@quality: check-fmt check-lint types

# ============================================================================
# TESTING
# ============================================================================

# Run all tests
@test:
    uv run pytest -v

# Run tests with coverage report
@test-cov:
    uv run pytest --cov=src/claude_tools --cov-report=html --cov-report=term

# Run specific test file
@test-file FILE:
    uv run pytest -v {{ FILE }}

# Run tests matching pattern
@test-pattern PATTERN:
    uv run pytest -v -k "{{ PATTERN }}"

# Run tests in parallel (faster)
@test-parallel:
    uv run pytest -v -n auto

# Watch mode (auto-run on file changes)
@test-watch:
    uv run pytest-watch -- -v

# ============================================================================
# DOCS
# ============================================================================

# Build documentation
@docs-build:
    uv run mkdocs build

# Serve docs locally (http://localhost:8000)
@docs-serve:
    uv run mkdocs serve

# Check docs with strict mode
@docs-check:
    uv run mkdocs build --strict

# Deploy docs to GitHub Pages
@docs-deploy:
    uv run mkdocs gh-deploy

# ============================================================================
# BUILD & PUBLISH
# ============================================================================

# Build distribution packages
@build:
    uv run python -m build

# Build wheel only
@build-wheel:
    uv run python -m build --wheel

# Build sdist only
@build-sdist:
    uv run python -m build --sdist

# Upload to TestPyPI (dry run)
@publish-test:
    uv run python -m twine upload --repository testpypi dist/*

# Upload to PyPI (production)
@publish:
    uv run python -m twine upload dist/*

# ============================================================================
# MAINTENANCE
# ============================================================================

# Clean all generated files and caches
@clean:
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name .pytest_cache .mypy_cache .ruff_cache -delete 2>/dev/null || true
    find . -type f -name .coverage -delete 2>/dev/null || true
    rm -rf build dist *.egg-info htmlcov site .coverage*

# Update all dependencies
@update:
    uv sync --upgrade

# Check for outdated dependencies
@check-deps:
    uv pip list --outdated

# Show current version
@version:
    @uv run python -c "from claude_tools import __version__; print(__version__)"

# ============================================================================
# GIT & CI
# ============================================================================

# Run all pre-commit hooks
@pre-commit:
    uv run pre-commit run --all-files

# Run pre-commit on staged files
@pre-commit-staged:
    uv run pre-commit run

# Run quality checks + tests
@check: quality test

# Full CI pipeline
@ci: clean setup check

# Generate changelog
@changelog:
    uv run git-changelog --config-file .gitchangelog.cfg CHANGELOG.md

# ============================================================================
# INFO & DEBUG
# ============================================================================

# Show project information
@info:
    echo "Project: claude-tools"
    echo "Root: {{ justfile_directory() }}"
    uv python --version
    uv --version

# Show available Python versions
@python-versions:
    uv python list

# List installed packages
@packages:
    uv pip list

# Show environment details
@env:
    echo "Working directory: $(pwd)"
    echo "Python: $(which python3)"
    python3 --version
    uv --version
    uv pip list

# Count lines of code
@loc:
    find src tests -name "*.py" -exec wc -l {} + 2>/dev/null | tail -1 || echo "No Python files found"

# Show git status
@status:
    git status

# Show recent commits
@recent LIMIT="10":
    git log --oneline -{{ LIMIT }}

# ============================================================================
# HELP & DOCUMENTATION
# ============================================================================

# Show help for a workflow (setup, dev, test, release)
@help WORKFLOW="":
    #!/bin/bash
    case "{{ WORKFLOW }}" in
      setup)
        echo "🏗️ SETUP WORKFLOW"
        echo ""
        echo "First time setup:"
        echo "  1. just setup           Install project with all dependencies"
        echo "  2. just install-hooks   Setup git pre-commit hooks"
        echo "  3. just ci              Run full CI to verify setup"
        echo ""
        echo "Troubleshooting:"
        echo "  just clean              Remove all generated files"
        echo "  just reinstall          Clean reinstall (removes lock file)"
        echo "  just info               Show project information"
        ;;
      dev)
        echo "👨‍💻 DEVELOPMENT WORKFLOW"
        echo ""
        echo "Running the installer:"
        echo "  just dev                Run installer (interactive, prompts for path)"
        echo "  just run PATH           Run installer with specific project path"
        echo "  just repl               Start Python REPL for exploration"
        echo ""
        echo "Code changes:"
        echo "  just fmt                Format code automatically"
        echo "  just lint               Lint and fix issues"
        echo "  just types              Run type checker"
        echo "  just quality            All code quality checks at once"
        echo ""
        echo "Before committing:"
        echo "  just check              Quality checks + tests"
        echo "  just pre-commit         Run pre-commit hooks"
        ;;
      test)
        echo "🧪 TESTING WORKFLOW"
        echo ""
        echo "Running tests:"
        echo "  just test               Run all tests"
        echo "  just test-cov           Tests with coverage report"
        echo "  just test-file FILE     Run specific test file"
        echo "  just test-pattern STR   Run tests matching pattern"
        echo "  just test-parallel      Run tests in parallel (faster)"
        echo "  just test-watch         Watch mode (auto-run on file changes)"
        echo ""
        echo "Coverage:"
        echo "  just test-cov           Generate coverage report"
        echo "                          Open: htmlcov/index.html"
        ;;
      release)
        echo "🚀 RELEASE WORKFLOW"
        echo ""
        echo "Preparation:"
        echo "  just ci                 Full CI pipeline (all checks + tests)"
        echo "  just check-deps         Check for outdated dependencies"
        echo "  just update             Update all dependencies"
        echo ""
        echo "Building:"
        echo "  just clean              Clean all generated files"
        echo "  just build              Build wheel and sdist"
        echo "  just build-wheel        Build wheel only"
        echo "  just build-sdist        Build source distribution only"
        echo ""
        echo "Publishing:"
        echo "  just publish-test       Upload to TestPyPI (verify first)"
        echo "  just publish            Upload to PyPI (production)"
        echo ""
        echo "Documentation:"
        echo "  just docs-build         Build docs locally"
        echo "  just docs-check         Check docs with strict mode"
        echo "  just docs-deploy        Deploy docs to GitHub Pages"
        ;;
      *)
        echo "Available workflows:"
        echo "  just help setup         Setup workflow - getting started"
        echo "  just help dev           Development workflow"
        echo "  just help test          Testing workflow"
        echo "  just help release       Release workflow"
        ;;
    esac
