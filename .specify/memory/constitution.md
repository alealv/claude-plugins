<!--
  Sync Impact Report
  ==================
  Version change: 0.0.0 → 1.0.0 (initial ratification)

  Added principles:
    - I. DRY (Don't Repeat Yourself)
    - II. KISS (Keep It Simple, Stupid)
    - III. Tested Before Merged
    - IV. Lean Documentation
    - V. Stable Public Interface

  Added sections:
    - Technology Constraints
    - Development Workflow

  Templates requiring updates:
    - .specify/templates/plan-template.md ✅ no changes needed
      (Constitution Check section is already generic)
    - .specify/templates/spec-template.md ✅ no changes needed
      (User stories and requirements structure aligns)
    - .specify/templates/tasks-template.md ✅ no changes needed
      (Phase structure and parallel markers compatible)
    - .specify/templates/checklist-template.md ✅ no changes needed
      (Generic checklist structure)

  Follow-up TODOs: none
-->

# claude-tools Constitution

## Core Principles

### I. DRY (Don't Repeat Yourself)

Every piece of knowledge MUST have a single, authoritative source.

- Shared logic MUST be extracted into a common module rather than
  duplicated across files.
- Configuration values (paths, defaults, enums) MUST be defined once
  and imported where needed.
- Documentation MUST NOT restate what the code already expresses;
  reference the source instead.

**Rationale**: Duplication leads to divergent behavior and increases
maintenance cost. A single source of truth keeps the codebase small
and consistent.

### II. KISS (Keep It Simple, Stupid)

Choose the simplest solution that satisfies the requirement.

- New abstractions MUST solve a concrete, present problem; speculative
  design is prohibited.
- Prefer flat module structures over deep nesting.
- Avoid adding dependencies when the standard library or existing deps
  already cover the need.
- Three similar lines of code are preferable to a premature abstraction.

**Rationale**: Simplicity reduces bugs, lowers onboarding friction, and
makes the codebase easier to reason about.

### III. Tested Before Merged

Every behavioral change MUST be covered by tests before it reaches the
main branch.

- New features MUST include at least unit tests for core logic.
- Bug fixes MUST include a regression test that fails without the fix.
- The full suite (`just test`) MUST pass before committing.
- Code quality gates (`just quality`) MUST pass before committing.

**Rationale**: Tests are the executable specification. Untested code is
unverified code.

### IV. Lean Documentation

CLAUDE.md MUST contain only the information an AI agent needs to work
effectively in the repository. Details belong in specs or docs.

- CLAUDE.md covers: project overview, dev commands, architecture
  summary, key patterns, and critical gotchas.
- Detailed design decisions, feature specs, and implementation plans
  MUST live in `.specify/` or `docs/`.
- Comments in code MUST only appear where logic is non-obvious;
  self-documenting code is the default expectation.

**Rationale**: A lean guidance file stays accurate and useful. Bloated
docs become stale and ignored.

### V. Stable Public Interface

The CLI contract and the installation behavior MUST remain backward
compatible within a major version.

- The `claude-tools` command, its arguments, and its config type
  handling (commands, skills, agents, hooks) define the public API.
- Breaking changes to CLI behavior MUST increment the major version.
- Internal module layout (`_internal/`) is private and MAY change
  freely.

**Rationale**: Users and CI scripts depend on the CLI interface.
Stability builds trust and adoption.

## Technology Constraints

- **Language**: Python >=3.10
- **Package manager**: uv (not pip). All commands use `uv run`.
- **Build backend**: pdm-backend
- **Linting/formatting**: Ruff
- **Type checking**: ty
- **Testing**: pytest
- **TUI**: Rich
- **Task runner**: just (see `justfile`)
- **Versioning**: Dynamic via git tags (`scripts/get_version.py`).
  Never manually edit version numbers.

## Development Workflow

1. **Quality first**: Run `just quality` (format + lint + types) before
   committing.
2. **Test always**: Run `just test` and confirm a green suite.
3. **Commit style**: Conventional Commits with an emoji prefix
   (see git log for examples). Use `/commit` skill.
4. **Branch strategy**: Feature branches off `main`; merge via PR.
5. **No secrets in repo**: All sensitive data stays in password managers
   and is injected at runtime.

## Governance

This constitution is the highest-authority document for development
decisions in this repository. When a practice conflicts with the
constitution, the constitution wins.

- **Amendments** require: (1) a description of the change,
  (2) rationale, (3) version bump, and (4) update to this file.
- **Version policy**: MAJOR for principle removals or redefinitions,
  MINOR for new principles or sections, PATCH for clarifications.
- **Compliance**: Every PR and implementation plan SHOULD be checked
  against these principles. The plan template's "Constitution Check"
  section enforces this.

**Version**: 1.0.0 | **Ratified**: 2026-02-13 | **Last Amended**: 2026-02-13
