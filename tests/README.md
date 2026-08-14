# Tests

Automated tests prove component behavior.

- Development fixtures live in `data/development_cases/` and may be used while designing/fixing behavior.
- Frozen known-answer benchmark fixtures live in `data/evaluation_cases/` and may be consumed by tests or benchmark runners without becoming tuning data.
- Phase 1 and Phase 2 focused tests use Python's standard-library `unittest`; no runtime dependency is required for the encounter/evidence contract, mocked Ollama guardrail tests, generic deterministic rule-engine contract tests, or the first outpatient E/M rule tests.

A test should answer a behavioral question, not merely prove that code executes.

Phase 1 evidence behavior remains covered, including provenance, temporal scope, ambiguity/contradiction, medication-list status versus management, source linkage, historical preservation, and model guardrail safety.

## Phase 2 generic rule-engine contract

`test_rules.py` verifies:

- every executable rule carries authoritative source metadata;
- rule evaluations preserve rule/source/evidence traceability;
- `SUPPORTED`, `UNSUPPORTED`, `REVIEW`, and `NOT_APPLICABLE` remain distinct;
- duplicate rule IDs fail closed to `REVIEW`;
- source-verified but unimplemented rules cannot create support;
- provider applicability remains explicit; and
- cross-encounter evidence is rejected.

## Phase 2 first source-verified outpatient E/M pathway

`test_outpatient_em_rules.py` consumes `data/development_cases/phase2_outpatient_em_rule_cases.json` and verifies the first narrow AMA-backed pathway recorded in `rules/OUTPATIENT_EM_MEDICATION_MANAGEMENT.md`.

It covers:

- supported behavior;
- unsupported behavior for the narrow pathway without claiming the entire service is unsupported;
- ambiguity/review behavior;
- established-patient applicability;
- the same rule path for the current PMHNP/NP and psychiatrist benchmark classes; and
- duplicate actual rule-ID/source conflict → `REVIEW`.

The test does not reproduce the full CPT MDM table, CPT descriptors, or comprehensive code/time tables.

Latest completed local checkpoint before this rule was added: 29/29 tests passed on 2026-08-13. The new outpatient E/M implementation is **verification pending** until the focused and full suites below are run against current `main`.

Focused PowerShell verification:

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests -p "test_outpatient_em_rules.py" -v
```

Broader repository verification:

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests -v
```

Do not mark the rule `TESTED`/`ACTIVE`, satisfy Gate 2, or begin Gate-3-dependent compiler work until both required checkpoints are green and their individual results are inspected.
