# DEV-004 — Copied-Forward History Noise

**Status:** Development-only synthetic fixture. Not a billing-gold case.

## Purpose

Test temporal separation between historical/copied-forward material and current encounter evidence.

## Synthetic encounter

> Prior-visit history copied into today's note: aripiprazole was increased from 5 mg to 10 mg daily at the previous appointment because of persistent symptoms.
>
> Today: symptoms are stable and no new adverse effects are reported. Continue aripiprazole 10 mg daily without change.

## Expected evidence observations

- The increase from 5 mg to 10 mg is historical and must not be relabeled as a current dose change.
- Current `MedicationActivity` is continuation of aripiprazole 10 mg daily.
- Current symptom stability and absence of new adverse effects are separate current facts.
- Provenance should preserve which text is explicitly historical and which text belongs to the current encounter.
- No billing code or candidate service is asserted by this fixture.

## Failure this case should expose

Treating copied-forward medication changes as current work merely because they appear in the present note text.
