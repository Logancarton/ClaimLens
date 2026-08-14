# Tests

Automated tests prove component behavior.

- Development fixtures live in `data/development_cases/` and may be used while designing/fixing behavior.
- Frozen known-answer benchmark fixtures live in `data/evaluation_cases/` and may be consumed by tests or benchmark runners without becoming tuning data.
- Phase 1 and Phase 2 focused tests use Python's standard-library `unittest`; no runtime dependency is required for the encounter/evidence contract, mocked Ollama guardrail tests, or generic deterministic rule-engine contract tests.

A test should answer a behavioral question, not merely prove that code executes.

Phase 1 evidence behavior remains covered, including provenance, temporal scope, ambiguity/contradiction, medication-list status versus management, source linkage, historical preservation, and model guardrail safety.

Current Phase 2 rule-engine questions include:

- Does every executable rule carry authoritative source metadata?
- Does a rule evaluation preserve the rule ID, source references, and evidence references needed for traceability?
- Can the engine preserve distinct `SUPPORTED`, `UNSUPPORTED`, `REVIEW`, and `NOT_APPLICABLE` outcomes without collapsing uncertainty?
- Do conflicting definitions sharing a rule ID fail closed to `REVIEW` instead of silently choosing one source?
- Can a merely source-verified but not yet implemented rule avoid creating billing support?
- Does provider-specific behavior stay not-applicable to another provider class unless rule metadata explicitly includes that class?
- Does the engine reject evidence belonging to a different encounter?

The current Phase 2 tests intentionally exercise generic deterministic rule mechanics. They do **not** encode restricted CPT descriptors, the detailed MDM table, or code-level time thresholds while the authoritative CPT source/licensing path remains unresolved.

Latest local verification checkpoint (2026-08-13): after pulling `main` through `da1a9d3`, the full suite ran 29 tests and all 29 passed, including all seven generic Phase 2 rule-engine contract tests.

Run the applicable suite from the repository root in PowerShell:

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests -v
```

When Phase 2 source-verified outpatient E/M rules are implemented, add known-answer supported, unsupported, ambiguous, and source-conflict cases before Gate 2 can be satisfied.
