# DEV-001 — Clear Current Medication Activity

**Status:** Development-only synthetic fixture. Not a billing-gold case.

## Purpose

Establish the simplest positive evidence pattern: a condition is addressed and a medication action is explicitly current.

## Synthetic encounter

> Anxiety has improved since the last visit. The patient is taking sertraline 50 mg daily and reports no medication side effects. Continue sertraline 50 mg daily. Follow up as scheduled.

## Expected evidence observations

- `ConditionAddressed`: anxiety is addressed in the current encounter.
- `MedicationActivity`: sertraline 50 mg daily is explicitly continued in the current encounter.
- The statement about no medication side effects is current encounter evidence.
- Provenance should point to the exact text supporting each extracted fact.
- No psychotherapy evidence should be inferred from this note.
- No billing code or candidate service is asserted by this fixture.

## Failure this case should expose

A system that misses explicit current medication management, loses provenance, or invents additional services from a simple medication-management note.
