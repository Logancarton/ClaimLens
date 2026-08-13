# Architecture

## Canonical signal flow

`Encounter → Evidence Extraction → Structured Evidence → Rule Engine → Claim Compiler → Adversarial Audit → Payer Validation → Human Review`

## Separation of responsibility

### Encounter layer
Owns the raw encounter input and encounter metadata. It does not decide billing.

### AI evidence layer
Interprets unstructured clinical language and maps it into a constrained structured schema. It answers: **What does the record actually say?**

### Rule layer
Represents deterministic billing requirements whenever possible. It answers: **What does that evidence support under the applicable rules?**

### Compiler
Builds a candidate claim from structured evidence plus rule results. It must preserve provenance from claim element back to evidence and rule.

### Auditor
Independently challenges the candidate claim for unsupported assumptions, contradictions, missing requirements, or weak evidence.

### Payer layer
Applies payer-specific overlays after the base rules are established. Payer behavior must not silently redefine the underlying clinical evidence.

### Result layer
Produces a human-readable and machine-readable result containing the candidate claim, support, uncertainty, warnings, and review status.

## Architectural invariants

1. AI interpretation and deterministic rules remain separate.
2. No claim element may appear without traceable supporting evidence or an explicit reason for ambiguity.
3. Missing documentation remains missing; ClaimLens never fabricates a fix.
4. The auditor is allowed to reject or downgrade the compiler result.
5. Human review remains the terminal authority in early versions.
6. New complexity is added only after a measured failure demonstrates the need.
