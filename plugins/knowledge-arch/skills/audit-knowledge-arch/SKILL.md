---
name: audit-knowledge-arch
description: Audit the current repo's agent-knowledge architecture and report layer presence + health — size caps (AGENTS.md/CLAUDE.md < 200 lines, MEMORY.md < 24 KB, nested AGENTS.md < 32 KiB for Codex), missing @AGENTS.md import, code-structure prose that should be a graph query, missing nested AGENTS.md, duplicated facts. Use when the user asks to audit/check the agent docs, memory, or knowledge architecture, or when the SessionStart nudge fires.
---

# Audit the knowledge architecture

Reference: this plugin's `reference/methodology.md`. Produce a concise report — a table
`Layer | Status (✅/⚠️/❌) | Finding | Fix` — then a one-paragraph verdict. Don't change
files; this is read-only (offer to run `setup-knowledge-arch` for fixes).

Run these checks (from the repo root):

## Size caps
```bash
for f in AGENTS.md CLAUDE.md; do [ -f "$f" ] && printf "%-12s %s lines  %s B\n" "$f" "$(wc -l <"$f"|tr -d ' ')" "$(wc -c <"$f"|tr -d ' ')"; done
# Nested AGENTS.md (Codex reads root->cwd; combined < 32 KiB):
find . -name AGENTS.md -not -path '*/node_modules/*' -not -path '*/.git/*' -exec wc -c {} +
# Machine-local memory index (first 200 lines / 25 KB load; keep < 24 KB):
P="$HOME/.claude/projects/$(pwd | sed 's:/:-:g')/memory/MEMORY.md"
[ -f "$P" ] && printf "MEMORY.md   %s lines  %s B\n" "$(wc -l <"$P"|tr -d ' ')" "$(wc -c <"$P"|tr -d ' ')" || echo "MEMORY.md: none"
```
- `AGENTS.md` / `CLAUDE.md` **> 200 lines** → ⚠️ (community sweet spot ~150; both load in full every session).
- combined nested `AGENTS.md` **≥ 32 KiB** → ⚠️ (Codex truncates from the bottom).
- `MEMORY.md` **≥ 24 KB or > 200 lines** → ❌ (bottom entries silently dropped at load).

## Wiring & layers
```bash
head -1 CLAUDE.md                                   # must be @AGENTS.md
grep -qi "Knowledge Architecture" AGENTS.md && echo "KA section: yes" || echo "KA section: MISSING"
grep -qiE "graph-first|graphify (query|affected)" AGENTS.md CLAUDE.md && echo "graph-first rule: yes" || echo "graph-first rule: missing"
ls -d .claude/rules .claude/skills docs .specify/memory/constitution.md graphify-out 2>/dev/null
```
- `CLAUDE.md` first line ≠ `@AGENTS.md` → ⚠️ (the recommended cross-tool wrapper).
- No Knowledge Architecture section / graph-first rule in `AGENTS.md` → ⚠️.
- `.claude/rules/*.md` missing `paths:` frontmatter → ⚠️ (loads every session unconditionally).
- No constitution → ⚠️ (principles ungoverned).

## Graph-first & duplication (spot checks)
- `graphify-out/` absent but the repo is non-trivial → ⚠️ (no graph code layer; structure questions fall back to grep/prose).
- Look for hand-maintained **architecture prose / module maps / "X calls Y" diagrams** in `AGENTS.md`, `CLAUDE.md`, `docs/`, or memory that the code graph could answer on demand → ⚠️ "duplicates the graph, will go stale."
- Look for the same fact stated in **two** layers (docs + AGENTS, or memory + rules) → ⚠️ "one source per fact."

## Codex parity
```bash
# rules exist but no nested AGENTS.md mirroring them?
ls .claude/rules/*.md 2>/dev/null && find . -name AGENTS.md -not -path './AGENTS.md' -not -path '*/.git/*'
```
- `.claude/rules/` present but no per-directory `AGENTS.md` mirrors → ⚠️ (Codex can't read `.claude/rules/`).

## Procedures-in-the-wrong-place
- Multi-step procedures sitting in `CLAUDE.md` sections or memory topic files → ⚠️ "should be a skill."

End with: overall health (Healthy / Drifting / Needs setup) and the top 1-3 fixes. If fixes
are wanted, hand off to the `setup-knowledge-arch` skill.
