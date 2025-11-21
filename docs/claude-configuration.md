# Claude Configuration Repository

This is a meta repository to host all the commands, hooks, skills, and agents for Claude Code.

## Purpose

This repository serves as a centralized location for:
- **Commands**: Custom slash commands for Claude Code
- **Hooks**: Event-based automation scripts
- **Skills**: Specialized capabilities and domain knowledge
- **Agents**: Autonomous task handlers

## Repository Structure

This is a **meta-repository** that hosts reusable configurations. The structure mirrors Claude Code's organization but at the root level for easy sharing across projects:

```
claude/
├── commands/                     # Custom slash commands
│   ├── command-name.md
│   └── ...
├── skills/                       # Reusable skills
│   ├── skill-name/
│   │   ├── SKILL.md
│   │   └── ...
│   └── ...
├── agents/                       # Agent definitions
│   └── ...
├── hooks/                        # Hook scripts and examples
│   └── ...
├── README.md                     # Main documentation
└── .gitignore
```

## Installation

Use the interactive installer to add commands, skills, agents, or hooks to your projects:

```bash
# Install claude-tools first
pip install claude-tools

# Run the installer
claude-tools /path/to/your/project
```

Or run without arguments to be prompted:

```bash
claude-tools
```

### Installer Features

- **Tab Navigation**: Press `Tab` to cycle through commands, skills, agents, and hooks
- **Item Selection**: Use `↑`/`↓` arrows to navigate, `Space` to select/deselect items
- **Confirmation**: Navigate to buttons with arrows, press `Enter` on OK to install
- **Cancellation**: Press `Esc`, `q`, or select Cancel button to exit
- **Hook Integration**: Automatically merges hook settings into `.claude/settings.json`

The installer will copy selected items into your project's `.claude/` directory.

## Component Details

### Commands (.claude/commands/)
- **Format**: Markdown files with YAML frontmatter
- **Naming**: lowercase-with-hyphens.md
- **Invocation**: `/command-name` in Claude Code
- **Arguments**: Use `$ARGUMENTS` or `$1`, `$2` for specific parameters

### Skills (.claude/skills/skill-name/)
- **Format**: Directory with required `SKILL.md` file
- **Naming**: lowercase-with-hyphens (max 64 chars)
- **Auto-discovery**: Claude autonomously uses skills when relevant
- **Scope**: Keep each skill focused on one capability
- **Documentation**: Include SKILL.md, README.md, and supporting files

### Hooks (.claude/hooks/)
- **Configuration**: Defined in JSON settings files
- **Format**: Directory with bash scripts and settings.json
- **Types**: PreToolUse, PostToolUse, UserPromptSubmit, Stop, SessionStart, etc.
- **Handlers**: Command (bash scripts) or Prompt (LLM-based)

### Agents (.claude/agents/)
- **Structure**: Directory-based with system prompts and tool configurations
- **Usage**: Defined via CLI arguments or plugin configurations

## Settings Hierarchy

Settings apply in this precedence order (highest to lowest):
1. Enterprise managed policies
2. Command line arguments
3. Local project settings (`.claude/settings.local.json`)
4. Shared project settings (`.claude/settings.json`)
5. User settings (`~/.claude/settings.json`)

## Best Practices

1. **Version Control**: Commit `.claude/settings.json` and shared configurations to git
2. **Local Overrides**: Use `.claude/settings.local.json` for personal preferences (git-ignored)
3. **Naming Conventions**: Use lowercase with hyphens for all commands and skills
4. **Documentation**: Include clear descriptions in frontmatter for discoverability
5. **Focused Skills**: Each skill should have one primary capability
6. **Team Sharing**: Project skills and commands are automatically available to team members

## Resources

- [Slash Commands](https://code.claude.com/docs/en/slash-commands)
- [Hooks](https://code.claude.com/docs/en/hooks)
- [Skills](https://code.claude.com/docs/en/skills)
- [Plugins](https://code.claude.com/docs/en/plugins)
- [Settings](https://code.claude.com/docs/en/settings)
