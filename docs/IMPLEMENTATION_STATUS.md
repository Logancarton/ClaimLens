# Implementation Status

## Current work state

- **Current phase:** Phase 1 — Evidence extraction baseline.
- **Current gate:** Gate 1 — Evidence extraction baseline.
- **Gate 0 status:** **SATISFIED** — Phase 0 specification freeze completed 2026-08-13.
- **Gate 1 status:** **NOT SATISFIED**.
- **Active phase issue:** GitHub Issue #2.
- **Initial benchmark scope:** frozen; see `docs/BILLING_SCOPE.md` and `docs/DECISIONS.md`.
- **Initial provider scope:** PMHNP/NP and psychiatrist are distinct benchmark provider classes.
- **Workflow scope:** both `PRE_SIGN` and `PRE_SUBMIT`.
- **Minimum v0.1 evidence schema:** frozen in `docs/DATA_MODEL.md` and implemented in `src/claimlens/evidence.py`.
- **Selected Phase 1 model baseline:** `google/medgemma-1.5-4b-it`.
- **Selected Phase 1 runtime:** local Ollama API using model name `medgemma1.5`.
- **Phase 1 progress:** encounter contract, evidence schema, provenance validation, temporal scope, uncertainty/review preservation, deterministic development baseline, Ollama structured-output adapter, and a local baseline CLI are implemented.
- **Phase 1 verification:** the existing 7 focused Phase 1 tests were green before the runtime integration; 3 new isolated Ollama-adapter tests pass for valid structured mapping, untraceable-source rejection, and malformed-output rejection. The actual MedGemma model run is still pending.
- **Remaining Gate 1 work:** install/pull and run MedGemma through Ollama on the development machine, record the model-backed baseline metrics, perform the final affected-file sweep, and then evaluate Gate 1 from evidence.
- **Allowed work:** Phase 1 model-backed baseline execution, failure analysis, additional synthetic development cases, focused tests, and extraction measurement.
- **Blocked work:** Phase 2 rule-engine implementation and later-phase runtime work until Gate 1 is satisfied.

This file is the single repository source of truth for the **current phase/gate and actual component maturity**. `docs/RELEASE_GATES.md` defines advancement requirements. GitHub issues are the work queue but do not override this state.

Status vocabulary: **Not Started → Designed → Built → Integrated → Verified**.

A component is not Verified because code exists. Verification requires explicit behavioral evidence.

| Component | Status | Evidence |
|---|---|---|
| Product scope | Designed | Phase 0 approved; `docs/PRODUCT_SCOPE.md`, `docs/DECISIONS.md` |
| Use cases | Designed | Phase 0 approved; `docs/USE_CASES.md`, `docs/DECISIONS.md` |
| Product requirements | Designed | `docs/PRODUCT_REQUIREMENTS.md` |
| Core architecture | Designed | Phase 0 confirmed; `docs/ARCHITECTURE.md` |
| Data model | Built | Frozen schema implemented in `src/claimlens/evidence.py`; contract tests in `tests/test_evidence.py` |
| Billing scope framework | Designed | `docs/BILLING_SCOPE.md` |
| Rule governance | Designed | Phase 0 confirmed; `docs/RULE_GOVERNANCE.md` |
| Benchmark framework | Designed | Phase 0 confirmed; `docs/BENCHMARK_PLAN.md` |
| Security/data development policy | Designed | Phase 0 confirmed; `docs/SECURITY_AND_DATA.md` |
| Encounter ingestion | Verified | `src/claimlens/encounter.py`; `tests/test_encounter.py` |
| AI evidence extraction | Integrated | Frozen evidence interface plus local Ollama adapter are wired; real MedGemma baseline measurement remains pending |
| Phase 1 development cases | Verified | `data/development_cases/phase1_baseline_cases.json`; `tests/test_evidence.py` |
| Rule engine | Not Started | — |
| Claim compiler | Not Started | — |
| Adversarial auditor | Not Started | — |
| Payer overlays | Not Started | — |
| Frozen benchmark cases | Not Started | — |
| Insurance intake/verification | Not Started / Deferred | — |
| EHR/clearinghouse integration | Not Started / Deferred | — |

Update this file only when the status or work state is supported by repository evidence and applicable release-gate decisions.
