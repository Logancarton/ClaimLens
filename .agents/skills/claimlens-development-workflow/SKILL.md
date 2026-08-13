# ClaimLens Development Workflow Skill

## Purpose

Use this workflow for implementation, debugging, architecture review, testing, and repository cleanup in ClaimLens.

## Start from project truth

Read the canonical project documents listed in `AGENTS.md`. Do not infer architecture from filenames alone. Use `docs/FILE_MAP.md` as the maintenance key for deciding where work belongs and which companion files must be checked when something changes.

## Workflow

### 0. Resolve work state
Before selecting or continuing work, read `docs/IMPLEMENTATION_STATUS.md`, `docs/RELEASE_GATES.md`, `docs/OPEN_QUESTIONS.md`, `.agents/AUTONOMY_POLICY.md`, and the relevant portion of `docs/FILE_MAP.md`.

Confirm:

- Current phase and gate.
- Whether the requested/open issue belongs to that phase.
- Whether an unresolved human-decision blocker prevents work.
- Whether the change is authorized by settled project truth.
- Which files `docs/FILE_MAP.md` says must be checked if this category of change is made.

If no eligible task exists, stop and report the blocker instead of starting later-phase work.

### 1. State the requested outcome
Translate the request into one observable behavior or repository outcome.

### 2. Identify ownership
Locate the component that owns the behavior according to `docs/ARCHITECTURE.md` and `docs/FILE_MAP.md`. Do not patch neighboring layers to avoid fixing the owner.

### 3. Establish the baseline
Use an existing test or create the smallest known-answer synthetic case that exposes the current behavior.

### 4. Preserve evidence boundaries
When working with AI output, require structured fields, provenance, uncertainty/ambiguity, and explicit absence. Never convert an unsupported model guess into evidence.

### 5. Preserve rule boundaries
Deterministic requirements belong in the rule system with source/version metadata. Prompts may explain or extract; they do not become authoritative billing policy.

### 6. Implement the smallest systemic change
Avoid one-case patches. Fix the process that caused the failure while preserving component ownership.

### 7. Verify
Run focused tests first, then broader tests. For AI behavior, use known-answer cases and record both false positives and false negatives where relevant.

### 8. Review for drift
Before completion ask:

- Did this expand product scope?
- Did AI absorb deterministic logic?
- Did a rule lose provenance?
- Did we introduce unnecessary infrastructure?
- Did any real patient/PHI data, credentials, or secrets enter the repository?
- Did we silently answer an open question or cross a release gate?

### 9. Synchronize all affected files
A task is not complete when only the primary implementation file is correct. Use the change matrix in `docs/FILE_MAP.md` to identify the affected set, then update every repository file whose truth, path, interface, example, test expectation, or project state is materially affected by the change.

Check and update, when applicable:

- Runtime/source files.
- Tests and test helpers.
- Development/evaluation fixtures.
- Prompts and rules.
- README, file maps, architecture, data model, terminology, scope, benchmark, security, and release-gate documentation.
- `docs/IMPLEMENTATION_STATUS.md` when status/work state changed.
- `docs/DECISIONS.md` only for explicitly settled decisions.
- `docs/OPEN_QUESTIONS.md` when an open question was explicitly resolved or a new blocker was discovered.
- GitHub issue/PR body or checklist state for tracked work.
- Agent/skill instructions when repository structure or workflow changed.

If `docs/FILE_MAP.md` identifies a companion file and it is intentionally not modified, verify that its existing content is still accurate. Do not touch unrelated files merely to create churn. "All files" means all files materially affected by the command.

### 10. Search for stale references
Search the repository for names, paths, interfaces, terminology, or assumptions changed by the task. Fix stale references before completion.

Examples include:

- Renamed files/directories still referenced in docs.
- Old class/function/interface names in tests or examples.
- A status document still saying Not Started after verified implementation.
- A GitHub issue checklist that no longer reflects completed work.
- A benchmark or fixture path that points to a previous folder name.

### 11. Final repository review
Review the complete diff/status, not only the file you intended to edit.

Confirm:

- The applicable `docs/FILE_MAP.md` change-matrix row was followed.
- Every affected companion file is synchronized.
- Tests/verification reflect the final state.
- No stale references remain.
- No unrelated changes were accidentally included.
- Project truth and tracked issue/PR state match the repository.

### 12. Finish cleanly
Commit only coherent verified work with a descriptive message. Report what changed, what was verified, and any remaining blocker.

## Status vocabulary

- **Not Started** — no meaningful design or implementation.
- **Designed** — behavior/architecture is defined but not implemented.
- **Built** — implementation exists.
- **Integrated** — implementation participates in the real signal path.
- **Verified** — explicit tests/benchmarks demonstrate intended behavior.

## Default development principle

ClaimLens earns complexity through demonstrated need, not possibility.
