# DEV-005 — Medication List Without Current Plan

**Status:** Development-only synthetic fixture. Not a billing-gold case.

## Purpose

Test the boundary between medication presence and documented medication-management activity.

## Synthetic encounter

> Depression and low motivation were discussed. Current medication list: bupropion XL 150 mg daily. The remainder of the note discusses sleep routine and work stress. No medication plan is documented.

## Expected evidence observations

- `ConditionAddressed`: depression/low motivation are addressed in the encounter.
- Bupropion XL 150 mg daily is present on the medication list.
- Medication presence alone must not be transformed into an undocumented start, stop, continuation, or dose change.
- The absence of a current medication plan should remain explicit rather than being backfilled from the medication list.
- Provenance should distinguish the medication-list source from current assessment/discussion text.
- No psychotherapy evidence, billing code, or candidate service should be inferred from the available text alone.

## Failure this case should expose

Inventing medication-management activity from a medication list or converting missing documentation into positive support.
