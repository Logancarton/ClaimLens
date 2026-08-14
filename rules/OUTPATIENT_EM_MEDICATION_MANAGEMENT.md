# Outpatient E/M Medication Management — Phase 2 Source Review

Status: **Source review in progress; generic rule-engine boundary verified; no detailed CPT level-selection table is activated here.**

Selected service family: outpatient evaluation/management for psychiatric medication-management encounters.

Human selection date: 2026-08-13.
Source verification date: 2026-08-13.
Generic rule-engine verification date: 2026-08-13.

## Purpose

This file records the authoritative-source boundary for the first Gate 2 rule family before executable billing logic is added. It is not a substitute for the CPT code set and does not make model output, secondary summaries, or payer guidance into coding authority.

## Authoritative source set identified

### American Medical Association — CPT E/M authority

Primary entry points reviewed:

- CPT Evaluation and Management: https://www.ama-assn.org/practice-management/cpt/cpt-evaluation-and-management
- CPT Evaluation and Management revisions FAQs: https://www.ama-assn.org/practice-management/cpt/cpt-evaluation-and-management-em-revisions-faqs
- CPT licensing resources: https://www.ama-assn.org/practice-management/cpt/cpt-licensing-frequently-asked-questions-faqs

The AMA is the authority for CPT coding content. Its current public E/M materials confirm the modern office/outpatient framework in which visit level may be selected using medical decision making or total practitioner/QHP time, while medically appropriate history/examination remains clinically relevant but is not itself the level-selection mechanism.

Detailed CPT code descriptors, the full MDM table, code-level time thresholds, and other restricted CPT content are copyrighted/licensed. ClaimLens must not copy restricted CPT content into Git or treat an AI/secondary paraphrase as a replacement for current CPT authority.

### Centers for Medicare & Medicaid Services — current Medicare E/M guidance

Primary source reviewed:

- CMS `MLN006764 — Evaluation and Management Services`, May 2026: https://www.cms.gov/files/document/mln006764-evaluation-management-services.pdf
- CMS E/M guidance landing page: https://www.cms.gov/medicare/payment/fee-schedules/physician/evaluation-management-visits

Source propositions relevant to later Medicare rules include:

- Office/outpatient E/M code choice depends on patient type, setting, and level of service.
- For Medicare office/outpatient E/M, patient type is new or established based on prior professional services with the practitioner/same-specialty same-group context described by CMS.
- For most E/M visit families, level selection uses MDM or time rather than history/exam as level selectors.
- When time supports the E/M level, the record must document the time using a total-time or start/stop representation described by CMS.
- Medical necessity remains a governing Medicare payment condition; a higher level should not be selected when a lower level is the appropriate medically necessary service.
- CMS explicitly directs users to the AMA E/M Services Guidelines for the detailed MDM breakdown.

These Medicare propositions are not silently generalized into every commercial payer or Medicaid program.

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

- Build or refine generic deterministic rule-engine structures required by `docs/RULE_GOVERNANCE.md`.
- Record source/version/effective-date/verification metadata.
- Implement and test propositions that can be supported from public authoritative material without reproducing restricted CPT content.
- Create synthetic supported, unsupported, ambiguous, and rule-conflict cases.
- Fail closed to `REVIEW` when applicability or authoritative rule detail is unresolved.

## What is not authorized yet

Agents must not:

- Reconstruct the detailed CPT MDM table from memory.
- Copy CPT descriptors or code-level time thresholds into the repository without appropriate rights.
- Use a payer blog, coding blog, AI answer, or model prompt as the authority for base CPT rules.
- Infer PMHNP-versus-psychiatrist differences unless an authoritative rule establishes that provider class is material.
- Skip base coding logic and treat Medicare, AHCCCS, or a commercial payer overlay as the universal rule set.

## Next implementation boundary

The generic deterministic rule engine is now verified. The next Gate 2 step is to define and test actual outpatient E/M rule IDs from authorized authoritative source detail. Full code-level E/M selection remains blocked wherever it requires restricted CPT detail until the human owner confirms appropriate CPT rights/access or otherwise explicitly resolves the source/licensing path.
