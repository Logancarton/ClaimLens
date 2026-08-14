# Implementation Status

## Current work state

- **Current phase:** Phase 2 — First validated billing rule set.
- **Current gate:** Gate 2 — Rule engine baseline.
- **Gate 0 status:** **SATISFIED** — Phase 0 specification freeze completed 2026-08-13.
- **Gate 1 status:** **SATISFIED** — Phase 1 evidence extraction baseline verified 2026-08-13.
- **Gate 2 status:** **NOT SATISFIED**.
- **Active phase issue:** GitHub Issue #3.
- **Initial benchmark scope:** frozen; see `docs/BILLING_SCOPE.md` and `docs/DECISIONS.md`.
- **Initial provider scope:** PMHNP/NP and psychiatrist are distinct benchmark provider classes.
- **Workflow scope:** both `PRE_SIGN` and `PRE_SUBMIT`.
- **Minimum v0.1 evidence schema:** frozen in `docs/DATA_MODEL.md` and implemented in `src/claimlens/evidence.py`.
- **Selected Phase 1 model baseline:** `google/medgemma-1.5-4b-it`.
- **Selected Phase 1 runtime:** local Ollama API using model name `medgemma1.5`.
- **Phase 1 verification:** complete. The full applicable unit suite passed 22/22 tests. The real local MedGemma/Ollama five-case development baseline then matched 5/5 cases (`exact_case_rate = 1.0`) with valid output rate 1.0, review accuracy 1.0, current action precision/recall 1.0/1.0, historical action precision/recall 1.0/1.0, zero unsupported current actions, and zero missed current actions. `docs/BASELINE_RESULTS.md` preserves the initial 1/5 baseline, its replication, the failed 0/5 prompt-v2 experiment, the intermediate guarded 3/5 result, and the final verified 5/5 result.
- **Gate 1 conclusion:** all Gate 1 requirements in `docs/RELEASE_GATES.md` are supported by repository and supplied local-runtime evidence: structured schema, provenance, explicit missing/ambiguous behavior, passing synthetic development cases, and a recorded model-backed baseline.
- **Phase 2 entry state:** Phase 2 is active, but substantive rule-engine implementation is blocked until the human owner selects which already-approved outpatient psychiatric service family should be implemented first. That selection is a human decision under `.agents/AUTONOMY_POLICY.md`; the agent must not choose it silently.
- **Allowed work:** Phase 2 repository review, preparation that does not choose or reinterpret billing scope, and implementation/testing after the first service family is explicitly selected and authoritative sources are identified.
- **Blocked work:** choosing the first service family on the user's behalf; implementing authoritative billing logic before that selection/source work; Phase 3 compiler implementation and later-phase runtime work until Gate 2 is satisfied.

This file is the single repository source of truth for the **current phase/gate and actual component maturity**. `docs/RELEASE_GATES.md` defines advancement requirements. GitHub issues are the work queue but do not override this state.

Status vocabulary: **Not Started → Designed → Built → Integrated → Verified**.

A component is not Verified because code exists. Verification requires explicit behavioral evidence and every applicable verification checkpoint defined in `AGENTS.md` and the ClaimLens development workflow skill.

| Component | Status | Evidence |
|---|---|---|
| Product scope | Designed | Phase 0 approved; `docs/PRODUCT_SCOPE.md`, `docs/DECISIONS.md` |
| Use cases | Designed | Phase 0 approved; `docs/USE_CASES.md`, `docs/DECISIONS.md` |
| Product requirements | Designed | `docs/PRODUCT_REQUIREMENTS.md` |
| Core architecture | Designed | Phase 0 confirmed; `docs/ARCHITECTURE.md` |
| Data model | Built | Frozen schema implemented in `src/claimlens/evidence.py`; contract tests in `tests/test_evidence.py`; medication-action vocabulary clarified in `docs/DATA_MODEL.md` |
| Billing scope framework | Designed | `docs/BILLING_SCOPE.md` |
| Rule governance | Designed | Phase 0 confirmed; `docs/RULE_GOVERNANCE.md` |
| Benchmark framework | Designed | Phase 0 confirmed; `docs/BENCHMARK_PLAN.md` |
| Security/data development policy | Designed | Phase 0 confirmed; `docs/SECURITY_AND_DATA.md` |
| Encounter ingestion | Verified | `src/claimlens/encounter.py`; `tests/test_encounter.py` |
| AI evidence extraction | Verified | Local Ollama/MedGemma path runs end-to-end; 22/22 applicable unit tests passed and the final real five-case Phase 1 development run matched 5/5 with all reported extraction/review precision/recall metrics at 1.0 and zero unsupported/missed current actions |
| Phase 1 development cases | Verified | `data/development_cases/phase1_baseline_cases.json`; final model-backed run matched all 5/5 expected cases; prior failed/partial iterations remain preserved in `docs/BASELINE_RESULTS.md` |
| Rule engine | Not Started | Phase 2 current; first service family requires explicit human selection before implementation |
| Claim compiler | Not Started | — |
| Adversarial auditor | Not Started | — |
| Payer overlays | Not Started | — |
| Frozen benchmark cases | Not Started | — |
| Insurance intake/verification | Not Started / Deferred | — |
| EHR/clearinghouse integration | Not Started / Deferred | — |

Update this file only when the status or work state is supported by repository evidence and applicable release-gate decisions.
