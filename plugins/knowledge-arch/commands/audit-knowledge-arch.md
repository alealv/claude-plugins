---
description: Audit the current repo's agent-knowledge architecture (layers + size caps + drift).
---

Audit the current repository's agent-knowledge architecture using the
`audit-knowledge-arch` skill: check each layer's presence and health — AGENTS.md /
CLAUDE.md size caps (<200 lines), the `MEMORY.md` 24 KB load cap, the `@AGENTS.md`
wrapper, the graph-first rule, nested `AGENTS.md` for Codex parity, hand-maintained
code-structure prose that a graph query should answer, duplicated facts across layers,
and procedures sitting in the wrong place. Produce the `Layer | Status | Finding | Fix`
table and a short verdict. Read-only — offer the `setup-knowledge-arch` skill for fixes.
