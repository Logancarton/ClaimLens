# Tests

Automated tests prove component behavior.

- Development fixtures live in `data/development_cases/` and may be used while designing/fixing behavior.
- Frozen known-answer benchmark fixtures live in `data/evaluation_cases/` and may be consumed by tests or benchmark runners without becoming tuning data.

A test should answer a behavioral question, not merely prove that code executes.

Examples:

- Did evidence extraction preserve provenance?
- Did the rule engine reject missing support?
- Did the compiler avoid unsupported services?
- Did the auditor catch the deliberately inserted defect?
