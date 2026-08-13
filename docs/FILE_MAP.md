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
Synthetic development and benchmark fixtures only. See `data/README.md`.

- `data/development_cases/` — cases agents may inspect, modify, and tune against during development.
- `data/evaluation_cases/` — frozen known-answer cases used as independent evaluation evidence once a benchmark version is frozen.

## `tests/`
Automated behavioral checks. See `tests/README.md`.

## `output/`
Generated local results. Contents are ignored except `.gitkeep`.

## `.agents/`
Project-specific AI guidance, including autonomy controls, the architecture steward, and reusable development skills.

- `.agents/AUTONOMY_POLICY.md` — defines autonomous work selection, authority boundaries, and human stop conditions.
- `.agents/ARCHITECTURE_STEWARD.md` — protects product and architecture boundaries.
- `.agents/skills/` — reusable ClaimLens development workflows followed by AI coding tools.
