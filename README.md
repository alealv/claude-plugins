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
/plugin install agent-commands@claude-plugins
/plugin install zellij-tools@claude-plugins
```

## Available Plugins

| Plugin | Type | Description |
|--------|------|-------------|
| **justfile-expert** | Skill | Expert guidance for Just task runner and justfiles |
| **agent-commands** | Commands | Session handoff, pickup, release, and changelog workflows |
| **zellij-tools** | Skill | Remote control Zellij terminal multiplexer sessions for interactive CLIs |

## Plugin Details

### justfile-expert

Expertise in the Just task runner: recipe syntax, attributes, groups, modules, cross-platform patterns, and troubleshooting. Includes a comprehensive reference document for advanced features.

### agent-commands

Session management and release workflows:
- `/handoff` - Create a detailed handoff plan for continuing work in a new session
- `/pickup` - Resume work from a previous handoff
- `/make-release` - Create a versioned release (auto-detects version from package.json, Cargo.toml, pyproject.toml, etc.)
- `/update-changelog` - Update CHANGELOG.md with recent changes

### zellij-tools

Remote control Zellij terminal multiplexer sessions for interactive CLIs, parallel workflows, and long-running processes. Includes helper scripts for waiting on output patterns and finding sessions.

## License

See [LICENSE](LICENSE) for details.
