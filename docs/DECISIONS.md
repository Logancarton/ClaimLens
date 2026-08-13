# Decision Log

## 2026-08-12 — ClaimLens is the single active side-project focus

ClaimLens is being developed as a commercial healthcare billing/audit product. Scope discipline takes priority over exploratory AI architecture work.

## 2026-08-12 — Evidence extraction is separate from billing logic

The AI interprets clinical language into structured evidence. Deterministic rules decide what that evidence supports whenever the requirement can be represented explicitly.

Reason: a probabilistic language model should not silently become the authority for deterministic billing requirements.

## 2026-08-12 — Compiler and auditor are separate roles

The compiler constructs the strongest defensible candidate claim. The auditor independently looks for reasons the claim may be unsupported, incomplete, contradictory, or ambiguous.

## 2026-08-12 — Insurance verification is deferred

Insurance-card/ID extraction, payer resolution, network matching, and live eligibility are valuable but deferred until the core claim compiler is demonstrated. Effective implementation will likely require external integrations.

## 2026-08-12 — No real patient data in Git

Real patient/PHI data must never be committed to this repository. Synthetic or deliberately de-identified fixtures are used for development and benchmarking.

## 2026-08-12 — Runtime package uses the ClaimLens name

The Python package is `src/claimlens/`, not `src/claim_compiler/`. “Claim compiler” describes one subsystem; ClaimLens is the product/runtime namespace.

## 2026-08-12 — `rules/` is the single rule home

Billing/payer rules live under `rules/`. `data/` is reserved for synthetic development cases and known-answer benchmark fixtures. This prevents two competing rule sources of truth.

## 2026-08-12 — Repository autonomy is gated by project truth

AI agents may continue eligible work with minimal supervision, but autonomy is bounded by the repository. `docs/IMPLEMENTATION_STATUS.md` owns the current phase/gate, `docs/RELEASE_GATES.md` owns advancement requirements, and GitHub issues are a work queue rather than authority to skip gates.

Unresolved product scope, billing-policy interpretation, benchmark release thresholds, production PHI/security workflows, integration/vendor/licensing commitments, and phase-advancement decisions require human judgment unless already settled explicitly.

Reason: near-autonomous development should reduce repetitive supervision without allowing an agent to redefine what ClaimLens is or what counts as valid evidence.

## 2026-08-12 — Development and evaluation fixtures are separated by purpose

Synthetic fixtures are organized as `data/development_cases/` and `data/evaluation_cases/`. Development cases may be tuned against. Frozen evaluation cases are independent benchmark evidence and must not silently become tuning data.

Reason: separating data by purpose makes benchmark leakage harder and gives autonomous agents an unambiguous rule for fixture use.

## 2026-08-13 — Initial benchmark includes all three outpatient psychiatric service families

The v0.1 benchmark scope includes outpatient evaluation/management for psychiatric medication-management encounters, psychiatric diagnostic evaluation, and psychotherapy services/add-ons.

These are treated as one bounded outpatient psychiatric benchmark territory rather than expanding ClaimLens into multiple specialties.

## 2026-08-13 — PMHNP/NP and psychiatrist are distinct v0.1 provider classes

The benchmark includes both provider classes and preserves their identity separately. Shared behavior may use the same rule path, while any provider-specific difference must be backed by an authoritative source before ClaimLens treats it differently.

## 2026-08-13 — Initial commercial target is independent/small psychiatric practice

The first commercial validation target is an individual outpatient psychiatric clinician/practice owner or small psychiatric prescriber practice. Larger groups may follow after the core workflow is demonstrated; billing companies and health systems remain later expansion targets.

## 2026-08-13 — Delivery model is software plus optional human-reviewed audit service

ClaimLens is developed as software. An AI-assisted, human-reviewed audit service may be used as an early validation/delivery channel, but manual service work must not be misrepresented as autonomous software behavior.

## 2026-08-13 — v0.1 supports both pre-sign and pre-submit review

The same core engine supports `PRE_SIGN` and `PRE_SUBMIT` checkpoints. Pre-sign review surfaces gaps while the clinician controls the note without inventing documentation. Pre-submit review evaluates the finalized record as-is before claim submission.

## 2026-08-13 — Historical/copied-forward material does not silently become current evidence

Repetition alone is insufficient to treat historical/copied-forward material as current-encounter evidence. Explicit current reassessment/reaffirmation/action can support current temporal scope. When timing is materially unclear, ClaimLens preserves `UNCLEAR` and escalates the dependent result to human review.

## 2026-08-13 — Material unresolved uncertainty requires human review

Material `AMBIGUOUS` or `CONTRADICTORY` evidence, material `UNCLEAR` temporal scope, unresolved rule-source conflict, or unknown material applicability resolves to `REVIEW`. Explicitly absent required support may resolve deterministically to `UNSUPPORTED`; absence does not automatically require review.

## 2026-08-13 — Phase 0 specification approved and Gate 0 may advance

The product scope and v0.1 MVP finish line are approved. The canonical architecture, rule-governance expectations, benchmark design, and development PHI/security boundary were reviewed and remain consistent with the selected service/provider/workflow scope. No unresolved architecture conflict blocks Phase 1.

The human owner explicitly requested completion of the Phase 0 freeze. With the Gate 0 criteria satisfied, `docs/IMPLEMENTATION_STATUS.md` may advance to Phase 1 / Gate 1. Later-phase questions remain unresolved unless separately decided.
