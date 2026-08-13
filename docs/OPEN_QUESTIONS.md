# Open Questions

These questions are intentionally unresolved. Do not silently decide them inside implementation code.

## Blocking rule

An open question blocks work only when the current release gate, active issue, or settled architecture requires resolution. Otherwise preserve it here and continue with eligible work.

## Phase 0 review queue

None. Phase 0 decisions required for Gate 0 are resolved and recorded in `docs/DECISIONS.md` and the owning project-truth documents.

## Phase 1 current question

### Model runtime / transport

- Which local runtime/transport should execute the selected `google/medgemma-1.5-4b-it` baseline: Transformers, Ollama, a llama.cpp-compatible path, or another explicitly approved mechanism?

The model choice itself is resolved. Runtime selection is now material because it can introduce dependencies, model-access terms, deployment behavior, and external-service assumptions. Do not silently select one in implementation.

## Later-phase questions

These remain important but do not block Phase 1 unless explicitly made current.

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
