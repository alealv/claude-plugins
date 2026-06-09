#!/bin/sh
# SessionStart nudge for the knowledge-arch plugin.
# Fast and SILENT by default — emits a short note (added to session context) only when a
# project's agent-knowledge layers have actually drifted (over a load cap or mis-wired).
# A healthy project, or one not using the methodology, produces no output.

proj="${CLAUDE_PROJECT_DIR:-$PWD}"
cd "$proj" 2>/dev/null || exit 0

issues=""
add() { issues="${issues}
  - $1"; }

# AGENTS.md: lean contract + wrapper wiring (only nudge if the project opted into AGENTS.md)
if [ -f AGENTS.md ]; then
  n=$(wc -l < AGENTS.md 2>/dev/null | tr -d ' ')
  [ "${n:-0}" -gt 200 ] && add "AGENTS.md is ${n} lines (>200 — keep the agent contract lean; move detail to docs/rules/skills)"
  if [ -f CLAUDE.md ] && [ "$(head -1 CLAUDE.md 2>/dev/null)" != "@AGENTS.md" ]; then
    add "CLAUDE.md does not start with @AGENTS.md (the recommended cross-tool wrapper)"
  fi
fi

# CLAUDE.md bloat (a real issue regardless of methodology)
if [ -f CLAUDE.md ]; then
  n=$(wc -l < CLAUDE.md 2>/dev/null | tr -d ' ')
  [ "${n:-0}" -gt 200 ] && add "CLAUDE.md is ${n} lines (>200 — both load in full every session)"
fi

# Machine-local auto-memory index over its load cap (silent data loss)
mem="$HOME/.claude/projects/$(printf '%s' "$proj" | sed 's:/:-:g')/memory/MEMORY.md"
if [ -f "$mem" ]; then
  b=$(wc -c < "$mem" 2>/dev/null | tr -d ' ')
  [ "${b:-0}" -ge 24576 ] && add "auto-memory MEMORY.md is $((b/1024)) KB (>=24 KB — only the first 200 lines / 25 KB load; bottom index entries are dropped)"
fi

[ -z "$issues" ] && exit 0

printf 'Knowledge-architecture nudge (knowledge-arch plugin):%s\n\nRun /audit-knowledge-arch for the full report, or use the setup-knowledge-arch skill to fix.\n' "$issues"
exit 0
