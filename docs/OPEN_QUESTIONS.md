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

### CPT development/product licensing path — BLOCKING FOR RESTRICTED CPT DETAIL

Current AMA materials identify a CPT Developer Program that offers new organizations royalty-free CPT access for building and testing innovations. Separate AMA licensing guidance states that electronic products that use or rely on CPT content require an appropriate license for the actual product/use case, and new AI products should submit a licensing application so the AMA can determine the appropriate licensing approach.

Human decision required:

- Should ClaimLens use the AMA CPT Developer Program as the authorized development-access path and plan to obtain the appropriate product/distribution license before commercial CPT-dependent use?

Until explicitly resolved:

- ClaimLens may continue public-authority propositions, source metadata, generic rule-engine work, and tests that do not reproduce restricted CPT content.
- ClaimLens must not copy or reconstruct CPT descriptors, detailed MDM tables, code-level time thresholds, or other licensed CPT content in Git.
- An agent must not substitute a blog, AI summary, payer summary, remembered coding rule, or inferred approximation for CPT authority.
- Any later executed AMA agreement controls the actual permissions for CPT access, storage, transformation, display, distribution, and AI use; repository summaries do not override it.

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
