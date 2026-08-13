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

## Selected v0.1 service scope

The benchmark uses the bounded outpatient psychiatric service scope selected in `docs/BILLING_SCOPE.md`, including all three selected service families. Cases should cover each family and relevant cross-family interactions. Benchmark examples do not become billing-rule authority.

## Provider coverage

The v0.1 benchmark covers PMHNP/NP and psychiatrist as distinct provider classes. Both classes must be represented in the test set, including matched cases where provider identity is the only intentional difference. Provider-specific differences require verified project rules.

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

- `data/development_cases/` contains synthetic cases that may be inspected, modified, and used while developing behavior.
- `data/evaluation_cases/` contains known-answer cases reserved for independent evaluation.

Do not repeatedly tune prompts/rules/models against a frozen evaluation set and then treat that set as independent evidence. If an evaluation case must become development data, move/copy it into the development set and replace it with genuinely unseen evaluation coverage before using the benchmark as independent evidence again.

## Thresholds

Initial thresholds are deliberately not frozen before a baseline exists. Establish baseline performance first, then define release gates based on risk and observed error modes. Thresholds that determine release/pilot/stop decisions require explicit human approval under `.agents/AUTONOMY_POLICY.md`.
