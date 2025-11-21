# claude-tools

[![ci](https://github.com/alealv/claude-tools/workflows/ci/badge.svg)](https://github.com/alealv/claude-tools/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://alealv.github.io/claude-tools/)
[![pypi version](https://img.shields.io/pypi/v/claude-tools.svg)](https://pypi.org/project/claude-tools/)
[![gitter](https://img.shields.io/badge/matrix-chat-4DB798.svg?style=flat)](https://app.gitter.im/#/room/#claude-tools:gitter.im)

Installer for common Claude agents, skills, hooks and commands

## Installation

Install with pip:
```bash
pip install claude-tools
```

Or with [`uv`](https://docs.astral.sh/uv/):
```bash
uv tool install claude-tools
```

Or from source:
```bash
git clone https://github.com/alealv/claude-tools.git
cd claude-tools
uv tool install -e .
```

## Quick Start

### Run the installer
```bash
# Interactive mode - select configurations to install
claude-tools /path/to/your/project
```

Or with default path prompting:
```bash
claude-tools
```

### What it does
The installer discovers and installs Claude Code configurations:
- **Commands**: Custom slash commands (e.g., `/commit`, `/review`)
- **Skills**: Autonomous capabilities for Claude
- **Hooks**: Automation scripts (e.g., auto-commit on task completion)
- **Agents**: Task-specific Claude configurations

Select items using arrow keys and space bar, then confirm to install.

## Development

### Setup
```bash
just setup
just install-hooks
```

### Run tests
```bash
just test
just test-cov        # with coverage
```

### Code quality
```bash
just fmt             # format code
just lint            # lint code
just quality         # all checks
```

### Build and publish
```bash
just build
just publish-test    # test PyPI
just publish         # production PyPI
```

See `justfile` for all available commands or run `just` to list recipes.

## Documentation

For detailed documentation, see:
- [`docs/`](./docs/) - Complete documentation
- [`docs/claude-configuration.md`](./docs/claude-configuration.md) - Configuration guide
- [`hooks/auto-commit/README.md`](./hooks/auto-commit/README.md) - Auto-commit hook details
