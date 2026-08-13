# Product Scope

## Problem

Clinical documentation, coding rules, payer requirements, and claim preparation are separate systems. This creates missed revenue, unsupported billing, denials, audit exposure, and unnecessary human review.

## Product

ClaimLens converts an encounter into structured billing evidence, applies explicit rules, compiles a defensible candidate claim, and audits the result before human approval.

## Initial user and commercial target

The first commercial validation target is an independent or small outpatient psychiatric practice, beginning with psychiatric prescriber workflows. Individual psychiatric clinicians/practice owners are the initial buyer/user profile; larger groups, billing companies, and health systems remain later expansion targets.

The v0.1 benchmark includes PMHNP/NP and psychiatrist as distinct provider classes.

## Initial workflow checkpoints

ClaimLens supports the same core analysis at two checkpoints:

1. **Pre-sign** — identify billing-relevant documentation that is present, missing, ambiguous, contradictory, or temporally unclear while the clinician still controls the note. ClaimLens may flag issues but must not invent language or facts for the clinician to add.
2. **Pre-submit** — evaluate the finalized encounter record and candidate claim before submission. At this checkpoint, missing support remains missing; ClaimLens does not alter the signed record.

The workflow checkpoint changes the purpose of review, not the underlying evidence or billing rules.

## Inputs

Initially: synthetic clinical note text plus explicitly supplied encounter metadata. Later inputs may include diagnoses, provider information, payer information, prior notes, denial history, and integrated EHR/clearinghouse data.

## Outputs

- Structured billing-relevant evidence.
- Candidate claim/services.
- Evidence supporting each candidate.
- Missing or ambiguous evidence.
- Contradictions and audit findings.
- Rule/payer issues.
- Human-review status.

## Objective

Find the most appropriate defensible claim supported by the record.

ClaimLens must never optimize for the highest-paying code independent of documentation support.

## Hard boundaries

ClaimLens does not:

- Diagnose patients.
- Recommend clinical treatment.
- Invent or backfill undocumented facts.
- Autonomously alter clinical documentation.
- Alter a signed medical record.
- Treat probabilistic model output as a billing rule.
- Submit a questionable claim without human review.
- Store or commit real patient data in this repository.

## Deferred product area

Insurance intake/verification is planned after the core compiler. It may eventually ingest an insurance card and ID, resolve carrier/member/group information, obtain verified payer contact/claim-routing data, determine provider participation when authoritative data is available, and later perform eligibility checks through integration.
