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

### CPT development/product licensing path — RESOLVED

The human owner explicitly decided that ClaimLens will use the AMA CPT Developer Program as the authorized development/testing access path for CPT-dependent work and will plan to obtain the appropriate commercial/product CPT license before CPT-dependent functionality is distributed commercially.

This decision is recorded in `docs/DECISIONS.md`. It does not assert that Developer Program enrollment, CPT portal access, a development agreement, or a commercial/product CPT license has already been completed or obtained.

### AMA CPT Developer Program enrollment/access — CURRENT EXTERNAL BLOCKER

The product-policy decision is complete, but the required external access step is not verified. The human owner must register/enroll ClaimLens through the AMA CPT Developer Program, obtain the applicable development access/agreement, and review the governing terms before restricted CPT detail is used in development.

Until that external step is verified:

- ClaimLens may continue public-authority source review, source/version metadata work, schema readiness review, generic rule-engine work, and tests that do not reproduce restricted CPT content.
- ClaimLens must not copy or reconstruct CPT descriptors, detailed MDM tables, code-level time thresholds, or other licensed CPT content in Git.
- An agent must not substitute a blog, AI summary, payer summary, remembered coding rule, or inferred approximation for CPT authority.
- The current CMS E/M material may support Medicare-specific propositions, but those propositions must not be silently generalized into universal base CPT rules.
- Any executed AMA agreement controls actual permissions for CPT access, storage, transformation, display, distribution, and AI use; repository summaries do not override it.

The planned commercial/product license remains a future distribution requirement. It is not claimed as obtained and does not need to be completed before authorized development/testing begins if the applicable AMA development agreement permits that work.

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
