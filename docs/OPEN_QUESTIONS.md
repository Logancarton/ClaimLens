# Open Questions

These questions are intentionally unresolved. Do not silently decide them inside implementation code.

## Blocking rule

An open question blocks work only when the current release gate, active issue, or settled architecture requires resolution. Otherwise preserve it here and continue with eligible work.

## Phase 0 review queue

None. Phase 0 decisions required for Gate 0 are resolved and recorded in `docs/DECISIONS.md` and the owning project-truth documents.

## Phase 1 review queue

None. Gate 1 is satisfied. The MedGemma/Ollama evidence-extraction baseline is verified against the current Phase 1 development cases, with prior failed and partial runs preserved in `docs/BASELINE_RESULTS.md`.

## Phase 2 current questions

### First rule service family — RESOLVED

The human owner selected **outpatient evaluation/management for psychiatric medication-management encounters** as the first Gate 2 deterministic rule family. The decision is recorded in `docs/DECISIONS.md`.

### Detailed CPT E/M rule source / licensing — BLOCKING FOR RESTRICTED CPT DETAIL

The current authoritative-source review confirms that outpatient E/M level selection ultimately depends on the AMA CPT E/M guidelines. CMS's May 2026 `MLN006764 — Evaluation and Management Services` provides current Medicare guidance but explicitly directs users to the AMA E/M Services Guidelines for the detailed MDM breakdown.

ClaimLens may continue Phase 2 work that uses public authoritative propositions, source metadata, generic rule-engine infrastructure, and tests. It must **not** copy or embed restricted CPT descriptors, detailed MDM tables, code-level time thresholds, or other licensed CPT content unless the human owner confirms that ClaimLens has appropriate rights/access for the intended product use.

This does not authorize an agent to replace CPT authority with a blog, AI summary, payer summary, remembered coding rule, or inferred approximation.

## Later-phase questions

These remain important but do not block currently authorized Phase 2 preparation unless explicitly made current.

### Payer

- Which payer is the first payer-specific overlay after base logic?

### AI

- Should the auditor use the same model with a separate prompt or a genuinely independent model/process?
- At what measured failure point would fine-tuning be justified?

### Product operations

- What result format is most useful to clinicians/billers?
- How will rule updates be reviewed and released?
- What customer-level ROI metric becomes the primary commercial proof?

### Deferred integration

- Which clearinghouse/eligibility integration is most practical for insurance verification?
- How will provider network participation be sourced authoritatively?

## Resolution rule

When a question is explicitly resolved:

1. Record the decision in `docs/DECISIONS.md` when it changes product, architecture, scope, or operating policy.
2. Update the owning project-truth document.
3. Remove or mark the question resolved here only after those sources agree.
