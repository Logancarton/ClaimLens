# Tests

Automated tests prove component behavior.

- Development fixtures live in `data/development_cases/` and may be used while designing/fixing behavior.
- Frozen known-answer benchmark fixtures live in `data/evaluation_cases/` and may be consumed by tests or benchmark runners without becoming tuning data.
- Phase 1 focused tests use Python's standard-library `unittest`; no runtime dependency is required for the encounter/evidence contract or mocked Ollama guardrail tests.

A test should answer a behavioral question, not merely prove that code executes.

Current Phase 1 questions include:

- Did encounter input preserve explicit workflow stage and provider class without inference?
- Did evidence preserve exact source provenance?
- Did historical material remain distinct from current-encounter evidence?
- Did ambiguity and contradiction remain visible for review?
- Did medication-list presence avoid becoming undocumented medication-management activity?
- Does the Ollama schema reject status/list words as medication action types?
- Does a named medication action require direct source linkage between the medication and action?
- Are explicit medication-list facts, generic unresolved linkage, historical dose changes, and contradictions preserved by deterministic evidence-layer guardrails when the model omits or misclassifies them?

Run the focused suite from the repository root in PowerShell:

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests -v
```

Later phases add rule, compiler, and auditor behavioral tests only when their gates become active.
