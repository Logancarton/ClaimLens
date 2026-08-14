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

### Replication before correction

A second run using the same model, prompt, schema, and five development cases reproduced the same aggregate metrics and the same exact-case pattern: only `DEV-001` matched. The diagnostic runner measured total runtime at 235.051 seconds. This replication strengthens the interpretation that the observed failures are systematic enough to justify a targeted Phase 1 correction rather than being treated as a one-off generation anomaly.

The replicated case diagnostics showed:

- `DEV-002`: emitted `lamotrigine/current`, did not escalate review.
- `DEV-003`: retained `continue fluoxetine` but missed `stop fluoxetine`, contradiction evidence, and required review.
- `DEV-004`: retained current aripiprazole continuation but missed the historical aripiprazole increase.
- `DEV-005`: correctly emitted no medication action but missed explicit medication-list presence.

### Prompt v2 experiment

`prompts/extract_evidence.txt` was tightened to explicitly distinguish medication-list status from medication management, preserve historical actions, retain both sides of contradictions, and represent unresolved generic linkage as ambiguity. The same five development cases were rerun with the same MedGemma/Ollama runtime.

Observed v2 metrics:

- Valid output rate: 1.0
- Exact case rate: 0.0
- Review accuracy: 0.6
- Current medication-action precision: 0.6667
- Current medication-action recall: 1.0
- Historical medication-action precision: undefined (`null`)
- Historical medication-action recall: 0.0
- Unsupported current actions: 2
- Missed current actions: 0
- Total runtime: 143.37 seconds

Prompt v2 improved current-action recall: both `continue` and `stop` were retained for `DEV-003`. However, prompt-only correction regressed exact-case performance and produced new status-as-action errors (`medication_list_presence` inside the medication activity field). Historical recall remained zero and review escalation did not improve. This falsifies the idea that prompt clarification alone is sufficient for the measured Phase 1 failures.

The v2 run also exposed a development-fixture inconsistency: `DEV-002` explicitly states that lamotrigine appears on the current medication list, while the original expected value for medication-list presence was zero. The development expectation was corrected to one; this is a development-fixture correction, not a retroactive change to frozen evaluation truth.

### Current correction under test

The next Phase 1 iteration uses the same model and cases but adds deterministic evidence-layer guardrails around model output:

- Canonical medication activity values are schema-constrained; status words such as `current`, `listed`, `taking`, or `medication_list_presence` cannot be accepted as medication actions.
- A named medication activity must be directly supported by source text linking that medication to the action; otherwise the named action is removed and unresolved linkage becomes reviewable ambiguity.
- Explicit medication-list language is preserved deterministically and model-created list evidence without explicit list language is filtered.
- Explicit historical medication changes with historical source cues are preserved deterministically.
- Contradiction state is derived deterministically when supported current actions conflict.

These are evidence-normalization/safety guardrails, not billing rules. The first baseline and failed prompt-v2 experiment remain preserved as evidence.

Interpretation:

The model/runtime integration works reliably enough to run the experiment, but raw/prompted MedGemma output is not yet reliable enough to mark evidence extraction Verified. Gate 1 remains not satisfied pending a rerun of the hybrid guarded extractor and broader Phase 1 development coverage.
