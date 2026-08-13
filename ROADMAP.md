# ClaimLens Roadmap

## Phase 0 — Define and freeze the product

- Define product scope and non-goals.
- Define billing scope.
- Define data objects and signal flow.
- Define repository ownership and development workflow.
- Define safety and PHI handling rules.

Success: a new contributor can explain ClaimLens, its boundaries, and its first measurable target without reading implementation code.

## Phase 1 — Evidence extraction

Input one synthetic outpatient psychiatric note and return a structured evidence object.

Success: evidence fields are traceable to the source note and unsupported facts are not invented.

## Phase 2 — Deterministic billing rules

Apply a narrow set of billing rules to structured evidence.

Success: known synthetic cases produce the expected support/unsupported/ambiguous determinations.

## Phase 3 — Claim compiler

Assemble a candidate claim from supported evidence and rules.

Success: ClaimLens explains exactly why each candidate service is supported.

## Phase 4 — Adversarial auditor

Challenge the candidate claim independently.

Success: deliberately weak, contradictory, or incomplete cases are flagged without excessive false alarms.

## Phase 5 — Benchmark

Create at least 100 known-answer synthetic/adversarial encounters.

Measure evidence extraction accuracy, claim accuracy, unsupported-code rate, missed supported services, hallucinated evidence, and audit false-positive/false-negative rates.

## Phase 6 — Payer overlays

Add payer-specific rule layers only after the base compiler is reliable.

## Phase 7 — Insurance intake and verification

Add insurance-card/ID extraction, payer resolution, provider-network matching, and eventually live eligibility through external integrations.

## Deferred until earned

EHR integration, autonomous claim submission, custom foundation-model training, broad medical-specialty support, large agent networks, and other advanced architecture remain out of scope until a measured product need justifies them.
