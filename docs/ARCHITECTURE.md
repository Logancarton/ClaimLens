# Architecture

## Canonical signal flow

`Encounter → Evidence Extraction → Structured Evidence → Rule Engine → Claim Compiler → Adversarial Audit → Payer Validation → Human Review`

The same core signal flow supports both v0.1 workflow checkpoints: `PRE_SIGN` and `PRE_SUBMIT`. The checkpoint changes how findings are used, not how evidence or rules are interpreted.

## Separation of responsibility

### Encounter layer
Owns the raw encounter input and explicitly supplied encounter metadata. It does not decide billing and does not infer missing provider, patient-status, place-of-service, or workflow-stage facts.

PMHNP/NP and psychiatrist remain distinct provider identities in encounter metadata so later rule evaluation can use provider class when an authoritative rule requires it.

### AI evidence layer
Interprets unstructured clinical language and maps it into the constrained schema defined in `docs/DATA_MODEL.md`. It answers: **What does the record actually say?**

For v0.1, this layer may populate shared evidence states/provenance plus the E/M, psychiatric-evaluation, psychotherapy, condition, medication, and data-activity evidence structures needed by the selected benchmark scope.

The evidence layer must not select a billing level or convert an extraction confidence score into billing support. Historical/copied-forward material does not become current evidence merely because it is repeated; unclear temporal status remains explicit.

### Rule layer
Represents deterministic billing requirements whenever possible. It answers: **What does that evidence support under the applicable rules?**

Rules consume structured evidence and encounter metadata; they do not rewrite the source evidence to make a requirement pass. Provider-specific behavior is allowed only when rule provenance establishes that provider class is material.

### Compiler
Builds a candidate claim from structured evidence plus rule results. It must preserve provenance from claim element back to evidence and rule.

### Auditor
Independently challenges the candidate claim for unsupported assumptions, contradictions, missing requirements, weak evidence, or material uncertainty.

Material ambiguity, contradiction, unclear temporal scope, unresolved rule-source conflict, or unknown material applicability must remain a human-review condition rather than being silently collapsed to support.

### Payer layer
Applies payer-specific overlays after the base rules are established. Payer behavior must not silently redefine the underlying clinical evidence.

### Result layer
Produces a human-readable and machine-readable result containing the candidate claim, support, uncertainty, warnings, workflow stage, and review status.

At `PRE_SIGN`, findings may identify documentation gaps while the clinician still controls the note, but ClaimLens does not invent documentation. At `PRE_SUBMIT`, the finalized record is evaluated as-is; missing support remains missing.

## v0.1 evidence handoff

The Evidence → Rule handoff carries facts, not conclusions. At minimum it preserves:

- Evidence state: present, absent, ambiguous, contradictory, or not applicable.
- Exact source provenance.
- Current/historical/unclear temporal scope when relevant.
- Workflow stage: pre-sign or pre-submit.
- Rendering provider type/credential as supplied encounter metadata.
- Atomic facts needed by the selected E/M, psychiatric-evaluation, and psychotherapy benchmark families.
- Separate E/M and psychotherapy time evidence when both appear in one encounter.

The rule engine owns all code/service eligibility and level-selection decisions.

## Architectural invariants

1. AI interpretation and deterministic rules remain separate.
2. No claim element may appear without traceable supporting evidence or an explicit reason for ambiguity.
3. Missing documentation remains missing; ClaimLens never fabricates a fix.
4. Historical/copied-forward material does not silently satisfy current-encounter requirements.
5. The auditor is allowed to reject or downgrade the compiler result.
6. Material unresolved uncertainty fails to human review.
7. Human review remains the terminal authority in early versions.
8. New complexity is added only after a measured failure demonstrates the need.
