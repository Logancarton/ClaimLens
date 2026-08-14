# Development Cases

This folder contains synthetic outpatient-psychiatry fixtures that may be inspected, edited, and tuned against during development.

Phase 1 cases test the frozen encounter-to-evidence contract in `docs/DATA_MODEL.md`. They remain **evidence-focused rather than billing-gold cases**: they must not create billing rules or silently become frozen evaluation data.

Current human-readable Phase 1 seed cases:

- `DEV-001-clear-current-medication-activity.md` — clear current condition and medication continuation.
- `DEV-002-ambiguous-medication-change.md` — a discussed future change must not become a documented current dose change.
- `DEV-003-contradictory-current-medication-plan.md` — conflicting current plan statements must remain contradictory.
- `DEV-004-copied-forward-history-noise.md` — historical medication change must not be relabeled as current activity.
- `DEV-005-medication-list-without-current-plan.md` — medication presence alone must not become current management activity.

`phase1_baseline_cases.json` makes those same synthetic evidence behaviors executable with explicit `PRE_SIGN`/`PRE_SUBMIT` workflow metadata and both PMHNP/NP and psychiatrist provider classes. It is development data and may be tuned against; it is not the frozen v0.1 evaluation set.

## Phase 2 rule-development cases

`phase2_outpatient_em_rule_cases.json` contains synthetic known-answer inputs for the first source-verified outpatient E/M rule pathway. Its expected billing-rule outcomes are legitimate only because the owning proposition and primary AMA sources are recorded in `rules/OUTPATIENT_EM_MEDICATION_MANAGEMENT.md`.

The Phase 2 cases cover:

- a supported established office/outpatient pathway;
- an unsupported instance of that narrow pathway;
- material ambiguity that must route to `REVIEW`; and
- a new-patient case for which the established-patient rule is `NOT_APPLICABLE`.

Rule-source conflict behavior is exercised separately in `tests/test_outpatient_em_rules.py` because it depends on competing rule definitions rather than encounter facts.

These Phase 2 development cases do not reproduce the complete CPT MDM table, CPT descriptors, or comprehensive code/time tables. They must not be broadened from memory or secondary coding summaries.

All content here is synthetic. Do not place real patient data, copied PHI, credentials, or proprietary payer material in this folder.
