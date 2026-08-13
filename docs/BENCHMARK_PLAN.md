# Benchmark Plan

ClaimLens must be benchmarkable before it is trusted.

## Benchmark unit

A benchmark case contains:

1. Synthetic encounter input.
2. Expected structured evidence.
3. Expected rule evaluations.
4. Expected candidate service state.
5. Expected audit findings.
6. Rationale for the gold answer.

## Initial benchmark families

- Clear supported encounter.
- Clear unsupported encounter.
- Missing required evidence.
- Ambiguous wording.
- Contradictory statements.
- Irrelevant documentation noise.
- Copied-forward material that should not be treated as current evidence.
- Medication started/stopped/continued/changed.
- Psychotherapy present but incomplete.
- Similar cases separated by one billing-relevant fact.
- Cases designed to tempt overcoding.
- Cases designed to expose under-detection of supported services.

## Core metrics

### Evidence layer
- Precision of extracted evidence.
- Recall of required evidence.
- Hallucinated-evidence rate.
- Ambiguity detection accuracy.
- Provenance accuracy.

### Rule / compiler layer
- Candidate-service accuracy.
- Unsupported-service rate.
- Missed-supported-service rate.
- Correct `REVIEW` escalation rate.

### Auditor layer
- True-positive rate for deliberate defects.
- False-positive rate on clean cases.
- Defect-category accuracy.

## Comparison strategy

Compare architectural changes against a frozen benchmark version. Do not declare improvement from anecdotal examples alone.

## Data split

Maintain development cases separately from frozen evaluation cases. Do not repeatedly tune prompts/rules against the same evaluation set and then treat that set as independent evidence.

## Thresholds

Initial thresholds are deliberately not frozen before a baseline exists. Establish baseline performance first, then define release gates based on risk and observed error modes.
