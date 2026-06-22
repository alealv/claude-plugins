---
name: isolated-worktree-commit
description: Commit your in-progress changes to a target branch (usually main) through a disposable git worktree, then fast-forward-merge and push — safe when the shared working tree is on another branch (a parallel agent hopped HEAD), is dirty, or holds other people's uncommitted work. Use whenever you must land a clean commit without disturbing whatever branch the main checkout currently sits on.
---

# Isolated worktree commit

Land your changes on a target branch (e.g. `main`) without touching the branch the main checkout is currently on.

## When to use

- **Multiple agents share one clone** and HEAD keeps hopping between feature branches — you can't safely `git checkout main` in the shared tree without disturbing someone's work.
- The working tree is **dirty with other people's uncommitted changes** and you only want to land *yours*.
- You want each change as its **own clean commit on the target branch** (no half-finished branch state in the shared tree).

If you own the working tree and it's clean, you don't need this — just commit on a branch and open a PR.

## The flow

> Re-run `git branch --show-current` and `git status --short` first — a parallel agent may have changed HEAD or staged files since your last command. Never `git add .` (you'd sweep their work); always name *your* paths.

```bash
# 1. Stash ONLY your files (scoped pathspec; -u includes untracked/new files).
git stash push -u -m "<feature> (move to worktree)" -- <path1> <path2> ...

# 2. Disposable worktree branched off the TARGET (e.g. main), not the current branch.
git worktree add .worktrees/<name> -b <feat-branch> main

# 3. (project setup) copy any secret/config the worktree needs to be functional
#    e.g. cp ../../.vault_pass .vault_pass ; export SOME_PATH=../../<dir>

# 4. Pop your stash into the worktree.
cd .worktrees/<name> && git stash pop

# 5. Edit/verify as needed, then commit with -F (NOT inline -m): some pre-commit
#    hooks grep the whole command line and trip on words in an inline message;
#    -F also dodges shell-quoting issues. End the message per the repo convention.
git add <your paths>
git commit -F /tmp/msg.txt

# 6. If hooks auto-fixed files (commit aborts / "files were modified by this hook"):
#    re-stage and amend — the staged content is now the hook-formatted version.
[ -n "$(git status --porcelain)" ] && git add -A && git commit --amend -F /tmp/msg.txt

# 7. Fast-forward the target to your branch. `branch -f` works because the target
#    is NOT checked out anywhere (the shared tree is on a different branch).
cd <repo-root>
git merge-base --is-ancestor main <feat-branch> && git branch -f main <feat-branch>

# 8. Push (verify FF over the remote first; confirm with the user before pushing to main).
git fetch origin main
git merge-base --is-ancestor origin/main main && git push origin main

# 9. Cleanup: remove copied secrets, drop the worktree + branch.
rm -f .worktrees/<name>/.vault_pass
git worktree remove .worktrees/<name>
[ "$(git rev-parse <feat-branch>)" = "$(git rev-parse main)" ] && git branch -D <feat-branch>
```

## Why each step matters

- **Scoped stash (`-- <paths>`):** the shared tree may hold a parallel agent's work; a blanket stash or `git add .` would scoop it into your commit. Stash and add only your files.
- **Worktree off the target:** lets you build a clean commit on a fresh checkout of `main` while the shared tree stays on its branch. The disposable worktree is auto-removed in step 9.
- **`git commit -F file`, not `-m`:** inline messages can trip command-scanning pre-commit hooks and shell quoting. A message file is robust. (Re-amend after hook auto-fixes.)
- **`git branch -f main <branch>` for the merge:** a true fast-forward that needs no checkout of `main`. It fails if `main` is checked out in some worktree, and it's only safe when `main` is an ancestor of your branch (the `--is-ancestor` guard) — otherwise do a real merge/rebase.
- **Push gate:** verify `origin/main` is an ancestor of local `main` (clean FF) and get explicit user confirmation before pushing to a protected/default branch.

## Gotchas

- **Branch hopping:** parallel agents silently change HEAD between your commands — re-verify the branch before every commit and before the FF merge.
- **Don't delete other worktrees:** `git worktree list` will show parallel streams' worktrees. Remove only the one you created.
- **`update-ref`/`branch -f` drift:** if you FF the target while the shared tree is *on* that target, the shared tree shows old content as "modified" — refresh with `git checkout HEAD -- <files>`. (Avoided here because the shared tree is on a different branch.)
- **Project-specific setup** (note for repos that need it): copy the secret/password file the build needs (e.g. an Ansible `.vault_pass`), and export any path env the tooling expects (e.g. a collections/deps dir pointing back at the parent clone — copy, don't symlink).

## Done means

- Your change is a single clean commit on the target branch, pushed (with the user's OK).
- The disposable worktree and feature branch are gone.
- The shared working tree and every parallel stream are untouched.
