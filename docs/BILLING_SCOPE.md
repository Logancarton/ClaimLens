# Billing Scope

## Initial setting

Outpatient psychiatry / behavioral-health professional services, centered on psychiatric prescriber workflows.

## Initial clinician types

The v0.1 benchmark uses two distinct provider classes:

- PMHNP / nurse practitioner whose scope authorizes the psychiatric service being evaluated.
- Psychiatrist.

Both provider classes appear in benchmark cases. ClaimLens keeps the provider identity distinct even when an applicable rule reaches the same result for both.

Any provider-specific supervision, collaboration, signature, enrollment, or billing condition must come from an authoritative rule for the relevant payer, jurisdiction, setting, and service. ClaimLens does not infer such a condition from provider title alone.

## Initial benchmark service families

The v0.1 benchmark includes all three of these linked outpatient psychiatric service families:

- Outpatient evaluation/management for psychiatric medication-management encounters.
- Psychiatric diagnostic evaluation.
- Psychotherapy services and psychotherapy add-ons.

This remains a deliberately bounded outpatient psychiatric scope. It does not expand v0.1 into other specialties or settings.

Exact code logic is not considered implemented merely because a code appears in a prompt or document. Each supported service must have validated source rules, explicit tests, and known-answer cases.

## Payer sequence

1. Establish base coding/documentation logic.
2. Add Medicare rules as versioned rule sources.
3. Add Arizona-specific requirements only where they materially differ or add obligations.
4. Add commercial payer overlays one payer at a time.

## Out of scope initially

- Inpatient hospital coding.
- Emergency department coding.
- Surgery/procedural specialties.
- DRG coding.
- Autonomous claim submission.
- Live eligibility/network verification.

## Rule-source requirement

Billing rules are versioned knowledge. Every production rule should eventually record its authoritative source, effective date/version, and verification date. AI-generated summaries are not authoritative rule sources.
