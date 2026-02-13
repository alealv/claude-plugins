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
