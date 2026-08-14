# Open Questions

These questions are intentionally unresolved. Do not silently decide them inside implementation code.

## Blocking rule

An open question blocks work only when the current release gate, active issue, or settled architecture requires resolution. Otherwise preserve it here and continue with eligible work.

## Phase 0 review queue

None. Phase 0 decisions required for Gate 0 are resolved and recorded in `docs/DECISIONS.md` and the owning project-truth documents.

## Phase 1 review queue

None. Gate 1 is satisfied. The MedGemma/Ollama evidence-extraction baseline is verified against the current Phase 1 development cases, with prior failed and partial runs preserved in `docs/BASELINE_RESULTS.md`.

## Phase 2 current question

### First rule service family — BLOCKING

Which already-approved outpatient psychiatric service family should be implemented first as the Gate 2 deterministic rule baseline?

Current frozen options from `docs/BILLING_SCOPE.md`:

- Outpatient evaluation/management for psychiatric medication-management encounters.
- Psychiatric diagnostic evaluation.
- Psychotherapy services and psychotherapy add-ons.

Selecting the first service family is a human decision under `.agents/AUTONOMY_POLICY.md`. Until explicitly selected, agents must not choose one by convenience or begin authoritative rule implementation that assumes the choice.

## Later-phase questions

These remain important but do not block Phase 2 unless explicitly made current.

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
