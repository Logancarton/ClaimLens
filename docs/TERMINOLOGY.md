# Terminology

Use these terms consistently across code, docs, prompts, tests, and discussion.

## ClaimLens
The product/system as a whole.

## Claim Compiler
The subsystem that assembles candidate claim services from structured evidence and rule evaluations.

## Encounter
The source clinical encounter plus explicitly provided encounter metadata.

## Evidence
A billing-relevant fact actually supported by the encounter.

## Evidence State
The record-level state of an evidence item: `PRESENT`, `ABSENT`, `AMBIGUOUS`, `CONTRADICTORY`, or `NOT_APPLICABLE`. Evidence state describes what the record supports; it is not a billing decision.

## Temporal Scope
Whether an evidence item belongs to the `CURRENT_ENCOUNTER`, is `HISTORICAL`, or is `UNCLEAR`. This represents timing without deciding how copied-forward content is detected.

## Provenance
The location/source showing where an evidence item came from.

## Data Activity
An atomic documented data-review or data-analysis action captured as evidence. Rules decide how, or whether, it counts toward a billing requirement.

## Evaluation/Management Evidence
Structured facts relevant to outpatient E/M evaluation, including addressed problems, data activities, management activities, and documented practitioner time. It does not contain an E/M level decision.

## Psychiatric Evaluation Evidence
Structured facts documented during a psychiatric diagnostic evaluation, such as presenting reason, histories, mental status examination, diagnostic impression, and treatment plan.

## Psychotherapy Evidence
Structured facts showing whether psychotherapy occurred and documenting its time, intervention, target, participation/response, and other source-supported features.

## Rule
A versioned billing/payer requirement represented outside the language model when deterministic expression is possible.

## Rule Evaluation
Application of one rule to available evidence.

## Candidate Service
A service proposed by the compiler, not yet a final claim decision.

## Audit Finding
A reason the auditor believes a candidate may be unsupported, incomplete, contradictory, ambiguous, or otherwise require review.

## Supported
Required evidence/rules for the evaluated scope are satisfied.

## Unsupported
Required support is absent or fails an applicable rule.

## Ambiguous
The record does not permit a reliable supported/unsupported conclusion.

## Contradictory
Relevant pieces of the record conflict in a way that affects interpretation.

## Review
Human judgment is required before relying on the result.

## Verified
A component has explicit behavioral evidence demonstrating intended performance. “Implemented” alone does not mean verified.
