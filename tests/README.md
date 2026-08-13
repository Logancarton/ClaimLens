# Tests

Automated tests prove component behavior. Known-answer benchmark fixtures live in `data/test_cases/` and may be consumed by tests or benchmark runners.

A test should answer a behavioral question, not merely prove that code executes.

Examples:

- Did evidence extraction preserve provenance?
- Did the rule engine reject missing support?
- Did the compiler avoid unsupported services?
- Did the auditor catch the deliberately inserted defect?
