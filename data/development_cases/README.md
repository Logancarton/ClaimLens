# Development Cases

This folder contains synthetic outpatient-psychiatry fixtures that may be inspected, edited, and tuned against during development.

Phase 1 uses these cases to test the frozen encounter-to-evidence contract in `docs/DATA_MODEL.md`. They remain **evidence-focused rather than billing-gold cases**: they must not create billing rules, assert candidate services, or silently become frozen evaluation data.

Current human-readable seed cases:

- `DEV-001-clear-current-medication-activity.md` — clear current condition and medication continuation.
- `DEV-002-ambiguous-medication-change.md` — a discussed future change must not become a documented current dose change.
- `DEV-003-contradictory-current-medication-plan.md` — conflicting current plan statements must remain contradictory.
- `DEV-004-copied-forward-history-noise.md` — historical medication change must not be relabeled as current activity.
- `DEV-005-medication-list-without-current-plan.md` — medication presence alone must not become current management activity.

`phase1_baseline_cases.json` makes those same synthetic behaviors executable with explicit `PRE_SIGN`/`PRE_SUBMIT` workflow metadata and both PMHNP/NP and psychiatrist provider classes. It is development data and may be tuned against; it is not the frozen v0.1 evaluation set.

Expected observations are test targets for evidence state, provenance, temporal scope, provider/workflow preservation, and review-preserving uncertainty. They are not executable billing policy.

All content here is synthetic. Do not place real patient data, copied PHI, credentials, or proprietary payer material in this folder.
