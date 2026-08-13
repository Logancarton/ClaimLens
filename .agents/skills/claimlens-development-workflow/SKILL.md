# ClaimLens Development Workflow Skill

## Purpose

Use this workflow for implementation, debugging, architecture review, testing, and repository cleanup in ClaimLens.

## Start from project truth

Read the canonical project documents listed in `AGENTS.md`. Do not infer architecture from filenames alone.

## Workflow

### 0. Resolve work state
Before selecting or continuing work, read `docs/IMPLEMENTATION_STATUS.md`, `docs/RELEASE_GATES.md`, `docs/OPEN_QUESTIONS.md`, and `.agents/AUTONOMY_POLICY.md`.

Confirm:

- Current phase and gate.
- Whether the requested/open issue belongs to that phase.
- Whether an unresolved human-decision blocker prevents work.
- Whether the change is authorized by settled project truth.

If no eligible task exists, stop and report the blocker instead of starting later-phase work.

### 1. State the requested outcome
Translate the request into one observable behavior or repository outcome.

### 2. Identify ownership
Locate the component that owns the behavior according to `docs/ARCHITECTURE.md`. Do not patch neighboring layers to avoid fixing the owner.

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

### 9. Synchronize project truth
Update `docs/IMPLEMENTATION_STATUS.md` only when evidence justifies a new status or work-state change. Add architecture/product decisions to `docs/DECISIONS.md` only when explicitly settled. Preserve unresolved items in `docs/OPEN_QUESTIONS.md`.

### 10. Finish cleanly
Review diff/status. Commit only coherent verified work with a descriptive message.

## Status vocabulary

- **Not Started** — no meaningful design or implementation.
- **Designed** — behavior/architecture is defined but not implemented.
- **Built** — implementation exists.
- **Integrated** — implementation participates in the real signal path.
- **Verified** — explicit tests/benchmarks demonstrate intended behavior.

## Default development principle

ClaimLens earns complexity through demonstrated need, not possibility.
