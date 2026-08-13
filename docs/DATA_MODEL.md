# Data Model

This file defines what ClaimLens knows before implementation choices define how it is stored.

## Core objects

### Encounter
Raw note plus encounter metadata.

### EvidenceItem
A single billing-relevant fact extracted from the encounter. Each item should eventually contain a category, normalized value, source/provenance, confidence, and ambiguity state.

### ConditionAddressed
A problem/condition actually addressed during the encounter, distinct from diagnoses merely present on a problem list.

### MedicationActivity
Medication start, stop, continuation, dose change, adverse-effect discussion, adherence discussion, or other prescription-management activity.

### PsychotherapyEvidence
Documented psychotherapy time, intervention, target/problem, and other required support fields.

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

## Future objects

InsuranceCard, PatientIdentity, ProviderContract, EligibilityResult, DenialEvent, and ClaimOutcome are deferred until their corresponding modules are built.
