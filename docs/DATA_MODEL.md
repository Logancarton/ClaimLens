# Data Model

This file defines what ClaimLens knows before implementation choices define how it is stored.

The v0.1 evidence schema captures observable encounter facts needed by the selected outpatient psychiatric benchmark scope. It does **not** encode billing conclusions. Deterministic rules decide what those facts support.

## Shared evidence contract

Every extracted evidence object must be able to carry:

- `state` — `PRESENT`, `ABSENT`, `AMBIGUOUS`, `CONTRADICTORY`, or `NOT_APPLICABLE`.
- `source` — exact provenance back to note text or explicitly supplied encounter metadata.
- `normalized_value` — optional structured representation of what the source says.
- `temporal_scope` — `CURRENT_ENCOUNTER`, `HISTORICAL`, or `UNCLEAR` when timing matters.
- `confidence` — optional model interpretation confidence; never billing authority.

`temporal_scope` gives ClaimLens a place to represent current versus historical evidence. It does not settle the still-open policy question of how copied-forward text is detected.

## Core objects

### Encounter
Raw note plus explicitly supplied encounter metadata.

Minimum v0.1 metadata:

- Encounter/source identifier.
- Date of service when supplied.
- Raw note text.
- Patient status when supplied and relevant to later rules (`NEW`, `ESTABLISHED`, `UNKNOWN`).
- Rendering provider type/credential when supplied; PMHNP/NP and psychiatrist identities remain distinct.
- Place of service when supplied.

Encounter metadata is preserved as supplied; the evidence extractor must not infer provider credential, patient status, or place of service from unsupported text.

### EvidenceItem
A single billing-relevant fact extracted from the encounter using the shared evidence contract.

### ConditionAddressed
A problem/condition actually addressed during the encounter, distinct from diagnoses merely present on a problem list.

Minimum fields:

- Condition/problem reference or normalized label.
- Evidence that it was addressed in the current encounter.
- Status/complexity characteristics explicitly supported by the record.
- Associated assessment/plan evidence references.

### DataActivity
An atomic data-review or data-analysis activity documented in the encounter.

Minimum fields:

- Activity type.
- Object/source involved when stated.
- Result or interpretation when stated.
- Evidence provenance.

The rule layer, not the extractor, determines how individual activities count toward any E/M requirement.

### MedicationActivity
A documented medication-management activity.

Minimum fields:

- Medication when identifiable.
- Activity type: start, stop, continue, dose change, prescribe, monitor, adverse-effect discussion, adherence discussion, or other documented management activity.
- Associated condition/problem when supported.
- Rationale or decision context when documented.
- Evidence provenance.

### EvaluationManagementEvidence
Container for facts relevant to outpatient E/M evaluation without deciding an E/M level.

Minimum fields:

- `problems_addressed` — references to `ConditionAddressed` objects.
- `data_activities` — references to `DataActivity` objects.
- `management_activities` — medication and other documented management/risk decisions.
- `practitioner_time_minutes` — documented E/M practitioner time when present.
- `time_documentation_type` — total time, start/stop, absent, or ambiguous.

No E/M level is stored as evidence. Level selection belongs to deterministic rule evaluation.

### PsychiatricEvaluationEvidence
Structured evidence from a psychiatric diagnostic evaluation.

Minimum fields, each using the shared evidence contract where applicable:

- Reason for evaluation / chief complaint.
- Referral source when documented.
- History of present illness / current symptoms.
- Past psychiatric history.
- Significant medical history.
- Current medications.
- Social history.
- Family history.
- Mental status examination.
- Diagnostic impression / problem list.
- Treatment plan and documented goals.
- Medical assessment or management activity when present.
- Information source when material information came from someone other than the patient.

These fields capture documentation facts. Whether a particular service requires each field is a rule question, not an extraction decision.

### PsychotherapyEvidence
Structured evidence that psychotherapy occurred and what was documented about it.

Minimum fields:

- Psychotherapy present/absent/ambiguous state.
- Psychotherapy time in minutes when documented.
- Time documentation type: total time, start/stop, absent, or ambiguous.
- Therapeutic intervention/method documented.
- Target problem, symptom, or treatment goal.
- Patient participation/interaction when documented.
- Response/progress or lack of change when documented.
- Relationship to the active treatment plan when documented.
- Separate-identifiability evidence when psychotherapy and E/M occur in the same encounter.

Psychotherapy time and E/M time must remain separate evidence values. The extractor does not decide which psychotherapy code, if any, the duration supports.

### Rule
A deterministic requirement or policy condition with source/version metadata.

### RuleEvaluation
The result of applying one rule to structured evidence: supported, unsupported, ambiguous, or not applicable.

### CandidateService
A proposed billable service linked to the evidence and rules supporting it.

### AuditFinding
A challenge to a candidate service or claim: missing evidence, contradiction, unsupported inference, rule conflict, or uncertainty.

### PayerProfile
Payer-specific requirements layered on top of base rules.

### ClaimResult
The final compiled result presented for human review.

## v0.1 evidence-schema boundary

The schema is intentionally broad enough to represent the selected E/M, psychiatric evaluation, and psychotherapy benchmark families but narrow enough to avoid embedding code logic in the AI layer.

Phase 1 may extend a field only when a development case or source-verified rule demonstrates that the existing schema cannot represent a required fact. Schema changes must preserve provenance and benchmark compatibility.

## Future objects

InsuranceCard, PatientIdentity, ProviderContract, EligibilityResult, DenialEvent, and ClaimOutcome are deferred until their corresponding modules are built.
