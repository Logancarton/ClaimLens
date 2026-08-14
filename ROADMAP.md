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

## Phase 1 — Evidence extraction — COMPLETE

The frozen encounter/evidence contract is implemented and the model-backed development baseline is verified.

Gate 1 is satisfied: structured evidence is implemented; provenance and missing/ambiguous behavior work; the applicable unit suite passed; and the final local MedGemma/Ollama five-case development baseline matched 5/5 expected cases. Prior failed and partial results remain preserved in `docs/BASELINE_RESULTS.md`.

## Phase 2 — Deterministic billing rules — CURRENT

Apply a narrow set of source-verified rules to structured evidence.

The first rule family is outpatient evaluation/management for psychiatric medication-management encounters. The generic deterministic rule-engine contract is verified. The human owner selected the AMA CPT Developer Program as the authorized development/testing path, with appropriate commercial/product CPT licensing planned before commercial CPT-dependent distribution.

Current boundary: Developer Program enrollment/access and the applicable development agreement have not yet been verified. Detailed CPT-dependent E/M rule implementation remains blocked until that external access step is complete. CMS Medicare-specific propositions must not be substituted as universal base CPT rules.

Success: Gate 2 in `docs/RELEASE_GATES.md` is satisfied—at least one service family has source-verified rules, rule metadata/provenance exists, deterministic rule tests pass, and rule conflicts fail safely to review.

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
