# File Map

## Root

- `README.md` — one-page identity and core signal flow.
- `ROADMAP.md` — build order and success gates.
- `AGENTS.md` — instructions for AI coding/review agents.
- `requirements.txt` — Python dependencies once they are actually needed.
- `.env.example` — environment-variable names only, never secrets.
- `.gitignore` — source-control exclusions and PHI guardrails.

## `docs/`
The project truth layer. Start with `docs/INDEX.md`.

## `src/claimlens/`
Runtime implementation owned by the ClaimLens product namespace.

- `main.py` — thin entry point and sequencing only.
- `encounter.py` — encounter input ownership.
- `evidence.py` — structured evidence extraction interface.
- `rules.py` — rule evaluation interface.
- `compiler.py` — candidate claim construction.
- `auditor.py` — adversarial review.
- `payer.py` — payer-specific overlays.
- `result.py` — final result structures/presentation.

## `rules/`
Single source-control home for human-reviewable executable billing-rule definitions. See `rules/README.md` and `docs/RULE_GOVERNANCE.md`.

## `prompts/`
Versioned model instructions. Prompts interpret information; they are not authoritative billing rules.

## `data/`
Synthetic development cases and known-answer test fixtures only. See `data/README.md`.

## `tests/`
Automated behavioral checks. See `tests/README.md`.

## `output/`
Generated local results. Contents are ignored except `.gitkeep`.

## `agent/`
Project-specific architecture steward.

## `.agents/skills/`
Reusable ClaimLens development workflow followed by AI coding tools.
