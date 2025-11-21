# Claude Code Hooks

This directory contains event-based automation hooks for Claude Code.

## Available Hooks

### auto-commit

**Automatically commits changes after task completion with intelligent grouping**

**Features:**
- ✅ Automatic commits when Claude finishes tasks
- ✅ Conventional commit format (feat, fix, docs, etc.)
- ✅ Intelligent amending for related changes
- ✅ Prevents amending pushed commits
- ✅ Time-based and file-overlap analysis

**Use cases:**
- Automatic version control without manual commits
- Maintain clean, logical commit history
- Group related changes into single commits
- Separate unrelated changes into different commits

[→ View auto-commit documentation](auto-commit/README.md)

## Installing Hooks

### Option 1: Interactive Installer

```bash
./install.sh /path/to/your/project
# Navigate to Hooks tab and select hooks to install
```

### Option 2: Manual Installation

1. Copy the hook directory to your project:
```bash
cp -r hooks/auto-commit .claude/hooks/
```

2. Add the hook configuration to `.claude/settings.json`:
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "true",
        "handler": {
          "type": "command",
          "command": "bash .claude/hooks/auto-commit/auto-commit.sh"
        }
      }
    ]
  }
}
```

## Hook Events

Claude Code supports these hook events:

| Event | When It Runs | Use Case |
|-------|--------------|----------|
| **PreToolUse** | Before tool execution | Validate/modify tool parameters |
| **PostToolUse** | After successful tool use | Auto-format, commit, notify |
| **UserPromptSubmit** | When user submits input | Enrich prompts, validate input |
| **Stop** | When Claude finishes working | Auto-commit, cleanup, summary |
| **SubagentStop** | When subagent finishes | Subagent-specific actions |
| **SessionStart** | At conversation start | Setup, initialization |
| **SessionEnd** | At conversation end | Cleanup, reporting |
| **Notification** | On system notifications | Custom alerts |
| **PermissionRequest** | On permission dialogs | Auto-approve/deny |

## Hook Types

### Command Hooks

Execute bash scripts for deterministic operations:

```json
{
  "matcher": "tool == 'FileWrite'",
  "handler": {
    "type": "command",
    "command": "bash .claude/hooks/check-syntax.sh"
  }
}
```

### Prompt Hooks

Query the LLM for context-aware decisions (Stop/SubagentStop only):

```json
{
  "matcher": "true",
  "handler": {
    "type": "prompt",
    "prompt": "Should Claude continue working or is the task complete?"
  }
}
```

## Exit Codes

Hooks communicate via exit codes:

- **0**: Success, continue normally
- **2**: Blocking error (stderr becomes feedback to Claude)
- **Other**: Non-blocking error (logged in verbose mode)

## Best Practices

1. **Keep hooks fast** - Slow hooks delay Claude's workflow
2. **Handle errors gracefully** - Use appropriate exit codes
3. **Test thoroughly** - Verify hooks work in all scenarios
4. **Document behavior** - Include README for each hook
5. **Use matchers wisely** - Only run when needed
6. **Avoid side effects** - Hooks should be idempotent when possible

## Creating Custom Hooks

1. Create a new directory in `hooks/`:
```bash
mkdir hooks/my-hook
```

2. Create the hook script:
```bash
touch hooks/my-hook/my-hook.sh
chmod +x hooks/my-hook/my-hook.sh
```

3. Add hook logic:
```bash
#!/usr/bin/env bash
# Your hook implementation
exit 0  # Success
```

4. Create settings.json:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "tool == 'Write'",
        "handler": {
          "type": "command",
          "command": "bash .claude/hooks/my-hook/my-hook.sh"
        }
      }
    ]
  }
}
```

5. Document it:
```bash
touch hooks/my-hook/README.md
```

## Matcher Expressions

Matchers use JavaScript-like expressions:

```javascript
// Always run
"true"

// Match specific tool
"tool == 'FileWrite'"

// Match multiple tools
"tool == 'FileWrite' || tool == 'FileEdit'"

// Match file patterns
"args.file_path && args.file_path.endsWith('.py')"

// Complex conditions
"tool == 'Bash' && args.command.includes('git')"
```

## Debugging Hooks

### Enable Verbose Mode

Run Claude Code with verbose flag:
```bash
claude --verbose
```

### Check Hook Output

Hooks write to stderr for debugging:
```bash
echo "Debug: Processing file $FILE" >&2
```

### Test Independently

Run hooks manually:
```bash
bash .claude/hooks/auto-commit/auto-commit.sh
echo $?  # Check exit code
```

## Security Considerations

1. **Review hook code** - Understand what each hook does
2. **Limit permissions** - Use restrictive matchers
3. **Avoid secrets** - Don't hardcode credentials
4. **Validate inputs** - Check parameters before use
5. **Use allowlists** - Prefer allow over deny patterns

## Resources

- [Claude Code Hooks Documentation](https://code.claude.com/docs/en/hooks)
- [Hook Examples](https://github.com/anthropics/claude-code/tree/main/examples/hooks)
- [Settings Reference](https://code.claude.com/docs/en/settings)

## Contributing

To add a new hook to this repository:

1. Create the hook directory with all files
2. Include comprehensive README
3. Add examples of usage
4. Test in real projects
5. Document any dependencies
6. Update this README

## License

MIT License - Same as parent repository
