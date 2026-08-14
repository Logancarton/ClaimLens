# ClaimLens Agent Instructions

Repository: `Logancarton/ClaimLens`
Default branch: `main`

The repository is the source of truth. Chat history may provide context, but it must not override the repository.

## Required startup sequence

Before architecture, implementation, debugging, or autonomous continuation work:

1. Read `README.md`.
2. Read `docs/INDEX.md` and follow the project-truth reading order relevant to the task.
3. Read `docs/FILE_MAP.md` as the maintenance key for ownership, dependencies, and end-of-task synchronization.
4. Re-check `docs/IMPLEMENTATION_STATUS.md` for the current phase, gate, and actual component maturity.
5. Re-check `docs/OPEN_QUESTIONS.md` for unresolved items relevant to the current phase.
6. Re-check `docs/RELEASE_GATES.md` before starting work that could advance a phase.
7. Read `docs/DECISIONS.md` so settled decisions are not reopened silently.
8. Read `.agents/AUTONOMY_POLICY.md` before selecting work without direct human instruction.
9. Read `.agents/ARCHITECTURE_STEWARD.md`.
10. Follow `.agents/skills/claimlens-development-workflow/SKILL.md`.

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
- A task is not complete until every materially affected repository file has been synchronized.
- Never leave stale paths, names, examples, comments, tests, fixtures, documentation, issue text, or project-truth references that contradict the completed change.

## Required verification checkpoints

Testing is a multi-step completion boundary, not a single command near the end of a task. Use every applicable checkpoint in order:

1. **Baseline / reproduction** — before changing behavior, reproduce the defect or establish the current known-answer result when practical.
2. **Focused verification** — after the smallest systemic change, run the tests that directly exercise the changed behavior and its safety boundaries.
3. **Broader suite** — before calling implementation complete, run the full applicable unit/integration suite for the affected repository area.
4. **Real runtime verification** — when behavior depends on a model, local runtime, external service, or environment the agent cannot faithfully simulate, run the real required path before claiming that behavior is Verified.
5. **Result inspection** — compare against the recorded baseline and inspect per-case/failure details, not only an aggregate pass/fail number.
6. **Repository synchronization** — only after required verification is green, update baseline/status/gate evidence, tracked issue/PR state, and every affected companion file identified by `docs/FILE_MAP.md`.

If the agent cannot execute a required checkpoint, the state is **implemented; verification pending**. The agent must not mark the component Verified, close the tracked issue, declare the release gate satisfied, or begin work that depends on that gate.

When a human supplies the required local test/runtime output, treat that output as verification evidence and resume the same workflow immediately. Do not stop after saying the tests passed: record the result, evaluate the active gate, synchronize affected project-truth files and issue/PR state, perform the stale-reference/final-diff sweep, and finish the current task cleanly.

A failed checkpoint returns the workflow to failure analysis within the current phase. Preserve failed experiments and prior baseline results; never rewrite prior evidence merely because a later iteration passes.

## Completion synchronization rule

At the end of every command/task, use the change matrix in `docs/FILE_MAP.md` to identify the materially affected file set, then perform a repository-wide affected-file sweep before declaring completion.

Synchronize every file materially affected by the change, including when applicable:

- Runtime/source files.
- Tests and test helpers.
- Development and evaluation fixtures.
- Prompts and rule definitions.
- README/file maps and architecture/data-model documentation.
- `docs/IMPLEMENTATION_STATUS.md`.
- `docs/DECISIONS.md` and `docs/OPEN_QUESTIONS.md` when the work changes or resolves their content.
- Release-gate, benchmark, security, or scope documents when their truth changed.
- GitHub issue/PR text or checklist state when the task is tracked there.
- Agent/skill instructions when workflow or repository structure changed.

Before finishing, search the repository for old names, paths, interfaces, or assumptions touched by the task and update any stale references. Review the final diff/status and confirm that no affected companion file identified by `docs/FILE_MAP.md` was omitted.

"All files" means all files materially affected by the command. Do not create meaningless churn in unrelated files merely to change timestamps or wording.

## Work order

Resolve current phase/gate → select an eligible unblocked issue → inspect → identify owner → consult `docs/FILE_MAP.md` for affected companions → define expected behavior → establish baseline/reproduction → implement smallest systemic change → run focused verification → run broader applicable suite → run required real runtime/model/integration verification → compare results with prior evidence → review for drift → synchronize every affected repository file → search for stale references → review final diff/status → update tracked issue/PR and gate state if justified → commit/push only coherent verified work.

If no eligible work remains in the current phase, stop and report the exact blocker. Do not substitute work from a later phase.
