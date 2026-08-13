# Evaluation Cases

This folder is reserved for **independent known-answer holdout cases** used to measure ClaimLens after development behavior exists.

No scored evaluation fixture is frozen yet. That is intentional: Phase 0 still requires the human owner to select the exact first billing/service family and define the minimum evidence schema. Creating gold rule evaluations, candidate-service answers, or audit answers before those decisions would silently settle unresolved product/billing questions.

When those Phase 0 decisions are complete, each evaluation case must contain the benchmark unit defined in `docs/BENCHMARK_PLAN.md`:

1. Synthetic encounter input.
2. Expected structured evidence.
3. Expected rule evaluations.
4. Expected candidate service state.
5. Expected audit findings.
6. Gold-answer rationale.

Evaluation cases must remain genuinely independent of tuning. Once a benchmark version is frozen, do not repeatedly inspect/tune against these cases and still describe the resulting score as independent evidence. If a holdout case is promoted into development data, replace its evaluation coverage before using the benchmark as independent evidence again.

Use `CASE_TEMPLATE.md` only as a human-readable planning template. It is not a runtime schema and is not itself a benchmark case.

All content committed here must be synthetic or deliberately de-identified and must contain no real PHI, credentials, secrets, or proprietary payer material.
