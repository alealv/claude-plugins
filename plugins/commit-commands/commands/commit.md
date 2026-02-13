---
allowed-tools: Bash(git:*), Bash(ruff:*), Bash(prettier:*), Bash(eslint:*), Bash(black:*), Bash(cargo fmt:*), Bash(go fmt:*), Bash(ls:*), Read, Grep, Glob
argument-hint: [message] | --amend
description: Create self-contained commits with clear, conventional messages. Amends when updating the same task. Reads project conventions.
---

# Smart Commit

Create a well-formatted commit: $ARGUMENTS

## Current Repository State

- Git status: !`git status --porcelain`
- Current branch: !`git branch --show-current`
- Staged changes: !`git diff --cached --stat`
- Unstaged changes: !`git diff --stat`
- Recent commits: !`git log --oneline -5`

## Principles

1. **One task, one commit** - Each commit solves exactly one problem or adds one feature
2. **Clear messages** - Simple, specific, with appropriate emoji
3. **Amend when appropriate** - Update the previous commit if continuing the same task
4. **Follow project conventions** - Respect existing commit styles and guidelines
5. **Include ticket references** - Link to issues when identifiable

## Workflow

### 1. Check Project Conventions

Look for commit guidelines:
```bash
ls -la .commitlintrc* commitlint.config.* CONTRIBUTING.md 2>/dev/null || true
```

If found, read and follow those conventions.

### 2. Determine: New Commit or Amend?

**Amend** the previous commit if:
- User passed `--amend` argument
- You're fixing, updating, or completing the same task
- The previous commit is unpushed (`git status` shows "ahead of origin")
- Changes are directly related to the last commit's purpose

**New commit** if:
- Working on a different task/feature
- Previous commit is already pushed
- Changes represent a distinct logical unit

### 3. Extract Ticket/Issue Reference

Look for ticket references in branch name:
- Jira: `PROJ-123`, `ABC-456`
- GitHub: `#123`, `gh-123`
- Linear: `ENG-123`
- GitLab: `!123`, `#123`

### 4. Run Formatters (if no pre-commit hooks)

Check if pre-commit hooks exist:
```bash
ls -la .pre-commit-config.yaml .husky/ .git/hooks/pre-commit 2>/dev/null || true
```

**If hooks exist**: They will run automatically on `git commit`.

**If NO hooks exist**, run available formatters:
- Python: `ruff format .` or `black .`
- JavaScript/TypeScript: `prettier --write .` or `eslint --fix .`
- Rust: `cargo fmt`
- Go: `go fmt ./...`

Detect which tools are available and run them.

### 5. Stage and Commit

```bash
# Stage all changes (if not already staged)
git add -A

# For new commit:
git commit -m "emoji type(scope): description"

# For amend:
git commit --amend -m "emoji type(scope): description"
```

### 6. Verify

```bash
git log -1 --stat
```

Report: "Committed: `emoji type(scope): description`" or "Amended: `emoji type(scope): description`"

## Commit Message Format

```
emoji type(scope): description

[ticket reference if found]
```

**Rules:**
- Imperative mood: "add" not "added"
- Lowercase description
- Max 50 chars for first line
- Specific, not generic

## Emoji Reference

Each commit type is paired with an appropriate emoji:

### Core Types
| Emoji | Type | Description |
|-------|------|-------------|
| ✨ | feat | New feature |
| 🐛 | fix | Bug fix |
| 📝 | docs | Documentation |
| 💄 | style | Formatting/style |
| ♻️ | refactor | Code refactoring |
| ⚡️ | perf | Performance improvements |
| ✅ | test | Tests |
| 🔧 | chore | Tooling, configuration |
| 🚀 | ci | CI/CD improvements |
| ⏪️ | revert | Reverting changes |

### Extended Emojis
| Emoji | Type | When to use |
|-------|------|-------------|
| 🚨 | fix | Fix compiler/linter warnings |
| 🔒️ | fix | Fix security issues |
| 🚑️ | fix | Critical hotfix |
| 💚 | fix | Fix CI build |
| ✏️ | fix | Fix typos |
| 🔥 | fix | Remove code or files |
| 🩹 | fix | Simple fix for non-critical issue |
| 🥅 | fix | Catch errors |
| 👽️ | fix | Update code due to external API changes |
| 🔇 | fix | Remove logs |
| 🏷️ | feat | Add or update types |
| 💬 | feat | Add or update text and literals |
| 🌐 | feat | Internationalization and localization |
| 👔 | feat | Add or update business logic |
| 📱 | feat | Work on responsive design |
| 🚸 | feat | Improve user experience / usability |
| 🧵 | feat | Multithreading or concurrency |
| 🔍️ | feat | Improve SEO |
| 🥚 | feat | Add or update an easter egg |
| 🚩 | feat | Add, update, or remove feature flags |
| 🦺 | feat | Add or update validation |
| ✈️ | feat | Improve offline support |
| 🔊 | feat | Add or update logs |
| ♿️ | feat | Improve accessibility |
| 💥 | feat | Introduce breaking changes |
| 📈 | feat | Add analytics or tracking code |
| 🚚 | refactor | Move or rename resources |
| 🏗️ | refactor | Make architectural changes |
| ⚰️ | refactor | Remove dead code |
| 🎨 | style | Improve structure/format of the code |
| 💡 | docs | Add or update comments in source code |
| 🗃️ | db | Database related changes |
| 🧪 | test | Add a failing test |
| 🤡 | test | Mock things |
| 📸 | test | Add or update snapshots |
| 🎉 | chore | Begin a project |
| 🔖 | chore | Release/Version tags |
| 📌 | chore | Pin dependencies to specific versions |
| ➕ | chore | Add a dependency |
| ➖ | chore | Remove a dependency |
| 📦️ | chore | Add or update compiled files or packages |
| 🙈 | chore | Add or update .gitignore file |
| 📄 | chore | Add or update license |
| 🌱 | chore | Add or update seed files |
| 🧑‍💻 | chore | Improve developer experience |
| 👥 | chore | Add or update contributors |
| 🔀 | chore | Merge branches |
| 👷 | ci | Add or update CI build system |
| 🍱 | assets | Add or update assets |
| 💫 | ui | Add or update animations and transitions |
| ⚗️ | experiment | Perform experiments |
| 🚧 | wip | Work in progress |

## Examples

Good commit messages:
```
✨ feat(auth): add user authentication system
🐛 fix(api): resolve memory leak in rendering process
📝 docs(readme): update API documentation with new endpoints
♻️ refactor(utils): simplify error handling logic in parser
🔒️ fix(auth): strengthen password requirements
🦺 feat(form): add input validation for registration
💚 fix(ci): resolve failing pipeline tests
🏗️ refactor(core): reorganize module structure
```

With ticket reference:
```
✨ feat(auth): add JWT token refresh

Refs: AUTH-42
```

## Error Handling

- **No changes**: Report "Nothing to commit" and exit
- **Conflicts**: Stop and inform user
- **Detached HEAD**: Warn user before proceeding
- **Hook failures**: Report which hook failed and why
