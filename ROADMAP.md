# ClaimLens Roadmap

## Phase 0 — Define and freeze the product — COMPLETE

Phase 0 converted the product idea into repository truth that implementation is not allowed to silently redefine.

### Frozen in repository truth

- [x] Product purpose, target user, boundaries, and non-goals are approved.
- [x] Initial commercial target and delivery model are selected.
- [x] Initial service scope and distinct PMHNP/NP and psychiatrist provider classes are selected.
- [x] Both `PRE_SIGN` and `PRE_SUBMIT` workflow checkpoints are defined.
- [x] Minimum v0.1 evidence schema is defined.
- [x] Historical/copied-forward handling and mandatory human-review conditions are defined.
- [x] Canonical signal flow and component ownership are confirmed.
- [x] Repository ownership and development workflow are defined.
- [x] Development PHI/security boundaries are confirmed.
- [x] Benchmark structure and evaluation discipline are confirmed.
- [x] No unresolved architecture conflict blocks implementation.
- [x] Gate 0 is satisfied and Phase 1 is authorized.

Success achieved: a new contributor can explain ClaimLens, its boundaries, canonical signal flow, first measurable target, provider/service scope, and safety rules without reading implementation code.

## Phase 1 — Evidence extraction — CURRENT

Implement the frozen encounter/evidence contract and convert one synthetic outpatient psychiatric encounter into structured evidence.

Phase 1 must preserve provider class, workflow stage, provenance, explicit uncertainty, and current/historical/unclear temporal scope.

Success: Gate 1 in `docs/RELEASE_GATES.md` is satisfied—structured evidence is implemented, provenance and missing/ambiguous states work, synthetic development cases pass expected behavior, and the first extraction baseline is recorded.

## Phase 2 — Deterministic billing rules

Apply a narrow set of source-verified rules to structured evidence.

Success: known synthetic cases produce expected support/unsupported/ambiguous determinations and rule conflicts fail safely to review.

## Phase 3 — Claim compiler

Assemble a candidate claim from supported evidence and rules.

Success: ClaimLens explains exactly why each candidate service is supported and rejects unsupported-service traps.

## Phase 4 — Adversarial auditor

Challenge the candidate claim independently.

Success: deliberately weak, contradictory, incomplete, or uncertain cases are flagged without excessive false alarms.

## Phase 5 — Benchmark

Create at least 100 known-answer synthetic/adversarial encounters.

Measure evidence extraction accuracy, temporal-scope accuracy, claim accuracy, unsupported-code rate, missed supported services, hallucinated evidence, correct review escalation, and audit false-positive/false-negative rates.

## Phase 6 — Payer overlays

Add payer-specific rule layers only after the base compiler is reliable.

## Phase 7 — Insurance intake and verification

Add insurance-card/ID extraction, payer resolution, provider-network matching, and eventually live eligibility through external integrations.

## Deferred until earned

EHR integration, autonomous claim submission, custom foundation-model training, broad medical-specialty support, large agent networks, and other advanced architecture remain out of scope until a measured product need justifies them.
