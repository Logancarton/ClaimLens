# Development Cases

This folder contains synthetic outpatient-psychiatry fixtures that may be inspected, edited, and tuned against during development.

These cases are intentionally **evidence-focused rather than billing-gold cases** while ClaimLens remains in Phase 0. The exact first billing/service family and minimum evidence schema are still unresolved in `docs/OPEN_QUESTIONS.md`, so development fixtures here must not silently choose a code family, create billing rules, or define a runtime schema by convenience.

Use the conceptual objects already defined in `docs/DATA_MODEL.md` when reviewing these cases: `ConditionAddressed`, `MedicationActivity`, `PsychotherapyEvidence`, provenance, uncertainty, and contradiction state. Treat the expected observations as design/test targets for evidence handling, not as executable billing policy.

Current seed cases:

- `DEV-001-clear-current-medication-activity.md` — clear current condition and medication continuation.
- `DEV-002-ambiguous-medication-change.md` — a discussed future change must not become a documented current dose change.
- `DEV-003-contradictory-current-medication-plan.md` — conflicting current plan statements must remain contradictory.
- `DEV-004-copied-forward-history-noise.md` — historical medication change must not be relabeled as current activity.
- `DEV-005-medication-list-without-current-plan.md` — medication presence alone must not become current management activity.

All content here is synthetic. Do not place real patient data, copied PHI, credentials, or proprietary payer material in this folder.
