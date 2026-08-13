# ClaimLens Autonomy Policy

## Purpose

Enable AI coding/review agents to continue ClaimLens work with minimal supervision without silently changing product truth, billing policy, safety boundaries, or phase gates.

This file governs **work selection and stop conditions**. It does not define product scope, billing rules, or release criteria.

## Authority model

Use these sources for different kinds of truth:

- `docs/PRODUCT_SCOPE.md` and `docs/MVP_DEFINITION.md` — what the product is and the current finish line.
- `docs/ARCHITECTURE.md` and `docs/DATA_MODEL.md` — component ownership and system structure.
- `docs/BILLING_SCOPE.md` and `docs/RULE_GOVERNANCE.md` — billing territory and rule authority.
- `docs/IMPLEMENTATION_STATUS.md` — **current phase, current gate, and actual maturity**.
- `docs/RELEASE_GATES.md` — evidence required to advance phases.
- `docs/DECISIONS.md` — settled decisions.
- `docs/OPEN_QUESTIONS.md` — unresolved questions; never silently answer one in code.
- GitHub issues — the work queue. An issue does not override a release gate or project decision.

If two authoritative sources conflict, stop substantive work and surface the conflict. Do not choose the convenient interpretation.

## Autonomous work-selection loop

1. Read `AGENTS.md` and the required project-truth documents.
2. Read `docs/IMPLEMENTATION_STATUS.md` to identify the current phase and gate.
3. Read `docs/OPEN_QUESTIONS.md` for unresolved items relevant to that phase.
4. Fetch open GitHub issues.
5. Select the highest-priority unblocked issue that belongs to the current phase.
6. Confirm the requested change is allowed by the current gate and does not require a human decision below.
7. Follow the ClaimLens development workflow skill.
8. Verify behavior, review drift, synchronize project truth, and finish cleanly.
9. If no eligible work remains, stop and report the exact blocker rather than starting a later phase.

## Work an agent may do autonomously

When consistent with the current phase/gate and an approved requirement or issue, an agent may:

- Clean up paths, references, naming, and documentation ownership without changing meaning.
- Add or improve tests for already-defined behavior.
- Create synthetic development fixtures that do not settle an unresolved product/billing question.
- Implement behavior already unambiguously specified by project truth and the current issue.
- Fix defects where expected behavior is already defined.
- Refactor without changing externally defined behavior when verification remains green.
- Update `IMPLEMENTATION_STATUS.md` when repository evidence clearly supports the status change.
- Record a decision in `DECISIONS.md` when the decision was explicitly made by the human owner or is an exact consequence of already-settled project truth.

## Human decision required — stop conditions

Stop and request human judgment before doing any of the following unless an existing explicit decision already settles it:

- Expand, narrow, or materially reinterpret product scope or the MVP finish line.
- Select the first customer/workflow when alternatives materially change v0.1.
- Select or expand a billing/service family.
- Resolve conflicting, ambiguous, or unsupported billing-policy interpretations.
- Treat a secondary/AI summary as authoritative when a rule requires authoritative sourcing.
- Choose benchmark acceptance thresholds that determine success, failure, release, pilot, or stop decisions.
- Advance a phase or declare a release gate satisfied when a required human review/approval remains unresolved.
- Introduce real PHI, production clinical data, or a new production data-handling workflow.
- Add an external integration, vendor dependency, paid service, contract-dependent data source, or licensed/proprietary content commitment.
- Introduce major architecture not required by an approved current-phase problem, including agent networks, vector databases, custom model training, or new infrastructure layers.
- Delete or rewrite benchmark evidence, failed experiments, rule provenance, decision history, or other records in a way that could hide prior evidence.

## Fail-closed behavior

When uncertain whether work is authorized:

- Preserve the current state.
- Do not silently guess.
- Add or update an open question when appropriate.
- Report the smallest decision needed to continue.

A blocked agent should return a precise blocker, not create substitute work in a later phase.

## Phase advancement rule

A later-phase GitHub issue may exist before it is eligible. Eligibility comes from `docs/IMPLEMENTATION_STATUS.md` plus `docs/RELEASE_GATES.md`, not issue existence or issue number.

A phase advances only when its gate evidence is present and all required human decisions for that gate are resolved.
