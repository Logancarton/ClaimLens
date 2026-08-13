# DEV-002 — Ambiguous Medication Change

**Status:** Development-only synthetic fixture. Not a billing-gold case.

## Purpose

Test whether ClaimLens can distinguish a possible future medication change from a change that actually occurred during the encounter.

## Synthetic encounter

> Mood is mostly stable. Lamotrigine 100 mg daily appears on the current medication list. We discussed that the dose could be increased in the future if depressive symptoms return. For now, continue current medications.

## Expected evidence observations

- `ConditionAddressed`: mood symptoms are discussed in the current encounter.
- A possible future lamotrigine increase is discussed, but a dose increase is **not** documented as occurring now.
- The system must not convert the hypothetical future increase into current `MedicationActivity` for a dose change.
- Linking “continue current medications” to a specific medication should preserve any ambiguity created by the note rather than inventing detail.
- Provenance should distinguish medication-list content from the discussion and plan text.
- No billing code or candidate service is asserted by this fixture.

## Failure this case should expose

Turning conditional or future language into a completed medication action, or resolving ambiguous medication linkage without support.
