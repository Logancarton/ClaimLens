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

The human owner explicitly decided that ClaimLens will use the AMA CPT Developer Program as the intended authorized development/testing access path for broader CPT-dependent work and will plan to obtain the appropriate commercial/product CPT license before CPT-dependent functionality is distributed commercially.

### Public AMA source use for the first narrow rule — RESOLVED

The human owner explicitly directed ClaimLens to continue Phase 2 using a narrowly paraphrased proposition that the AMA publishes openly, without copying the CPT dataset, full MDM grid, CPT descriptors, or comprehensive code/time tables.

The first implemented proposition is recorded in `rules/OUTPATIENT_EM_MEDICATION_MANAGEMENT.md`. This removes AMA Developer Program enrollment as a blocker for the **first narrow Gate 2 rule implementation**. It does not eliminate AMA copyright, future access requirements, or commercial product-licensing obligations.

### Current Phase 2 completion boundary — VERIFICATION PENDING, NOT A HUMAN POLICY QUESTION

The first source-verified outpatient E/M pathway, synthetic cases, and focused tests are implemented. Gate 2 remains open until the new focused tests and the full applicable unit suite are run on current `main` and their individual results are inspected.

This is a verification checkpoint rather than an unresolved product/billing decision. Do not start Phase 3 until verification is green and Gate 2 is formally evaluated.

## Non-blocking CPT access/licensing follow-up

AMA CPT Developer Program enrollment/access remains required for broader CPT-dependent development when the needed authoritative detail is not available under the narrow public-source boundary above. The planned commercial/product license remains required before commercial CPT-dependent distribution.

Until an applicable AMA agreement is obtained and reviewed:

- Do not copy or reconstruct the full CPT dataset, detailed MDM grid, CPT descriptors, or comprehensive code/time tables in Git.
- Do not substitute blogs, AI summaries, payer summaries, remembered coding rules, or inferred approximations for CPT authority.
- Do not treat CMS Medicare-specific propositions as universal base CPT rules.
- Any executed AMA agreement controls actual permissions for CPT access, storage, transformation, display, distribution, and AI use; repository summaries do not override it.

## Later-phase questions

These remain important but do not block currently authorized Phase 2 work unless explicitly made current.

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
