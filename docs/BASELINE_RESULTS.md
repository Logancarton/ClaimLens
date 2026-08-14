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

### Guarded extractor iteration

The next Phase 1 iteration used the same model and cases but added deterministic evidence-layer guardrails around model output:

- Canonical medication activity values are schema-constrained; status words such as `current`, `listed`, `taking`, or `medication_list_presence` cannot be accepted as medication actions.
- A named medication activity must be directly supported by source text linking that medication to the action; otherwise the named action is removed and unresolved linkage becomes reviewable ambiguity.
- Explicit medication-list language is preserved deterministically and model-created list evidence without explicit list language is filtered.
- Explicit historical medication changes with historical source cues are preserved deterministically.
- Contradiction state is derived deterministically when supported current actions conflict.

These are evidence-normalization/safety guardrails, not billing rules. The first baseline and failed prompt-v2 experiment remain preserved as evidence.

The guarded extractor was then rerun locally on the same five development cases. Observed metrics:

- Valid output rate: 1.0
- Exact case rate: 0.6
- Review accuracy: 0.8
- Current medication-action precision: 1.0
- Current medication-action recall: 0.75
- Historical medication-action precision: 1.0
- Historical medication-action recall: 1.0
- Unsupported current actions: 0
- Missed current actions: 1

Case results:

- `DEV-001`: match.
- `DEV-002`: match.
- `DEV-003`: mismatch — `fluoxetine/stop` was retained, but the independently explicit `fluoxetine/continue` action was missed, so the expected contradiction/review state was not derived.
- `DEV-004`: match — current aripiprazole continuation and historical aripiprazole increase were both preserved.
- `DEV-005`: mismatch — no medication-management action was emitted, but one explicit medication-list statement became two `medication_list_presence` items.

This result materially improves on both the initial 0.2 exact-case baseline and the 0.0 prompt-v2 experiment. It also narrows the remaining measured failures to two evidence-normalization mechanisms rather than broad model unreliability.

### Residual guardrail correction pending rerun

The current correction targets only those two measured mechanisms:

- Preserve another independently explicit current action only for a medication whose identity has already been validated by a directly supported model medication activity; require a current, non-conditional source sentence before adding the omitted action. This prevents generic phrases such as `monitor symptoms` from creating a medication identity.
- Make deterministic source parsing the single owner of explicit `medication_list_presence` evidence after validating any model-supplied list quote. One explicit list statement therefore yields one canonical list-presence item, while separate source statements remain distinct.

Focused mocked-Ollama tests cover both behaviors, conditional-action safety, and the requirement that generic non-medication action targets are not promoted. The real five-case MedGemma/Ollama baseline must be rerun before these corrections count as measured model-backed improvement.

Interpretation:

The model/runtime integration works reliably enough to run the experiment, and deterministic evidence guardrails substantially improved the development baseline. Evidence extraction is still not Verified because the latest measured guarded run is 3/5 exact and the residual correction has not yet been rerun through the real model-backed path. Gate 1 remains not satisfied.
