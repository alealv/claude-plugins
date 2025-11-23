# Auto-Commit Hook for Claude Code

Automatically commits changes after Claude completes a task, with intelligent logic for creating meaningful commits or amending existing ones.

## Features

### 🤖 Automatic Commit Creation

- Automatically commits all changes when Claude finishes a task
- Uses conventional commit format (feat, fix, docs, refactor, etc.)
- Generates meaningful commit messages using LLM analysis or static patterns
- Intelligently groups related changes

### 🔄 Intelligent Commit Grouping

**Creates NEW commits when:**
- Last commit is older than 5 minutes
- Different type of change (e.g., last was `feat`, now is `fix`)
- Working on unrelated files (< 30% overlap)
- Last commit was not by Claude
- Last commit has been pushed to remote

**AMENDS previous commit when:**
- Last commit is recent (< 5 minutes)
- Similar type of change (e.g., both are `refactor`)
- Working on same/related files (> 30% overlap)
- Last commit was by Claude
- Last commit has not been pushed

### 📊 Commit Type Detection

The hook automatically detects the commit type based on:

| Type | Detected When |
|------|---------------|
| `feat` | New functions, classes, or files added |
| `fix` | Bug fixes or corrections |
| `refactor` | Code restructuring without changing behavior |
| `docs` | README, CHANGELOG, or .md files changed |
| `test` | Test files added or modified |
| `build` | Dependencies updated (package.json, pyproject.toml, etc.) |
| `ci` | CI/CD configuration changes |
| `chore` | Other changes (cleanup, file removal, etc.) |

### 🧠 Commit Message Generation with Haiku Agent

The hook uses an autonomous agent powered by **Claude 3.5 Haiku** to generate intelligent commit messages:

**Agent-Based Generation (Preferred)**
- Autonomous agent analyzes code changes and generates meaningful, context-aware commit messages
- Uses **Claude 3.5 Haiku** model for fast, cost-effective analysis (~$0.001 per commit)
- Reasons about code changes to understand intent and impact
- Requires `ANTHROPIC_API_KEY` environment variable
- Requires `anthropic` Python package (`pip install anthropic`)
- Falls back to static analysis if unavailable

**Static Analysis (Fallback)**
- Pattern matching based on file changes and diff content
- No external dependencies required
- Provides basic but accurate commit messages

To enable the Haiku agent:
```bash
export ANTHROPIC_API_KEY="your-api-key"
pip install anthropic
```

## Installation

### Option 1: Using the Installer

```bash
./install.sh /path/to/your/project
# Select the auto-commit hook from the hooks tab
```

### Option 2: Manual Installation

1. Copy the hook to your project:
```bash
mkdir -p .claude/hooks/auto-commit
cp hooks/auto-commit/auto-commit.sh .claude/hooks/auto-commit/
cp hooks/auto-commit/commit-message-agent.py .claude/hooks/auto-commit/
chmod +x .claude/hooks/auto-commit/auto-commit.sh
chmod +x .claude/hooks/auto-commit/commit-message-agent.py
```

2. (Optional) Install Python dependencies for Haiku agent:
```bash
pip install anthropic
export ANTHROPIC_API_KEY="your-api-key"
```

3. Add to your `.claude/settings.json`:
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

## Configuration

You can customize the behavior by editing these variables in `auto-commit.sh`:

```bash
MAX_COMMIT_AGE_SECONDS=300  # Time window for amending (default: 5 minutes)
MIN_FILES_FOR_SPLIT=10      # Threshold for considering commit splits
```

## How It Works

### 1. Change Detection

When Claude finishes a task, the hook:
- Checks if there are uncommitted changes
- Collects git diff and changed files list
- Prepares data for analysis

### 2. Agent-Based Analysis (Haiku)

The commit message agent:
1. **Receives context**: Git diff + changed files
2. **Analyzes changes**: Uses Claude 3.5 Haiku to understand:
   - What functionality was added/changed/removed
   - The intent behind the changes
   - The scope/component affected
3. **Reasons about type**: Determines conventional commit type (feat/fix/docs/etc.)
4. **Generates description**: Creates specific, meaningful description
5. **Returns structured output**: `type|scope|description`

**Agent characteristics:**
- Model: Claude 3.5 Haiku (fast, cost-effective)
- Temperature: 0.2 (consistent, focused)
- Max tokens: 200 (concise responses)
- Fallback: Static pattern matching if agent unavailable

### 3. Static Analysis Fallback

If agent is unavailable, pattern matching is used:
```bash
# Example static logic
if [test files changed]; then type="test"
elif [new features added]; then type="feat"
elif [bugs fixed]; then type="fix"
# ... etc
```

### 4. Amend Decision

The hook decides whether to amend based on:

```
IF last_commit.author == "Claude" AND
   last_commit.age < 5_minutes AND
   (commit_types_similar OR is_refactor) AND
   file_overlap > 30% AND
   NOT pushed_to_remote
THEN
   amend = true
ELSE
   amend = false
```

### 5. Commit Execution

- **New commit**: Creates a new commit with generated message
- **Amend**: Updates the previous commit with new changes

## Examples

### Example 1: Continuous Feature Development

```bash
# User: "Add user authentication"
# Claude adds auth.py, updates routes.py
→ feat(src): add user authentication

# User: "Add password validation to auth"
# Claude updates auth.py (within 5 min, same file)
→ [AMENDED] feat(src): add user authentication
```

### Example 2: Separate Concerns

```bash
# User: "Add user model"
# Claude creates models/user.py
→ feat(models): add new files

# User: "Now write tests for the user model"
# Claude creates tests/test_user.py (different concern)
→ test(tests): add/update tests
```

### Example 3: Refactoring After Feature

```bash
# User: "Implement payment processing"
# Claude adds payment.py
→ feat(src): add new functionality

# User: "Refactor the payment code to be cleaner"
# Claude refactors payment.py (within 5 min)
→ [AMENDED] feat(src): add new functionality
```

## Commit Message Format

All commits follow the conventional commit format:

```
<type>(<scope>): <description>
```

### Examples:

```
feat(auth): add password validation
fix(api): handle null responses correctly
docs(readme): update installation steps
refactor(utils): simplify error handling
test(user): add edge case coverage
build(deps): update dependencies
```

## Safety Features

### Won't Amend If:

1. **Pushed to remote** - Prevents rewriting shared history
2. **Too old** - Commits older than 5 minutes create new commits
3. **Different author** - Won't amend commits not made by Claude
4. **Unrelated changes** - Creates new commit if files don't overlap
5. **Major type change** - Won't amend `feat` with `fix`

### Always Safe:

- Only commits changes made during the current task
- Never forces pushes
- Respects git's safety mechanisms
- Provides clear output about what it's doing

## Customization

### Adjust Time Window

To change how recent commits need to be for amending:

```bash
# In auto-commit.sh
MAX_COMMIT_AGE_SECONDS=600  # 10 minutes instead of 5
```

### Change Overlap Threshold

To adjust how much file overlap is needed for amending:

```bash
# In auto-commit.sh, find this line:
if [ $OVERLAP_PERCENTAGE -gt 30 ]; then

# Change to:
if [ $OVERLAP_PERCENTAGE -gt 50 ]; then  # Require 50% overlap
```

### Disable for Specific Projects

Remove the hook configuration from `.claude/settings.json` or use `.claude/settings.local.json`:

```json
{
  "hooks": {
    "Stop": []
  }
}
```

## Troubleshooting

### Hook Not Running

1. Check that the script is executable:
```bash
chmod +x .claude/hooks/auto-commit/auto-commit.sh
```

2. Verify the hook is configured in `.claude/settings.json`

3. Check for errors in Claude Code output

### Unwanted Amends

If the hook is amending too aggressively:

1. Reduce `MAX_COMMIT_AGE_SECONDS`
2. Increase the overlap percentage threshold
3. Add more specific type-matching logic

### Commits Not Meaningful Enough

The commit message generation is basic. For better messages:

1. Use Claude's `/commit` command manually
2. Adjust the analysis logic in `analyze_changes()` function
3. Add more sophisticated diff parsing

## Best Practices

1. **Review commits regularly** - Use `git log` to check what's been committed
2. **Squash before PR** - You may want to squash commits before creating a pull request
3. **Use with other hooks** - Combine with pre-commit hooks for code quality
4. **Disable for sensitive work** - Turn off for work requiring careful commit crafting

## Advanced: Hook Chaining

You can chain this with other hooks:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "true",
        "handler": {
          "type": "command",
          "command": "bash .claude/hooks/pre-commit-check.sh"
        }
      },
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

## Limitations

- Basic commit message generation (not as sophisticated as manual messages)
- May group commits that you'd prefer separate
- Cannot detect semantic meaning of changes
- Relies on file patterns and diff analysis

## Contributing

To improve the commit message generation:

1. Edit the `analyze_changes()` function
2. Add more pattern matching rules
3. Consider using LLM-based analysis for better messages

## License

MIT License - Same as the parent repository
