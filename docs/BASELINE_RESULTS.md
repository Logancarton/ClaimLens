# Baseline Results

## 2026-08-13 — Phase 1 MedGemma 1.5 4B / Ollama development baseline

This is a development-case baseline, not a frozen evaluation benchmark and not evidence of production readiness.

Runtime: local Ollama API
Model: `medgemma1.5` (selected baseline `google/medgemma-1.5-4b-it`)
Cases: 5 synthetic development cases

Observed metrics from the first successful local model-backed run:

- Valid output rate: 1.0
- Exact case rate: 0.2
- Review accuracy: 0.6
- Current medication-action precision: 0.75
- Current medication-action recall: 0.75
- Historical medication-action recall: 0.0
- Unsupported current actions: 1
- Missed current actions: 1

The original runner printed historical medication-action precision as `1.0`, but the model made zero historical-action predictions. That number was a measurement artifact rather than meaningful precision. With no predicted positives, historical precision is undefined; the runner was corrected after this baseline was preserved.

Case-level observations:

- `DEV-001`: exact match; current sertraline continuation extracted correctly.
- `DEV-002`: failed. The model emitted `lamotrigine/current` as a current medication action where no current dose action was expected. This is an unsupported-current-action failure around medication-list and hypothetical/future language.
- `DEV-003`: failed. The model extracted fluoxetine continuation but missed the contradictory stop action, so contradiction/review behavior was incomplete.
- `DEV-004`: failed. Current aripiprazole continuation was extracted, but the historical aripiprazole increase was missed.
- `DEV-005`: failed exact-match scoring despite no current or historical medication actions. The first runner did not expose the remaining comparison fields in its terminal row; the runner was updated to show review state, medication-list evidence, contradiction count, expected values, per-case timing, and progress on subsequent runs.

Interpretation:

The model/runtime integration works and all five cases returned valid structured output with traceable provenance. The dominant failures are not transport/schema failures; they are semantic extraction failures involving temporal scope, hypothetical/current action discrimination, contradiction capture, and historical recall. Gate 1 remains not satisfied while these known failures remain unresolved and before the Phase 1 evidence baseline demonstrates acceptable behavior across the selected evidence territory.
