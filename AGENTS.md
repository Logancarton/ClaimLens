# ClaimLens Agent Instructions

Repository: `Logancarton/ClaimLens`
Default branch: `main`

The repository is the source of truth. Chat history may provide context, but it must not override the repository.

## Required startup sequence

Before architecture, implementation, debugging, or autonomous continuation work:

1. Read `README.md`.
2. Read `docs/INDEX.md` and follow the project-truth reading order relevant to the task.
3. Re-check `docs/IMPLEMENTATION_STATUS.md` for the current phase, gate, and actual component maturity.
4. Re-check `docs/OPEN_QUESTIONS.md` for unresolved items relevant to the current phase.
5. Re-check `docs/RELEASE_GATES.md` before starting work that could advance a phase.
6. Read `docs/DECISIONS.md` so settled decisions are not reopened silently.
7. Read `.agents/AUTONOMY_POLICY.md` before selecting work without direct human instruction.
8. Read `.agents/ARCHITECTURE_STEWARD.md`.
9. Follow `.agents/skills/claimlens-development-workflow/SKILL.md`.

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
- GitHub issues are a work queue, not permission to skip the current release gate.
- Never silently resolve an item in `docs/OPEN_QUESTIONS.md` through implementation.
- Update implementation status and decisions only when repository evidence or an explicit human decision justifies the change.

## Work order

Resolve current phase/gate → select an eligible unblocked issue → inspect → identify owner → define expected behavior → establish baseline/test → implement smallest systemic change → run focused tests → run broader verification → review diff → update project truth → commit/push only coherent verified work.

If no eligible work remains in the current phase, stop and report the exact blocker. Do not substitute work from a later phase.
