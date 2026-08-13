# Open Questions

These questions are intentionally unresolved. Do not silently decide them inside implementation code.

## Blocking rule

An open question blocks work only when the **current release gate, active issue, or settled architecture requires that question to be resolved**. Otherwise preserve it here and continue with eligible work.

When a question becomes blocking, an autonomous agent must stop at the smallest decision boundary and request human judgment rather than selecting an answer by convenience.

## Phase 0 review queue

These questions should be reviewed during Phase 0 because they may materially shape v0.1. Their presence does not automatically mean every Phase 0 task is blocked.

### Product / workflow

- Is the first paid user an individual psychiatric clinician, a group practice, a billing company, or a health system?
- Is ClaimLens first sold as software, an AI-assisted audit service, or both?
- Does the first workflow run before note signing, before claim submission, or both?

### Billing scope

- Which provider types are in scope for version 1?

### Evidence

- What is the minimum evidence schema for the selected v0.1 benchmark service families?
- How should copied-forward historical content be distinguished from current encounter evidence?
- What confidence/ambiguity states should trigger mandatory human review?

## Later-phase questions

These remain important but should not block unrelated Phase 0 work unless a new explicit decision makes them current.

### Payer

- Which payer is the first payer-specific overlay after base logic?

### AI

- Which local model becomes the first baseline evidence extractor?
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

1. Record the decision in `docs/DECISIONS.md` when it changes product, architecture, billing scope, or operating policy.
2. Update the owning project-truth document.
3. Remove or mark the question resolved here only after those sources agree.
