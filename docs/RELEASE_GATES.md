# Release Gates

A phase advances because its gate is met, not because enough code was written.

## Gate 0 — Specification frozen enough to build

Required:

- Product scope reviewed.
- MVP finish line reviewed.
- Initial billing/service family selected.
- Evidence schema questions narrowed enough for Phase 1.
- No unresolved architecture conflict blocking implementation.

## Gate 1 — Evidence extraction baseline

Required:

- Structured evidence schema implemented.
- Provenance preserved.
- Explicit missing/ambiguous states work.
- Synthetic development cases pass expected extraction behavior.
- Baseline benchmark recorded.

## Gate 2 — Rule engine baseline

Required:

- At least one service family has source-verified rules.
- Rule metadata/provenance exists.
- Deterministic rule tests pass.
- Rule conflicts fail safely to review.

## Gate 3 — Compiler baseline

Required:

- Candidate service links back to evidence and rule evaluations.
- Unsupported-service traps are rejected.
- Missing-support cases cannot silently compile as supported.

## Gate 4 — Auditor baseline

Required:

- Auditor catches predefined defect categories.
- False-positive rate is measured on clean cases.
- Auditor cannot invent missing evidence as a repair.

## Gate 5 — v0.1 benchmark

Required:

- Frozen evaluation set.
- Reproducible run.
- Evidence, compiler, and auditor metrics recorded.
- Known major failure modes documented.
- Decision made: iterate, pilot, or stop.

## Gate 6 — Pilot readiness

Defined only after v0.1 results justify continuing toward operational use.
