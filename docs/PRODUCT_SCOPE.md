# Product Scope

## Problem

Clinical documentation, coding rules, payer requirements, and claim preparation are separate systems. This creates missed revenue, unsupported billing, denials, audit exposure, and unnecessary human review.

## Product

ClaimLens converts an encounter into structured billing evidence, applies explicit rules, compiles a defensible candidate claim, and audits the result before human approval.

## Initial user

Outpatient psychiatric clinicians and practices, beginning with medication-management workflows.

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
- Alter a signed medical record.
- Treat probabilistic model output as a billing rule.
- Submit a questionable claim without human review.
- Store or commit real patient data in this repository.

## Deferred product area

Insurance intake/verification is planned after the core compiler. It may eventually ingest an insurance card and ID, resolve carrier/member/group information, obtain verified payer contact/claim-routing data, determine provider participation when authoritative data is available, and later perform eligibility checks through integration.
