# Outpatient E/M Medication Management — Phase 2 Source Review

Status: **Public-authority source review and schema-readiness review complete through the current access boundary; AMA CPT Developer Program path selected; Developer Program enrollment/access pending; no detailed CPT level-selection table is activated here.**

Selected service family: outpatient evaluation/management for psychiatric medication-management encounters.

Human selection date: 2026-08-13.
Licensing-path decision date: 2026-08-13.
Source verification date: 2026-08-13.
Generic rule-engine verification date: 2026-08-13.

## Purpose

This file records the authoritative-source boundary for the first Gate 2 rule family before executable billing logic is added. It is not a substitute for the CPT code set and does not make model output, secondary summaries, or payer guidance into coding authority.

## Authoritative source set identified

### American Medical Association — CPT E/M authority

Primary entry points reviewed:

- CPT Evaluation and Management: https://www.ama-assn.org/practice-management/cpt/cpt-evaluation-and-management
- CPT Evaluation and Management revisions FAQs: https://www.ama-assn.org/practice-management/cpt/cpt-evaluation-and-management-em-revisions-faqs
- CPT Developer Program: https://www.ama-assn.org/practice-management/cpt/cpt-developer-program
- CPT licensing FAQs: https://www.ama-assn.org/practice-management/cpt/cpt-licensing-frequently-asked-questions-faqs

The AMA is the authority for CPT coding content. Its current public E/M materials confirm the modern office/outpatient framework in which visit level may be selected using medical decision making or total practitioner/QHP time, while medically appropriate history/examination remains clinically relevant but is not itself the level-selection mechanism.

Detailed CPT code descriptors, the full MDM table, code-level time thresholds, and other restricted CPT content are copyrighted/licensed. ClaimLens must not copy restricted CPT content into Git or treat an AI/secondary paraphrase as a replacement for current CPT authority.

### AMA development and product licensing path — HUMAN DECISION RESOLVED

The human owner explicitly decided on 2026-08-13 that ClaimLens will use the **AMA CPT Developer Program** as its authorized development/testing access path and will plan to obtain the appropriate commercial/product CPT license before CPT-dependent functionality is distributed commercially.

Current official AMA materials reviewed on 2026-08-13 state that:

- the CPT Developer Program is available for new organizations to access CPT content for building and testing innovations under a royalty-free development license;
- the program requires registration/sign-up and provides developer access to current CPT content through AMA delivery tools;
- electronic products that use, reference, display, develop against, maintain, distribute, or otherwise rely on CPT content require an appropriate license for the actual use case;
- AI-related CPT use is governed by the applicable AMA license terms/addendum and any required product approvals;
- the current general AMA licensing FAQ states that training or fine-tuning AI models on the CPT Standard Data File is prohibited, while retrieval-based use may be permitted only within the applicable license/product-approval terms; and
- an executed agreement controls actual permissions and supersedes repository summaries or general FAQ language when they differ.

Therefore:

- The **policy choice is settled**: ClaimLens will use the Developer Program for authorized build/test access.
- The **external access step is not verified**: this repository does not claim that ClaimLens has enrolled, obtained portal access, executed a development agreement, or obtained a commercial/product CPT license.
- A development license must not be treated as automatic authorization for commercial distribution, every AI use case, public/open-model ingestion, or repository storage of licensed CPT detail.
- The commercial/product license remains a required future distribution step and is not claimed as obtained.

### Centers for Medicare & Medicaid Services — current Medicare E/M guidance

Primary source reviewed:

- CMS `MLN006764 — Evaluation and Management Services`, May 2026: https://www.cms.gov/files/document/mln006764-evaluation-management-services.pdf
- CMS E/M guidance landing page: https://www.cms.gov/medicare/payment/fee-schedules/physician/evaluation-management-visits

Public CMS propositions relevant to later Medicare rules include:

- Office/outpatient E/M code choice depends on patient type, setting, and level of service.
- For Medicare office/outpatient E/M, patient type is new or established based on prior professional services with the practitioner/same-specialty same-group context described by CMS.
- For most E/M visit families, level selection uses MDM or time rather than history/exam as level selectors.
- When time supports the E/M level, the record must document the time using a total-time or start/stop representation described by CMS.
- Medical necessity remains a governing Medicare payment condition; a higher level should not be selected when a lower level is the appropriate medically necessary service.
- CMS explicitly directs users to the AMA E/M Services Guidelines for the detailed MDM breakdown.

These are Medicare-specific propositions. They are not silently generalized into every commercial payer, Medicaid program, or universal base CPT rule.

## Schema and architecture readiness assessment

The current ClaimLens encounter/evidence contracts can represent the public-source facts identified so far without a schema change:

- Patient type is represented by `Encounter.metadata.patient_status` (`NEW`, `ESTABLISHED`, `UNKNOWN`).
- Rendering provider class is represented by `Encounter.metadata.provider_class`.
- Place/setting information can be carried by `Encounter.metadata.place_of_service` when explicitly supplied.
- Problems addressed are represented by `EvaluationManagementEvidence.problems_addressed` / `ConditionAddressed`.
- Data work is represented by `EvaluationManagementEvidence.data_activities` / `DataActivity`.
- Management activity is represented by `EvaluationManagementEvidence.management_activities` / `MedicationActivity`.
- Practitioner time is represented by `EvaluationManagementEvidence.practitioner_time_minutes`.
- Time-documentation form is represented by `EvaluationManagementEvidence.time_documentation_type`.
- Provenance, state, and temporal scope remain available through the shared evidence contract.

No source-justified schema extension is required at this public-source boundary. Detailed authorized CPT E/M review may later demonstrate that another fact must be represented; ClaimLens will add such a field only after the authoritative source proves the need rather than pre-encoding remembered billing logic.

A second architecture constraint matters: the active base rule path intentionally has no payer/program identity because payer overlays are deferred. CMS May 2026 guidance is Medicare-specific. ClaimLens therefore must **not** activate CMS-only propositions as universal base CPT rules simply because those propositions are publicly accessible. Doing so would collapse the base-rule/payer-overlay boundary defined in `docs/ARCHITECTURE.md` and `docs/BILLING_SCOPE.md`.

This is why no payer infrastructure or Medicare-specific executable rule set is being added merely to work around the current AMA access boundary.

## What can be encoded from current public authority

Current public sources are sufficient to define high-level guardrails and source metadata such as:

- office/outpatient E/M selection depends on the appropriate patient type, setting, and service level;
- history/exam volume is not itself the office/outpatient level-selection mechanism;
- a time-based path requires documented time in an accepted representation;
- Medicare medical necessity can constrain payment for an E/M level; and
- Medicare patient-status and setting propositions are payer/program-specific.

Those propositions are useful for source review and later rule challenges, but they are **not sufficient to implement a complete base outpatient E/M level-selection rule set** without the detailed current CPT E/M authority. CMS explicitly points detailed MDM interpretation back to AMA guidance, and code-level thresholds/detail remain within the CPT licensing boundary.

Accordingly, adding synthetic known-answer cases for actual outpatient E/M level selection before authorized CPT access would force ClaimLens either to invent expected answers or to reconstruct restricted detail from memory. Both are prohibited.

## Verified generic rule-engine boundary

On 2026-08-13, after pulling current `main` through `da1a9d3`, the human owner ran:

`$env:PYTHONPATH="src"; python -m unittest discover -s tests -v`

All 29/29 tests passed, including all seven generic Phase 2 rule-engine contract tests. The verified mechanics now include:

- mandatory rule/source metadata;
- explicit `SUPPORTED`, `UNSUPPORTED`, `REVIEW`, and `NOT_APPLICABLE` outcomes;
- source and evidence traceability;
- provider applicability;
- fail-closed duplicate-rule-ID conflict handling;
- protection against using a source-verified but unimplemented rule as billing support; and
- rejection of cross-encounter evidence.

This verifies the generic rule-engine boundary only. It does not verify any actual outpatient E/M level-selection rule.

## What is authorized now

Agents may:

- Maintain the generic deterministic rule-engine structures required by `docs/RULE_GOVERNANCE.md`.
- Record public source/version/effective-date/verification metadata.
- Continue public-authority source review without reproducing restricted CPT content.
- Re-check the existing evidence schema against newly authorized source detail once Developer Program access is available.
- Prepare non-proprietary test scaffolding that does not invent actual CPT level expectations.
- Fail closed to `REVIEW` when applicability or authoritative rule detail is unresolved.

## What is not authorized yet

Agents must not:

- Reconstruct the detailed CPT MDM table from memory.
- Copy CPT descriptors or code-level time thresholds into the repository without verified rights under the applicable agreement.
- Use a payer blog, coding blog, AI answer, or model prompt as the authority for base CPT rules.
- Infer PMHNP-versus-psychiatrist differences unless an authoritative rule establishes that provider class is material.
- Activate Medicare-specific CMS guidance as universal base CPT logic.
- Add payer-selection infrastructure solely to bypass the current CPT source-access boundary.
- Treat the Developer Program decision as proof that enrollment/access or commercial licensing has already occurred.

## Next implementation boundary

The generic deterministic rule engine is verified, the official AMA development/licensing path is confirmed, the human owner selected that path, and the current schema is ready for the publicly identified E/M facts without extension.

The next required step is external: **register/enroll ClaimLens in the AMA CPT Developer Program, obtain the applicable development access/agreement, and review the governing terms.**

After that access is verified, Phase 2 can resume by reading the authorized current CPT E/M material, defining the smallest source-verified base outpatient E/M rule IDs and metadata, extending the schema only if an authoritative requirement cannot be represented, adding synthetic supported/unsupported/review/conflict cases from those verified rules, implementing deterministic evaluations, and running focused plus full verification.

Gate 2 remains **NOT SATISFIED** until that actual service-family rule evidence exists and the required deterministic tests are green.
