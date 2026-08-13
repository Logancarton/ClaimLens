# Product Requirements

Requirements are intentionally separated from implementation. A requirement can be approved before any code exists.

## P0 — Core MVP requirements

### PR-001 Traceable evidence extraction
ClaimLens shall convert an encounter into structured billing-relevant evidence and retain provenance back to the source encounter.

### PR-002 Explicit uncertainty
ClaimLens shall distinguish present, absent, ambiguous, contradictory, and not-applicable states when the distinction matters.

### PR-003 No invented support
ClaimLens shall not convert model inference into documented evidence when the record does not support the fact.

### PR-004 Deterministic rule evaluation
Requirements that can be expressed deterministically shall be evaluated outside the language model.

### PR-005 Candidate claim assembly
ClaimLens shall assemble candidate services only from structured evidence and applicable rule evaluations.

### PR-006 Independent audit
ClaimLens shall independently challenge candidate services for unsupported assumptions, missing evidence, contradictions, rule conflicts, and material uncertainty.

### PR-007 Human review terminal state
Early versions shall end in a human-reviewable result rather than autonomous submission. Material ambiguity, contradiction, unclear temporal scope, unresolved rule-source conflict, or unknown material applicability shall resolve to `REVIEW`.

### PR-008 Explainable result
Each candidate service and audit finding shall be traceable to evidence and applicable rules.

### PR-009 Known-answer verification
Core behavior shall be tested against synthetic known-answer cases before production data is considered.

### PR-010 PHI-safe development repository
The source repository shall not contain real patient/PHI data, credentials, or secrets.

### PR-011 Dual review checkpoints
The v0.1 core analysis shall support both `PRE_SIGN` and `PRE_SUBMIT` workflow stages. The same evidence and rule boundaries apply at both checkpoints; pre-sign may surface gaps while the clinician controls the note, while pre-submit evaluates the finalized record as-is.

### PR-012 Temporal evidence integrity
ClaimLens shall distinguish current-encounter evidence from historical/copied-forward material. Repetition alone shall not make historical material current. Material temporal uncertainty shall remain explicit and escalate to human review.

## P1 — After core reliability

- Versioned payer-specific overlays.
- Batch encounter audit.
- Structured export/API result.
- Denial/outcome feedback capture.
- User-facing review interface.

## P2 — Deferred integrations

- Insurance-card and ID ingestion.
- Provider-network matching.
- Live eligibility.
- EHR and clearinghouse integration.
- Automated claim submission.

## Non-functional requirements

### Reliability
The system should fail to `REVIEW` rather than confidently invent support or silently resolve material uncertainty.

### Provenance
Evidence and rules must remain inspectable.

### Versionability
Rules, prompts, schemas, models, and benchmark sets must be version-identifiable.

### Modularity
Evidence interpretation, rule logic, compilation, auditing, payer overlays, and presentation remain replaceable components.

### Measurability
Major changes require a benchmark result or explicit acceptance test showing what improved.
