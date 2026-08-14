# Outpatient E/M Medication Management — Phase 2 Rule Source

Status: **One narrow public-AMA outpatient E/M pathway is implemented; focused/full local verification pending. The full CPT MDM table is not reproduced or implemented.**

Selected service family: outpatient evaluation/management for psychiatric medication-management encounters.

Human selection date: 2026-08-13.
Licensing-path decision date: 2026-08-13.
Public-source implementation decision date: 2026-08-13.
Source verification date: 2026-08-13.
Generic rule-engine verification date: 2026-08-13.

## Purpose

This file is the human-reviewable authoritative source definition for the first Gate 2 service family. It records the exact proposition ClaimLens is allowed to implement, its limits, and the primary sources supporting it. It is not a substitute for the CPT code set and does not reproduce the detailed CPT MDM table.

## Authoritative source set

### American Medical Association — CPT authority

Primary sources used for the first implemented pathway:

- AMA STEPS Forward, **Simplified Outpatient Documentation and Coding**, published online January 20, 2026: https://edhub.ama-assn.org/steps-forward/module/2844245
- AMA public guidance for CPT 99214, updated January 26, 2026: https://www.ama-assn.org/practice-management/cpt/cpt-code-99214-established-patient-office-visit-30-39-minutes
- AMA CPT Evaluation and Management overview, updated January 26, 2026: https://www.ama-assn.org/practice-management/cpt/cpt-evaluation-and-management
- AMA CPT Evaluation and Management revisions FAQs, updated January 26, 2026: https://www.ama-assn.org/practice-management/cpt/cpt-evaluation-and-management-em-revisions-faqs

AMA remains the CPT coding authority. The public 2026 AMA outpatient toolkit states that office/outpatient level selection may be based on MDM or total date-of-service time and that MDM uses three elements, with the overall MDM level determined by the highest two of the three elements. The same AMA toolkit and related AMA material provide a public medication-review example in which two stable chronic conditions plus medication management meet moderate MDM, and AMA's public 99214 page identifies 99214 as the established-patient office/outpatient service associated with moderate MDM.

ClaimLens implements only that narrow public proposition. It does not reconstruct the full MDM table from memory and does not copy CPT descriptors, the complete MDM grid, or code-level time tables into the repository.

### Centers for Medicare & Medicaid Services — Medicare-specific context

Primary source reviewed:

- CMS `MLN006764 — Evaluation and Management Services`, May 2026: https://www.cms.gov/files/document/mln006764-evaluation-management-services.pdf
- CMS E/M landing page: https://www.cms.gov/medicare/payment/fee-schedules/physician/evaluation-management-visits

CMS material remains Medicare-specific. It may support later Medicare propositions, but it is not being used as a substitute for base CPT authority and is not silently generalized to Medicaid or commercial payers.

## Implemented rule

### Rule ID

`OUTPATIENT_EM_ESTABLISHED_99214_STABLE_CHRONIC_MEDICATION_PATHWAY`

### Scope

- Service family: `OUTPATIENT_EM_MEDICATION_MANAGEMENT`.
- Base coding jurisdiction: `CPT_BASE`.
- Established patient only.
- Office/outpatient setting only.
- PMHNP/NP and psychiatrist follow the same rule path; this rule does not invent a provider-class difference.

### Source-verified proposition

The rule evaluates a deliberately narrow pathway demonstrated directly by public AMA education:

1. The encounter is an established-patient office/outpatient encounter.
2. At least two chronic conditions addressed in the current encounter are explicitly supported as stable.
3. Current medication continuation is explicitly documented.
4. When all three facts are supported, this specific pathway supports moderate MDM / 99214.

The normalized value `stable_chronic` is only a compact representation of an explicitly supported condition-status fact. It is not itself an E/M level or billing conclusion.

The first implementation intentionally recognizes `continue` as the medication-management action because that is the action directly demonstrated by the public AMA medication-review example. Broader prescription-drug-management actions must be added only when the authoritative proposition supporting them is recorded and tested.

### Fail-closed behavior

- Unknown patient status → `REVIEW`.
- Non-established patient → `NOT_APPLICABLE` for this rule.
- Unknown office/outpatient setting → `REVIEW`.
- Non-office/outpatient setting → `NOT_APPLICABLE`.
- Material ambiguity, contradiction, or unclear temporal scope in condition status or medication management → `REVIEW`.
- Fewer than two explicitly stable chronic conditions, or no qualifying current medication continuation → `UNSUPPORTED` **for this pathway only**.
- Duplicate definitions with this same rule ID remain a rule-source conflict and the generic engine returns `REVIEW`.

An `UNSUPPORTED` result from this rule must never be interpreted as proof that 99214 is globally unsupported. Other MDM and time pathways are not yet represented by this narrow rule.

## Executable implementation

The governed metadata and deterministic evaluator are implemented in `src/claimlens/rules.py` through `outpatient_em_medication_management_rules()`.

Synthetic development cases are stored in:

`data/development_cases/phase2_outpatient_em_rule_cases.json`

Focused behavior tests are stored in:

`tests/test_outpatient_em_rules.py`

The cases cover:

- source-supported pathway;
- explicitly unsupported narrow pathway;
- material ambiguity routed to review;
- non-applicability for a new patient; and
- duplicate actual rule ID/source-conflict behavior failing closed to review.

## Evidence-schema assessment

No dataclass/schema extension is required for this first rule. Existing fields already carry every fact needed:

- `Encounter.metadata.patient_status` for new/established/unknown status;
- `Encounter.metadata.place_of_service` for explicit setting;
- `ConditionAddressed.status_complexity` for explicitly supported condition-status characteristics;
- `EvaluationManagementEvidence.problems_addressed` for current problems actually addressed;
- `EvaluationManagementEvidence.management_activities` / `MedicationActivity` for current medication management;
- shared evidence state, provenance, and temporal scope for fail-closed uncertainty handling.

The evidence extractor is not allowed to manufacture `stable_chronic` from a diagnosis list or infer medication continuation from medication-list presence. Those facts require actual source support.

## AMA development/product licensing path

The human owner previously selected the AMA CPT Developer Program as ClaimLens' intended authorized development/testing path and plans to obtain the appropriate commercial/product CPT license before CPT-dependent functionality is distributed commercially.

That plan remains in force. Developer Program enrollment/access and commercial/product licensing are not claimed as completed.

The current Phase 2 implementation uses only a narrowly paraphrased proposition that AMA itself publishes openly in its current educational material, with source references retained. Public accessibility does not waive AMA copyright or future product-licensing requirements. ClaimLens therefore continues to avoid committing the full CPT data set, detailed MDM grid, CPT descriptors, or comprehensive code/time tables.

Any executed AMA agreement controls later access, storage, transformation, display, distribution, and AI-use permissions and supersedes repository summaries where they differ.

## Current verification boundary

Implementation is complete enough for testing, but the new rule is not yet marked `TESTED` or `ACTIVE` and Gate 2 is not yet satisfied because the required local verification has not been supplied.

Required focused verification:

`$env:PYTHONPATH="src"; python -m unittest discover -s tests -p "test_outpatient_em_rules.py" -v`

Required broader verification:

`$env:PYTHONPATH="src"; python -m unittest discover -s tests -v`

After both are green and individual results are inspected, ClaimLens can evaluate Gate 2 against `docs/RELEASE_GATES.md`, synchronize the rule lifecycle/status/Issue #3, and only then determine whether Phase 3 may begin.
