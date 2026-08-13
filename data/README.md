# Data

This directory contains synthetic development and benchmark fixtures only.

- `development_cases/` — generated/fake encounters used while developing behavior. These may be inspected, modified, and tuned against.
- `evaluation_cases/` — known-answer fixtures reserved for independent evaluation. Once a benchmark version is frozen, do not tune prompts/rules/models against those frozen cases and still treat them as independent evidence.

Real patient/PHI data does not belong in this repository.

Billing rules do not live here. The authoritative executable-rule layer is `rules/`.
