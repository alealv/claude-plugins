---
description: Resume work from a previous handoff session
argument-hint: [handoff-filename]
allowed-tools: Read, Bash(ls:*), Bash(git:*), Glob
---

Resumes work from a previous handoff session which are stored in `.claude/handoffs`.

Requested handoff file: `$ARGUMENTS`

## Process

### 1. Check for handoffs directory

First verify the handoffs directory exists:

```bash
ls .claude/handoffs/ 2>/dev/null
```

If the directory does not exist or is empty, inform the user:
> No handoff files found. Use `/handoff` to create one first.

Then stop.

### 2. List or locate handoff file

If no handoff file was provided, list all available handoffs. Read each file and extract the first `# ` heading as the title. Present them as a numbered list like:

> **Available Handoffs:**
> 1. `2025-03-15-implement-auth.md` - Implement Authentication
> 2. `2025-03-14-fix-issue-42.md` - Fix Issue #42
>
> To pick up a handoff, use: `/pickup <filename>`

Then stop and wait for the user to choose.

If a handoff file was provided, locate it in `.claude/handoffs/`. The filename might be partial or misspelled -- use glob matching to find the best match. If there are multiple matches, ask the user which one they want.

### 3. Check repository state

Before diving into the handoff, check the current state of the repository so you understand the starting point:

```bash
git status
git branch --show-current
git log --oneline -5
```

Note any uncommitted changes, the current branch, and recent commits. If the repo state looks like it diverged from what the handoff describes (e.g., different branch, conflicting changes), flag this to the user before proceeding.

### 4. Read the handoff

Read the full contents of the handoff file.

### 5. Review and Plan

After reading the handoff, summarize back to the user:
- What the handoff is about (primary request and intent)
- Where things left off (current work section)
- What the proposed next step is
- Whether the current repo state aligns with what the handoff expects

Then ask the user: **"Ready to proceed, or would you like to adjust the plan?"**

Only continue once the user confirms.

### 6. Resume work

Follow the instructions and next steps described in the handoff file. The handoff contains the full context needed to continue the work.
