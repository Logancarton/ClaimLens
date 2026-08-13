# ClaimLens v0.1 MVP Definition

## One-sentence finish line

Given one synthetic outpatient psychiatric encounter, ClaimLens produces traceable structured billing evidence, applies a deliberately narrow set of validated rules, compiles a candidate claim, independently audits it, and returns a human-review result without inventing support.

## Required v0.1 signal path

`Encounter → Evidence → Rules → Candidate Claim → Audit → Result`

## v0.1 benchmark scope

The selected benchmark scope is the bounded outpatient psychiatric service territory defined in `docs/BILLING_SCOPE.md`, which includes all three selected service families and both PMHNP/NP and psychiatrist workflows.

The two provider types share the same core ClaimLens pathway unless verified project rules require a provider-specific distinction.

## v0.1 is complete only when

- The encounter input format is defined.
- The evidence schema is defined and implemented for the selected benchmark scope.
- Evidence preserves source provenance.
- Missing/ambiguous/contradictory evidence can be represented explicitly.
- The selected benchmark scope has source-verified executable rules for the behavior ClaimLens claims to support.
- The compiler can produce a supported/unsupported/review candidate result.
- The auditor can challenge the candidate independently.
- Known-answer synthetic cases exercise clean, missing, ambiguous, contradictory, overcoding-trap, and under-detection cases.
- A frozen evaluation set exists.
- Benchmark results are recorded and reproducible.

## Explicitly not required for v0.1

- UI.
- EHR integration.
- Clearinghouse integration.
- Insurance eligibility.
- Network verification.
- Autonomous submission.
- Multiple specialties.
- Custom foundation-model training.
- Large-scale agent architecture.
- Production PHI.

## Definition of success

The MVP is not successful because it can produce a plausible code. It is successful when the system can show what evidence supports its conclusion, decline unsupported conclusions, and reproduce known-answer behavior across a benchmark set.
