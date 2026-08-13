# File Map

## Root

- `README.md` — what ClaimLens is.
- `ROADMAP.md` — development sequence and success gates.
- `AGENTS.md` — rules for AI coding/review agents.
- `requirements.txt` — Python dependencies once dependencies are earned.
- `.env.example` — names of required environment variables, never real secrets.
- `.gitignore` — files/data that must remain local.

## `docs/`
Project truth: scope, architecture, billing boundary, data model, decisions, and implementation status.

## `src/claim_compiler/`
Runtime implementation.

- `main.py` — thin entry point / sequencing.
- `encounter.py` — encounter input ownership.
- `evidence.py` — structured evidence extraction.
- `rules.py` — rule evaluation interface.
- `compiler.py` — candidate claim construction.
- `auditor.py` — adversarial review.
- `payer.py` — payer-specific overlays.
- `result.py` — final result objects/presentation.

## `rules/`
Human-reviewable versioned rule definitions grouped by source/jurisdiction.

## `prompts/`
Model instructions. Prompts interpret information; they are not authoritative billing rules.

## `data/`
- `synthetic_cases/` — generated/fake development encounters.
- `test_cases/` — known-answer benchmark fixtures.
- `payer_rules/` — structured payer data when needed.

Never store real patient/PHI data here.

## `tests/`
Automated behavioral checks corresponding to runtime components.

## `output/`
Generated local results. Contents should not be committed.

## `agent/` and `.agents/skills/`
Project-specific architecture steward plus the reusable development workflow followed by AI coding tools.
