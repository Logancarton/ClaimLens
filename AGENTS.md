# ClaimLens Agent Instructions

Repository: `Logancarton/ClaimLens`
Default branch: `main`

The repository is the source of truth.

Before architecture or implementation work, read:

1. `README.md`
2. `docs/PRODUCT_SCOPE.md`
3. `docs/ARCHITECTURE.md`
4. `docs/BILLING_SCOPE.md`
5. `docs/DATA_MODEL.md`
6. `docs/IMPLEMENTATION_STATUS.md`
7. `docs/DECISIONS.md`
8. `agent/ARCHITECTURE_STEWARD.md`
9. `.agents/skills/claimlens-development-workflow/SKILL.md`

## Non-negotiable rules

- Preserve the canonical signal flow unless an explicit architecture decision changes it.
- Do not let the LLM silently replace deterministic billing rules.
- Never invent documentation or evidence.
- Never optimize for the highest-paying code independent of support.
- Never commit real patient/PHI data, credentials, tokens, or secrets.
- Do not add agents, memory systems, vector databases, custom model training, integrations, or infrastructure merely because they are interesting.
- Add complexity only to solve a demonstrated requirement or measured failure.
- Keep runtime orchestration thin and put behavior in the component that owns it.
- Tests must prove behavior, not merely execute code.
- Update implementation status and decisions when architecture or verified status changes.

## Work order

Inspect → identify owner → define expected behavior → establish baseline/test → implement smallest systemic change → run focused tests → run broader verification → review diff → update project truth → commit/push only verified work.
