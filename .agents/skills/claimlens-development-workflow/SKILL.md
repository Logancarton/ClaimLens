# ClaimLens Development Workflow Skill

## Purpose

Use this workflow for implementation, debugging, architecture review, testing, and repository cleanup in ClaimLens.

## Start from project truth

Read the canonical project documents listed in `AGENTS.md`. Do not infer architecture from filenames alone. Use `docs/FILE_MAP.md` as the maintenance key for deciding where work belongs and which companion files must be checked when something changes.

## Workflow

### 0. Resolve work state
Before selecting or continuing work, read `docs/IMPLEMENTATION_STATUS.md`, `docs/RELEASE_GATES.md`, `docs/OPEN_QUESTIONS.md`, `.agents/AUTONOMY_POLICY.md`, and the relevant portion of `docs/FILE_MAP.md`.

Confirm:

- Current phase and gate.
- Whether the requested/open issue belongs to that phase.
- Whether an unresolved human-decision blocker prevents work.
- Whether the change is authorized by settled project truth.
- Which files `docs/FILE_MAP.md` says must be checked if this category of change is made.

If no eligible task exists, stop and report the blocker instead of starting later-phase work.

### 1. State the requested outcome
Translate the request into one observable behavior or repository outcome.

### 2. Identify ownership
Locate the component that owns the behavior according to `docs/ARCHITECTURE.md` and `docs/FILE_MAP.md`. Do not patch neighboring layers to avoid fixing the owner.

### 3. Establish the baseline
Use an existing test or create the smallest known-answer synthetic case that exposes the current behavior. When a prior measured baseline exists, preserve it so later results can be compared rather than overwritten.

### 4. Preserve evidence boundaries
When working with AI output, require structured fields, provenance, uncertainty/ambiguity, and explicit absence. Never convert an unsupported model guess into evidence.

### 5. Preserve rule boundaries
Deterministic requirements belong in the rule system with source/version metadata. Prompts may explain or extract; they do not become authoritative billing policy.

### 6. Implement the smallest systemic change
Avoid one-case patches. Fix the process that caused the failure while preserving component ownership.

### 7. Verify in stages
Verification is mandatory and multi-step. Use every applicable stage in order.

#### 7A. Focused verification
Run the smallest tests that directly exercise the changed behavior, including negative/safety cases that could expose overgeneralization or unsupported inference.

#### 7B. Broader repository verification
Run the full applicable unit/integration suite for the affected area before considering implementation complete. A focused passing test does not substitute for the broader suite.

#### 7C. Real runtime/model/integration verification
If the behavior depends on a local model, external runtime, service, hardware path, or environment that the agent cannot faithfully reproduce, the real path is a required verification stage.

If the agent cannot run that stage, record the state as **implemented; verification pending** and stop gate-dependent advancement. Do not mark the component Verified, close the tracked issue, satisfy the release gate, or begin dependent later-phase work.

When the human supplies the required output, resume at this step without asking them to restate prior context.

#### 7D. Inspect and compare results
Do not rely only on an aggregate pass/fail line. Inspect relevant case-level behavior, false positives, false negatives, review/escalation behavior, provenance, and safety failures. Compare the new result with the prior recorded baseline when one exists.

For model-backed development runs, record the runtime/model identity, case count, aggregate metrics, important per-case outcomes, and whether the result is development evidence or a frozen evaluation result.

#### 7E. Verification decision
Only call behavior **Verified** when all required applicable stages are green. A failed stage returns the workflow to current-phase failure analysis; preserve the failed result rather than rewriting history.

### 8. Review for drift
Before completion ask:

- Did this expand product scope?
- Did AI absorb deterministic logic?
- Did a rule lose provenance?
- Did we introduce unnecessary infrastructure?
- Did any real patient/PHI data, credentials, or secrets enter the repository?
- Did we silently answer an open question or cross a release gate?

### 9. Synchronize all affected files
A task is not complete when only the primary implementation file is correct. Use the change matrix in `docs/FILE_MAP.md` to identify the affected set, then update every repository file whose truth, path, interface, example, test expectation, or project state is materially affected by the change.

Check and update, when applicable:

- Runtime/source files.
- Tests and test helpers.
- Development/evaluation fixtures.
- Prompts and rules.
- README, file maps, architecture, data model, terminology, scope, benchmark, security, and release-gate documentation.
- `docs/BASELINE_RESULTS.md` when a named development/model baseline was actually run.
- `docs/IMPLEMENTATION_STATUS.md` when status/work state changed.
- `docs/DECISIONS.md` only for explicitly settled decisions.
- `docs/OPEN_QUESTIONS.md` when an open question was explicitly resolved, became current, or a new blocker was discovered.
- GitHub issue/PR body or checklist state for tracked work.
- Agent/skill instructions when repository structure or workflow changed.

If `docs/FILE_MAP.md` identifies a companion file and it is intentionally not modified, verify that its existing content is still accurate. Do not touch unrelated files merely to create churn. "All files" means all files materially affected by the command.

Passing verification is not the end of the task. After required tests pass, continue automatically through synchronization, gate/status evaluation, stale-reference search, issue/PR updates, and final repository review.

### 10. Evaluate the active gate
After required verification and synchronization evidence exist, compare the result directly with `docs/RELEASE_GATES.md`.

- If gate criteria are not met, keep the current phase/gate open and record the exact remaining failure.
- If gate criteria are met and no required human review/approval remains unresolved, update `docs/IMPLEMENTATION_STATUS.md` to the next phase/gate and synchronize the completed/current issue state.
- If a human decision is required for the next work item, advance only as far as the evidence allows, record the new blocker in project truth, and stop before making that decision on the user's behalf.

### 11. Search for stale references
Search the repository for names, paths, interfaces, terminology, status claims, pending-verification wording, or assumptions changed by the task. Fix stale references before completion.

Examples include:

- Renamed files/directories still referenced in docs.
- Old class/function/interface names in tests or examples.
- A status document still saying Not Started after verified implementation.
- A GitHub issue checklist that no longer reflects completed work.
- A baseline document still saying rerun pending after the rerun was supplied.
- A benchmark or fixture path that points to a previous folder name.

### 12. Final repository review
Review the complete diff/status, not only the file you intended to edit.

Confirm:

- The applicable `docs/FILE_MAP.md` change-matrix row was followed.
- Every affected companion file is synchronized.
- Tests/verification reflect the final state.
- Baseline/status/gate claims match the actual verification evidence.
- Tracked issue/PR state matches project truth.
- No stale references remain.
- No unrelated changes were accidentally included.

### 13. Finish cleanly
Commit only coherent verified work with a descriptive message. Report what changed, what was verified, the resulting phase/gate state, and any remaining human-decision blocker.

## Status vocabulary

- **Not Started** — no meaningful design or implementation.
- **Designed** — behavior/architecture is defined but not implemented.
- **Built** — implementation exists.
- **Integrated** — implementation participates in the real signal path.
- **Verified** — all required applicable verification stages demonstrate intended behavior.

## Default development principle

ClaimLens earns complexity through demonstrated need, not possibility.
