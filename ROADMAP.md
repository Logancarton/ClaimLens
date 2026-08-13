# ClaimLens Roadmap

## Phase 0 — Define and freeze the product

Phase 0 converts the product idea into repository truth that implementation is not allowed to silently redefine.

### Defined in repository truth

- [x] Product purpose, target setting, boundaries, and non-goals are defined in `docs/PRODUCT_SCOPE.md`, `docs/USE_CASES.md`, `docs/MVP_DEFINITION.md`, and `docs/PRODUCT_REQUIREMENTS.md`.
- [x] The initial billing territory and rule-authority model are defined in `docs/BILLING_SCOPE.md` and `docs/RULE_GOVERNANCE.md`.
- [x] The initial benchmark service scope is selected in `docs/BILLING_SCOPE.md` and recorded in `docs/DECISIONS.md`.
- [x] The minimum v0.1 evidence schema for the selected benchmark scope is defined in `docs/DATA_MODEL.md` and aligned with `docs/ARCHITECTURE.md`.
- [x] Core data objects and the canonical signal flow are defined in `docs/DATA_MODEL.md` and `docs/ARCHITECTURE.md`.
- [x] Repository ownership, maintenance responsibilities, autonomous-work boundaries, and the development workflow are defined in `docs/FILE_MAP.md`, `AGENTS.md`, and `.agents/`.
- [x] Development safety, PHI boundaries, secret handling, and the production-data stop boundary are defined in `docs/SECURITY_AND_DATA.md`.
- [x] The initial benchmark structure and evaluation discipline are defined in `docs/BENCHMARK_PLAN.md`.

### Remaining Gate 0 work

- [ ] Complete the required human review of product scope and the v0.1 finish line.
- [ ] Resolve any Phase 0 open question that becomes material to the selected v0.1 workflow.
- [ ] Confirm that no unresolved architecture conflict blocks Phase 1.
- [ ] Record any resulting decisions in `docs/DECISIONS.md`, synchronize affected project-truth files, and update `docs/IMPLEMENTATION_STATUS.md` only when Gate 0 evidence actually supports advancement.

Success: a new contributor can explain ClaimLens, its boundaries, its canonical signal flow, and its first measurable target without reading implementation code, and `docs/RELEASE_GATES.md` Gate 0 is satisfied.

Phase 1 remains blocked until `docs/IMPLEMENTATION_STATUS.md` records Gate 0 as satisfied.

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
