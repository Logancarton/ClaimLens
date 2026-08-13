# Implementation Status

## Current work state

- **Current phase:** Phase 0 — Freeze ClaimLens v0.1 specification.
- **Current gate:** Gate 0 — Specification frozen enough to build.
- **Gate status:** **NOT SATISFIED**.
- **Active phase issue:** GitHub Issue #1.
- **Initial benchmark scope:** selected; see `docs/BILLING_SCOPE.md` and `docs/DECISIONS.md`.
- **Initial provider scope:** PMHNP/NP and psychiatrist are selected as distinct benchmark provider classes.
- **Minimum v0.1 evidence schema:** defined in `docs/DATA_MODEL.md` and aligned with `docs/ARCHITECTURE.md`.
- **Allowed work:** product/specification review, benchmark design, synthetic fixture organization, rule-source planning, and other Phase 0 work.
- **Blocked work:** substantive Phase 1 runtime implementation, model integration, evidence-extractor implementation, rule-engine implementation, compiler/auditor implementation, payer overlays, and deferred integrations.

This file is the single repository source of truth for the **current phase/gate and actual component maturity**. `docs/RELEASE_GATES.md` defines advancement requirements. GitHub issues are the work queue but do not override this state.

Status vocabulary: **Not Started → Designed → Built → Integrated → Verified**.

A component is not Verified because code exists. Verification requires explicit behavioral evidence.

| Component | Status | Evidence |
|---|---|---|
| Product scope | Designed | `docs/PRODUCT_SCOPE.md` |
| Use cases | Designed | `docs/USE_CASES.md` |
| Product requirements | Designed | `docs/PRODUCT_REQUIREMENTS.md` |
| Core architecture | Designed | `docs/ARCHITECTURE.md` |
| Data model | Designed | `docs/DATA_MODEL.md` |
| Billing scope framework | Designed | `docs/BILLING_SCOPE.md` |
| Rule governance | Designed | `docs/RULE_GOVERNANCE.md` |
| Benchmark framework | Designed | `docs/BENCHMARK_PLAN.md` |
| Security/data development policy | Designed | `docs/SECURITY_AND_DATA.md` |
| Encounter ingestion | Not Started | — |
| AI evidence extraction | Not Started | — |
| Rule engine | Not Started | — |
| Claim compiler | Not Started | — |
| Adversarial auditor | Not Started | — |
| Payer overlays | Not Started | — |
| Benchmark cases | Not Started | — |
| Insurance intake/verification | Not Started / Deferred | — |
| EHR/clearinghouse integration | Not Started / Deferred | — |

Update this file only when the status or work state is supported by repository evidence and applicable release-gate decisions.
