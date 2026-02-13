# Migrate claude-tools to claude-plugins Marketplace

## Context

Claude Code now has a native plugin system with decentralized marketplaces, making the Python CLI installer (`claude-tools`) obsolete. This design converts the repository into a standard Claude Code plugin marketplace while preserving all existing skill and command content.

## Decision

**Approach**: Multi-plugin marketplace (Approach A)

- Each skill/command group becomes its own installable plugin
- Users install via native `/plugin marketplace add` + `/plugin install`
- Python CLI, tests, packaging, and CI/CD are removed entirely
- All skill content (SKILL.md, commands, references, tools) preserved as-is

## Target Structure

```
claude-plugins/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── commit-commands/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── commands/
│   │   │   ├── commit.md
│   │   │   ├── code-review.md
│   │   │   └── generate-tests.md
│   │   └── README.md
│   ├── justfile-expert/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── skills/justfile-expert/
│   │   │   ├── SKILL.md
│   │   │   └── references/just-docs.md
│   │   └── README.md
│   ├── tmux-tools/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── skills/tmux/
│   │   │   ├── SKILL.md
│   │   │   └── tools/
│   │   └── README.md
│   ├── sudolang-prompter/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── skills/sudolang-prompter/
│   │   │   ├── SKILL.md
│   │   │   └── references/sudolang-spec.md
│   │   └── README.md
│   ├── web-browser/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── skills/web-browser/
│   │   │   ├── SKILL.md
│   │   │   └── tools/
│   │   └── README.md
│   └── agent-commands/
│       ├── .claude-plugin/plugin.json
│       ├── commands/
│       │   ├── handoff.md
│       │   ├── pickup.md
│       │   ├── make-release.md
│       │   └── update-changelog.md
│       └── README.md
├── README.md
└── LICENSE
```

## Plugin Grouping

| Plugin | Contents | Rationale |
|--------|----------|-----------|
| commit-commands | commit, code-review, generate-tests | Related git/dev workflow commands |
| justfile-expert | justfile skill + references | Independent skill |
| tmux-tools | tmux skill + shell tools | Independent skill |
| sudolang-prompter | sudolang skill + spec reference | Independent skill |
| web-browser | web-browser skill + JS tools | Independent skill |
| agent-commands | handoff, pickup, make-release, update-changelog | Related session/workflow commands |

## What Gets Removed

- `src/claude_tools/` - Python source (cli.py, installer.py, ui.py, debug.py)
- `tests/` - Python test suite
- `pyproject.toml` - Python packaging config
- `config/` - Ruff config
- `scripts/` - Version script
- `justfile` - Build recipes
- `docs/` - MkDocs documentation (except this plan)
- `.github/workflows/` - Python CI/CD
- `uv.lock`, `.python-version`

## What Gets Preserved

All skill and command content moves into plugin structure unchanged:
- SKILL.md files with frontmatter
- Command markdown files with frontmatter
- Reference documents
- Tool scripts (shell, JS)
- Supporting files (package.json, etc.)

## Special Migration: agent-commands-main

Files in `skills/agent-commands-main/common/` and `specific/` are actually commands (they use `$ARGUMENTS`). They become proper `commands/*.md` files with appropriate frontmatter added.

## Usage

```bash
# Add marketplace
/plugin marketplace add aalvarez/claude-plugins

# Install specific plugins
/plugin install commit-commands@claude-plugins
/plugin install justfile-expert@claude-plugins
```

## PyPI Deprecation

Final `claude-tools` PyPI release should:
- Update README to point users to the marketplace
- Mark package as deprecated on PyPI
