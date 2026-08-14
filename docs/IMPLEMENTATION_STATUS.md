# Implementation Status

## Current work state

- **Current phase:** Phase 2 — First validated billing rule set.
- **Current gate:** Gate 2 — Rule engine baseline.
- **Gate 0 status:** **SATISFIED** — Phase 0 specification freeze completed 2026-08-13.
- **Gate 1 status:** **SATISFIED** — Phase 1 evidence extraction baseline verified 2026-08-13.
- **Gate 2 status:** **NOT SATISFIED — VERIFICATION PENDING**.
- **Active phase issue:** GitHub Issue #3.
- **Initial benchmark scope:** frozen; see `docs/BILLING_SCOPE.md` and `docs/DECISIONS.md`.
- **Initial provider scope:** PMHNP/NP and psychiatrist are distinct benchmark provider classes.
- **Workflow scope:** both `PRE_SIGN` and `PRE_SUBMIT`.
- **Minimum v0.1 evidence schema:** frozen in `docs/DATA_MODEL.md` and implemented in `src/claimlens/evidence.py`.
- **Selected Phase 1 model baseline:** `google/medgemma-1.5-4b-it`.
- **Selected Phase 1 runtime:** local Ollama API using model name `medgemma1.5`.
- **Phase 1 verification:** complete. The full applicable unit suite passed 22/22 tests. The real local MedGemma/Ollama five-case development baseline then matched 5/5 cases (`exact_case_rate = 1.0`) with valid output rate 1.0, review accuracy 1.0, current action precision/recall 1.0/1.0, historical action precision/recall 1.0/1.0, zero unsupported current actions, and zero missed current actions. `docs/BASELINE_RESULTS.md` preserves the initial 1/5 baseline, its replication, the failed 0/5 prompt-v2 experiment, the intermediate guarded 3/5 result, and the final verified 5/5 result.
- **Gate 1 conclusion:** all Gate 1 requirements in `docs/RELEASE_GATES.md` are supported by repository and supplied local-runtime evidence: structured schema, provenance, explicit missing/ambiguous behavior, passing synthetic development cases, and a recorded model-backed baseline.
- **Phase 2 first rule family:** the human owner selected **outpatient evaluation/management for psychiatric medication-management encounters**. The decision is recorded in `docs/DECISIONS.md` and `docs/BILLING_SCOPE.md`.
- **Phase 2 source boundary:** AMA remains the CPT authority. Current official AMA 2026 public materials support a deliberately narrow established-patient medication-review pathway without requiring ClaimLens to reproduce the full CPT MDM table. The human owner explicitly authorized this narrow public-source implementation while preserving the AMA Developer Program/commercial licensing plan for broader CPT-dependent work and distribution.
- **Phase 2 first actual rule:** `OUTPATIENT_EM_ESTABLISHED_99214_STABLE_CHRONIC_MEDICATION_PATHWAY` is implemented in `src/claimlens/rules.py` with primary AMA source metadata. It applies only to an established office/outpatient encounter and supports the narrow public-AMA pathway when at least two explicitly stable chronic conditions are addressed and current medication continuation is documented. An `UNSUPPORTED` result means only that this partial pathway is not demonstrated; it does not claim another MDM or time pathway cannot support 99214.
- **Phase 2 source-specific development cases:** `data/development_cases/phase2_outpatient_em_rule_cases.json` contains synthetic supported, unsupported, review, and not-applicable cases. `tests/test_outpatient_em_rules.py` also exercises duplicate actual rule-ID/source conflict behavior → `REVIEW`.
- **Phase 2 schema review:** no dataclass/schema extension was required. Existing patient status, place of service, condition status/complexity, medication-management, provenance, state, and temporal-scope fields can represent the facts required by this first rule. The normalized `stable_chronic` value is a compact representation of an explicitly supported condition-status fact, not an E/M level or billing conclusion.
- **Phase 2 implementation progress:** `src/claimlens/rules.py` continues to provide the generic deterministic engine boundary and now also exposes the governed factory for the first source-verified outpatient E/M pathway. The generic engine preserves source metadata, lifecycle, explicit `SUPPORTED` / `UNSUPPORTED` / `REVIEW` / `NOT_APPLICABLE` outcomes, provider applicability, evidence/rule traceability, and fail-closed duplicate-rule conflict handling.
- **Phase 2 generic rule-engine verification:** complete. On 2026-08-13 the human owner pulled current `main` through `da1a9d3` and ran `$env:PYTHONPATH="src"; python -m unittest discover -s tests -v`. All 29/29 tests passed, including all seven generic Phase 2 rule-engine contract tests. No Phase 1 regression was observed.
- **Phase 2 prompt audit:** complete. `extract_evidence.txt` explicitly forbids code/service selection; `challenge_claim.txt` and `explain_result.txt` explicitly forbid creating or reinterpreting billing rules from model memory. No prompt contains authoritative E/M level logic.
- **Current Phase 2 completion blocker:** the newly implemented outpatient E/M pathway has not yet completed the required local focused + broader verification on current `main`. The rule lifecycle therefore remains `IMPLEMENTED`, not `TESTED` or `ACTIVE`, and Gate 2 remains open.
- **Allowed work:** run the focused `test_outpatient_em_rules.py` suite, then the full applicable unit suite; inspect individual results; compare against the prior 29/29 checkpoint; if green, update the rule lifecycle/status, Gate 2 conclusion, Issue #3, affected-file sweep, and stale references.
- **Blocked work:** declaring this rule tested/active before verification; declaring Gate 2 satisfied before the new tests are green; treating this one pathway as the complete CPT MDM table; copying/reconstructing restricted CPT content; using secondary summaries as CPT authority; beginning Phase 3 compiler work until Gate 2 is formally satisfied.
- **Non-blocking CPT licensing follow-up:** AMA Developer Program enrollment/access remains planned for broader CPT-dependent development; appropriate commercial/product CPT licensing remains required before commercial CPT-dependent distribution. Neither is claimed as completed.

This file is the single repository source of truth for the **current phase/gate and actual component maturity**. `docs/RELEASE_GATES.md` defines advancement requirements. GitHub issues are the work queue but do not override this state.

Status vocabulary: **Not Started → Designed → Built → Integrated → Verified**.

A component is not Verified because code exists. Verification requires explicit behavioral evidence and every applicable verification checkpoint defined in `AGENTS.md` and the ClaimLens development workflow skill.

| Component | Status | Evidence |
|---|---|---|
| Product scope | Designed | Phase 0 approved; `docs/PRODUCT_SCOPE.md`, `docs/DECISIONS.md` |
| Use cases | Designed | Phase 0 approved; `docs/USE_CASES.md`, `docs/DECISIONS.md` |
| Product requirements | Designed | `docs/PRODUCT_REQUIREMENTS.md` |
| Core architecture | Designed | Phase 0 confirmed; `docs/ARCHITECTURE.md` |
| Data model | Built | Frozen schema implemented in `src/claimlens/evidence.py`; contract tests in `tests/test_evidence.py`; existing E/M fields are sufficient for the first implemented rule |
| Billing scope framework | Designed | `docs/BILLING_SCOPE.md`; first Phase 2 rule family explicitly selected |
| Rule governance | Designed | `docs/RULE_GOVERNANCE.md` |
| Benchmark framework | Designed | `docs/BENCHMARK_PLAN.md` |
| Security/data development policy | Designed | `docs/SECURITY_AND_DATA.md` |
| Encounter ingestion | Verified | `src/claimlens/encounter.py`; `tests/test_encounter.py` |
| AI evidence extraction | Verified | Local Ollama/MedGemma path runs end-to-end; 22/22 applicable unit tests passed and the final real five-case Phase 1 development run matched 5/5 with all reported extraction/review precision/recall metrics at 1.0 and zero unsupported/missed current actions |
| Phase 1 development cases | Verified | `data/development_cases/phase1_baseline_cases.json`; final model-backed run matched all 5/5 expected cases; prior failed/partial iterations remain preserved in `docs/BASELINE_RESULTS.md` |
| Rule engine | Verified | Generic deterministic rule/source/result/lifecycle/conflict boundary implemented in `src/claimlens/rules.py`; all seven generic Phase 2 contract tests passed as part of the prior 29/29 local suite |
| Outpatient E/M medication-management rules | Built / Verification Pending | First actual AMA-backed pathway implemented in `src/claimlens/rules.py`; source definition in `rules/OUTPATIENT_EM_MEDICATION_MANAGEMENT.md`; synthetic cases and focused tests added; current-main local verification still required |
| Claim compiler | Not Started | — |
| Adversarial auditor | Not Started | — |
| Payer overlays | Not Started | — |
| Frozen benchmark cases | Not Started | — |
| Insurance intake/verification | Not Started / Deferred | — |
| EHR/clearinghouse integration | Not Started / Deferred | — |

Update this file only when the status or work state is supported by repository evidence and applicable release-gate decisions.
