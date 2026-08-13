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

Billing/payer rules live under `rules/`. `data/` is reserved for synthetic development cases and known-answer test fixtures. This prevents two competing rule sources of truth.
