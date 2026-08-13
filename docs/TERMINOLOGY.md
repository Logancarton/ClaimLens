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

## Provenance
The location/source showing where an evidence item came from.

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
