# DEV-003 — Contradictory Current Medication Plan

**Status:** Development-only synthetic fixture. Not a billing-gold case.

## Purpose

Test fail-closed handling when two current encounter statements conflict.

## Synthetic encounter

> Depression remains symptomatic. Assessment: continue fluoxetine 20 mg daily. The patient reports persistent nausea. Plan: stop fluoxetine because of nausea and reassess at follow-up.

## Expected evidence observations

- `ConditionAddressed`: depression is addressed in the current encounter.
- The note contains contradictory current medication instructions for fluoxetine: continue versus stop.
- ClaimLens must preserve the contradiction rather than choosing one statement as true by convenience.
- The nausea/adverse-effect discussion is current encounter evidence.
- Provenance should retain both conflicting source statements.
- The contradiction should be eligible for human review when the eventual evidence schema defines review behavior.
- No billing code or candidate service is asserted by this fixture.

## Failure this case should expose

Collapsing conflicting documentation into one confident medication action or silently repairing the note.
