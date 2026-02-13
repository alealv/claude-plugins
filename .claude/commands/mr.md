---
allowed-tools: Bash(git:*), Bash(gh:*), Bash(glab:*), Bash(ruff:*), Bash(prettier:*), Bash(eslint:*), Bash(black:*), Bash(cargo fmt:*), Bash(go fmt:*), Bash(ls:*), Bash(which:*), Read, Grep, Glob
argument-hint: [MR/PR title or description]
description: Commit, push, and open a merge/pull request. Auto-detects GitHub or GitLab remote.
---

# Merge Request

Commit all changes, push, and open a merge/pull request: $ARGUMENTS

## Current Repository State

- Git status: !`git status --porcelain`
- Current branch: !`git branch --show-current`
- Full diff (staged + unstaged): !`git diff HEAD`
- Recent commits: !`git log --oneline -10`
- Remote tracking: !`git status -sb`
- Remote URL: !`git remote get-url origin 2>/dev/null || echo "no remote"`

## Workflow

### 1. Detect Remote Platform

Inspect the `origin` remote URL:
- Contains `github.com` → **GitHub** (use `gh`)
- Contains `gitlab.com` or any GitLab instance → **GitLab** (use `glab`)
- Otherwise → ask the user

Verify the CLI is available:
```bash
which gh glab 2>/dev/null
```

If the required CLI is missing, report the install command and stop:
- GitHub: `brew install gh`
- GitLab: `brew install glab`

### 2. Branch Check

If on `main`, `master`, or the default branch:
- Create a new branch. Derive name from the diff context.
- Format: `type/short-description` (e.g., `feat/add-auth`, `fix/memory-leak`)
- Switch to the new branch before committing.

If already on a feature branch, stay on it.

### 3. Run Formatters (if no pre-commit hooks)

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

### 4. Stage and Commit

Follow the same commit message format as `/commit`:

```
emoji type(scope): description
```

**Rules:**
- Imperative mood, lowercase description
- Max 50 chars for first line
- Pick emoji from the Emoji Reference (same as `/commit`)

### 5. Push

```bash
git push -u origin <branch-name>
```

### 6. Create Merge/Pull Request

**GitHub:**
```bash
gh pr create --title "title" --body "$(cat <<'EOF'
## Summary

- <bullet points>

## Test Plan

- [ ] <verification steps>
EOF
)"
```

**GitLab:**
```bash
glab mr create --title "title" --description "$(cat <<'EOF'
## Summary

- <bullet points>

## Test Plan

- [ ] <verification steps>
EOF
)"
```

**MR/PR body**:
- `## Summary` - 1-3 bullet points extracted from the diff
- `## Test Plan` - Concrete verification steps as a checklist
- If a ticket reference is found in the branch name, include it

### 7. Report

Output the MR/PR URL and a one-line summary. Nothing else.

## Emoji Reference

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

## Error Handling

- **No changes**: Report "Nothing to ship" and exit
- **CLI missing**: Report install command and stop
- **Not authenticated**: Report the auth command (`gh auth login` / `glab auth login`)
- **MR/PR already exists**: Report the existing URL instead

## Efficiency

Be concise. Execute branch creation, staging, committing, pushing, and MR/PR creation using parallel tool calls where possible. Do not send unnecessary text beyond the final URL report.
