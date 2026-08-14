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
- **Phase 2 first rule family:** the human owner selected **outpatient evaluation/management for psychiatric medication-management encounters**. The decision is recorded in `docs/DECISIONS.md` and `docs/BILLING_SCOPE.md`.
- **Phase 2 source review:** current authoritative entry points are recorded in `rules/OUTPATIENT_EM_MEDICATION_MANAGEMENT.md`. AMA is the CPT coding authority. Current CMS May 2026 E/M guidance provides Medicare-specific propositions but explicitly directs detailed MDM interpretation back to AMA E/M guidance. On 2026-08-13 the current AMA Developer Program and licensing materials were re-checked: the Developer Program offers new organizations a royalty-free development license for CPT build/test work, while electronic-product and AI uses remain subject to the applicable AMA license terms/product approvals.
- **Phase 2 CPT access decision:** resolved. The human owner explicitly selected the AMA CPT Developer Program as ClaimLens' authorized development/testing path and plans to obtain the appropriate commercial/product CPT license before CPT-dependent functionality is distributed commercially. This does **not** mean Developer Program enrollment, CPT portal access, a development agreement, or a commercial/product CPT license has already been completed or obtained.
- **Phase 2 schema/architecture readiness review:** complete through the public-source boundary. The current encounter/evidence contracts already represent the publicly identified E/M inputs: patient status, provider class, place of service, problems addressed, data activities, management activities, practitioner time, and time-documentation type. No source-justified schema extension is required yet. Detailed CPT access may reveal additional required facts later; ClaimLens will not pre-encode them from memory. CMS-only propositions remain Medicare-specific, and the current base rule path intentionally has no active payer/program identity because payer overlays are deferred. Therefore CMS rules must not be activated as universal base CPT logic merely to bypass the AMA access boundary.
- **Phase 2 implementation progress:** `src/claimlens/rules.py` implements the generic deterministic rule-engine boundary with rule/source metadata, lifecycle states, explicit `SUPPORTED` / `UNSUPPORTED` / `REVIEW` / `NOT_APPLICABLE` outcomes, provider applicability, traceability, and fail-closed duplicate-rule conflict handling. `tests/test_rules.py` contains focused contract tests for these mechanics. This is generic engine infrastructure, not yet a completed outpatient E/M billing rule set.
- **Phase 2 generic rule-engine verification:** complete. On 2026-08-13 the human owner pulled current `main` through `da1a9d3` and ran `$env:PYTHONPATH="src"; python -m unittest discover -s tests -v`. All 29/29 tests passed, including all seven Phase 2 generic rule-engine contract tests. No regression was observed in Phase 1 encounter/evidence/Ollama tests.
- **Phase 2 prompt audit:** complete. `extract_evidence.txt` explicitly forbids code/service selection; `challenge_claim.txt` and `explain_result.txt` explicitly forbid creating or reinterpreting billing rules from model memory. No prompt contains authoritative E/M level logic.
- **Current Phase 2 blocker:** external AMA access, not an unresolved product decision. The human owner must register/enroll ClaimLens in the AMA CPT Developer Program, obtain the applicable development access/agreement, and review the governing terms. Until that is verified, detailed base CPT MDM/level-selection logic cannot be source-verified safely. The separate commercial/product CPT license remains required before commercial CPT-dependent distribution and is not claimed as obtained.
- **Allowed work:** continue public-authority source/version review and generic rule-engine maintenance that does not reproduce restricted CPT content; after Developer Program access is verified, inspect the authorized current CPT E/M source, define the smallest source-verified outpatient E/M rule set, extend the schema only if that source demonstrates a real gap, then add synthetic known-answer cases and deterministic tests.
- **Blocked work:** copying or reconstructing restricted CPT detail without verified rights/access; using Medicare-specific CMS propositions as universal base CPT rules; substituting remembered/secondary billing logic for CPT authority; declaring Gate 2 satisfied before source-verified service rules and deterministic tests are green; Phase 3 compiler implementation until Gate 2 is satisfied.

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
| Billing scope framework | Designed | `docs/BILLING_SCOPE.md`; first Phase 2 rule family explicitly selected |
| Rule governance | Designed | Phase 0 confirmed; `docs/RULE_GOVERNANCE.md` |
| Benchmark framework | Designed | Phase 0 confirmed; `docs/BENCHMARK_PLAN.md` |
| Security/data development policy | Designed | Phase 0 confirmed; `docs/SECURITY_AND_DATA.md` |
| Encounter ingestion | Verified | `src/claimlens/encounter.py`; `tests/test_encounter.py` |
| AI evidence extraction | Verified | Local Ollama/MedGemma path runs end-to-end; 22/22 applicable unit tests passed and the final real five-case Phase 1 development run matched 5/5 with all reported extraction/review precision/recall metrics at 1.0 and zero unsupported/missed current actions |
| Phase 1 development cases | Verified | `data/development_cases/phase1_baseline_cases.json`; final model-backed run matched all 5/5 expected cases; prior failed/partial iterations remain preserved in `docs/BASELINE_RESULTS.md` |
| Rule engine | Verified | Generic deterministic rule/source/result/lifecycle/conflict boundary implemented in `src/claimlens/rules.py`; all seven Phase 2 generic contract tests passed as part of the 29/29 local suite on 2026-08-13 |
| Outpatient E/M medication-management rules | Designed / Source Review / Access Pending | First Phase 2 family selected; authoritative source and licensing boundary plus schema-readiness assessment recorded in `rules/OUTPATIENT_EM_MEDICATION_MANAGEMENT.md`; Developer Program path selected but enrollment/access not yet verified; detailed CPT-dependent implementation not yet authorized/completed |
| Claim compiler | Not Started | — |
| Adversarial auditor | Not Started | — |
| Payer overlays | Not Started | — |
| Frozen benchmark cases | Not Started | — |
| Insurance intake/verification | Not Started / Deferred | — |
| EHR/clearinghouse integration | Not Started / Deferred | — |

Update this file only when the status or work state is supported by repository evidence and applicable release-gate decisions.
