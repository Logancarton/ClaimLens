# File Map — ClaimLens Maintenance Key

This file is the master key for deciding **where work belongs, which companion files must be checked, and what should be updated when something changes**.

Use `docs/INDEX.md` to understand the project-truth reading order. Use this file when making or finishing a change.

## How to use this key

For every task:

1. Identify what kind of thing changed.
2. Use the change matrix below to find the files that must be checked.
3. Update only the files whose truth is materially affected.
4. Before finishing, search for stale paths, names, interfaces, examples, assumptions, tests, fixtures, issue text, or status references.
5. A task is not complete until the affected set is synchronized.

## Change → files to check

| If this changes... | Always check these files/areas |
|---|---|
| Product purpose, boundary, or target user | `PRODUCT_SCOPE.md`, `USE_CASES.md`, `MVP_DEFINITION.md`, `PRODUCT_REQUIREMENTS.md`, `COMMERCIAL_MODEL.md`, `DECISIONS.md` |
| MVP finish line | `MVP_DEFINITION.md`, `PRODUCT_REQUIREMENTS.md`, `RELEASE_GATES.md`, `IMPLEMENTATION_STATUS.md`, active issue |
| Concrete user workflow/use case | `USE_CASES.md`, `PRODUCT_SCOPE.md`, `MVP_DEFINITION.md`, `PRODUCT_REQUIREMENTS.md`, `ARCHITECTURE.md` if ownership changes |
| Architecture or signal flow | `ARCHITECTURE.md`, `DATA_MODEL.md`, `FILE_MAP.md`, owning `src/` modules, tests, `DECISIONS.md` |
| Data object/schema/field | `DATA_MODEL.md`, `ARCHITECTURE.md`, owning `src/` module, tests, fixtures, benchmark expectations, `TERMINOLOGY.md` if vocabulary changes |
| Canonical term/name | `TERMINOLOGY.md`, repository-wide references, docs, source comments/interfaces, tests, fixtures, issue/PR text |
| Billing/service scope | `BILLING_SCOPE.md`, `RULE_GOVERNANCE.md`, `BENCHMARK_PLAN.md`, `MVP_DEFINITION.md` if v0.1 changes, `DECISIONS.md` |
| Billing rule or rule source | rule definition under `rules/`, `RULE_GOVERNANCE.md`, rule tests, benchmark cases, provenance/source metadata |
| Evidence extraction behavior/schema | `DATA_MODEL.md`, `ARCHITECTURE.md`, `src/claimlens/evidence.py`, prompts, tests, development fixtures, benchmark expectations |
| Encounter input contract | `DATA_MODEL.md`, `ARCHITECTURE.md`, `src/claimlens/encounter.py`, tests, fixtures |
| Claim compilation behavior | `ARCHITECTURE.md`, `src/claimlens/compiler.py`, rule/evidence interfaces, tests, benchmark expectations |
| Audit behavior/finding taxonomy | `ARCHITECTURE.md`, `src/claimlens/auditor.py`, tests, benchmark expectations, `TERMINOLOGY.md` if terms change |
| Payer overlay behavior | `BILLING_SCOPE.md`, `RULE_GOVERNANCE.md`, `src/claimlens/payer.py`, rules, tests, security/integration docs when relevant |
| Final result/status contract | `DATA_MODEL.md`, `src/claimlens/result.py`, `main.py` if orchestration changes, tests, benchmark outputs |
| Runtime orchestration | `ARCHITECTURE.md`, `src/claimlens/main.py`, affected component interfaces, integration tests |
| Prompt/model instruction | file under `prompts/`, evidence/auditor interface as applicable, tests, benchmark cases; never treat prompt text as billing authority |
| Test expectation | owning behavior, relevant fixtures, benchmark plan if evaluation meaning changed |
| Development fixture | `data/development_cases/`, owning tests/behavior only; do not silently modify frozen evaluation cases |
| Evaluation fixture/benchmark truth | `data/evaluation_cases/`, `BENCHMARK_PLAN.md`, `RELEASE_GATES.md`, benchmark outputs; require explicit justification before changing frozen truth |
| Benchmark metric/threshold | `BENCHMARK_PLAN.md`, `RELEASE_GATES.md`, `IMPLEMENTATION_STATUS.md` if gate state changes, `DECISIONS.md` when explicitly approved |
| Security/PHI handling | `SECURITY_AND_DATA.md`, `.gitignore`, architecture/data flow, dependencies/integrations, risk register |
| Dependency/environment requirement | `requirements.txt`, `.env.example`, architecture/security docs if material, README/setup instructions if user-visible |
| File/folder path or repository structure | `FILE_MAP.md`, `docs/INDEX.md` if navigation changes, `AGENTS.md`, relevant skill files, README/tests/docs references, repository-wide stale-path search |
| Agent/workflow behavior | `AGENTS.md`, relevant `.agents/` file or skill, `FILE_MAP.md` when maintenance behavior changes |
| Risk discovered/retired | `RISK_REGISTER.md`, affected requirement/architecture/security/benchmark docs when truth changes |
| Open question resolved | `OPEN_QUESTIONS.md`, `DECISIONS.md`, every document/code path whose truth changes because of the answer |
| Component maturity/status | `IMPLEMENTATION_STATUS.md`, tests/benchmark evidence, active issue/PR checklist |
| Phase/gate advancement | `IMPLEMENTATION_STATUS.md`, `RELEASE_GATES.md`, active issue/PR, unresolved gate-related open questions |
| Commercial/ROI assumption | `COMMERCIAL_MODEL.md`, `PRODUCT_SCOPE.md` or requirements if product behavior changes, risk register when relevant |

## Project-truth document key

### `PRODUCT_SCOPE.md`
**Purpose:** Defines what ClaimLens is, who it is for, the objective, inputs/outputs, and hard product boundaries.

**Update when:** Product purpose, target user, product boundary, major input/output class, or deferred capability materially changes.

**Check with:** `USE_CASES.md`, `MVP_DEFINITION.md`, `PRODUCT_REQUIREMENTS.md`, `COMMERCIAL_MODEL.md`, `DECISIONS.md`.

**Do not use for:** Implementation status, detailed architecture, billing-rule logic, or temporary experiments.

### `USE_CASES.md`
**Purpose:** Defines concrete jobs and workflows ClaimLens must perform.

**Update when:** A supported workflow is added, removed, narrowed, or materially redefined.

**Check with:** `PRODUCT_SCOPE.md`, `MVP_DEFINITION.md`, `PRODUCT_REQUIREMENTS.md`, `ARCHITECTURE.md`.

**Do not use for:** Low-level implementation detail or future ideas that are not accepted use cases.

### `MVP_DEFINITION.md`
**Purpose:** Defines the exact v0.1 finish line and what is explicitly not required.

**Update when:** The v0.1 finish line changes by explicit human decision.

**Check with:** `PRODUCT_SCOPE.md`, `PRODUCT_REQUIREMENTS.md`, `RELEASE_GATES.md`, `IMPLEMENTATION_STATUS.md`.

**Do not use for:** General long-term roadmap or component status.

### `PRODUCT_REQUIREMENTS.md`
**Purpose:** Defines functional and non-functional requirements ClaimLens must satisfy.

**Update when:** A requirement is added, removed, clarified, reprioritized, or materially changes acceptance behavior.

**Check with:** scope, use cases, MVP, architecture, tests/benchmark.

**Do not use for:** Recording whether a requirement is already built; use `IMPLEMENTATION_STATUS.md` for that.

### `COMMERCIAL_MODEL.md`
**Purpose:** Defines the intended customer value, revenue/ROI logic, and commercial assumptions.

**Update when:** Buyer, delivery model, value proposition, pricing logic, or ROI assumptions materially change.

**Check with:** `PRODUCT_SCOPE.md`, `USE_CASES.md`, `RISK_REGISTER.md`.

**Do not use for:** Technical implementation decisions unless they materially change the commercial model.

### `ARCHITECTURE.md`
**Purpose:** Defines canonical signal flow, component boundaries, ownership, and architectural invariants.

**Update when:** A component responsibility, handoff, signal path, interface boundary, or major structural decision changes.

**Check with:** `DATA_MODEL.md`, `FILE_MAP.md`, owning source files, tests, `DECISIONS.md`.

**Do not use for:** Temporary coding notes or implementation status.

### `DATA_MODEL.md`
**Purpose:** Defines the core objects, fields, relationships, provenance, and states ClaimLens understands.

**Update when:** A domain object, schema, field, relationship, state, or provenance contract changes.

**Check with:** architecture, terminology, owning source file, tests, fixtures, benchmark.

**Do not use for:** Billing-policy prose or runtime status.

### `TERMINOLOGY.md`
**Purpose:** Defines canonical project vocabulary so docs, code, tests, and agents use the same language.

**Update when:** A canonical term is introduced, renamed, deprecated, or clarified.

**Check with:** repository-wide stale-term search.

**Do not use for:** Long explanations of architecture or billing rules.

### `BILLING_SCOPE.md`
**Purpose:** Defines the billing territory, service families, provider/workflow scope, and payer sequencing ClaimLens is allowed to address.

**Update when:** Supported billing territory or service family changes by explicit decision.

**Check with:** `RULE_GOVERNANCE.md`, `BENCHMARK_PLAN.md`, MVP, rules, `DECISIONS.md`.

**Do not use for:** Individual rule implementation or AI-generated interpretations.

### `RULE_GOVERNANCE.md`
**Purpose:** Defines how billing rules are sourced, verified, versioned, tested, activated, superseded, and trusted.

**Update when:** Rule authority, provenance requirements, lifecycle, conflict handling, or governance process changes.

**Check with:** `BILLING_SCOPE.md`, `rules/`, tests, benchmark, security/licensing concerns.

**Do not use for:** The actual content of a specific executable rule.

### `BENCHMARK_PLAN.md`
**Purpose:** Defines how ClaimLens correctness is evaluated, including case families, splits, metrics, and benchmark discipline.

**Update when:** Evaluation design, metric definitions, case taxonomy, data split meaning, or explicitly approved thresholds change.

**Check with:** evaluation fixtures, tests, `RELEASE_GATES.md`, `IMPLEMENTATION_STATUS.md`.

**Do not use for:** Development-only examples or silently moving success thresholds after results are known.

### `RELEASE_GATES.md`
**Purpose:** Defines the evidence required before advancing phases/releases.

**Update when:** Gate criteria change by explicit decision or a new phase/release gate is introduced.

**Check with:** benchmark plan, status, active issue/PR, open questions.

**Do not use for:** Claiming a gate passed without evidence; actual state belongs in `IMPLEMENTATION_STATUS.md`.

### `RISK_REGISTER.md`
**Purpose:** Records known product, clinical/billing-safety, technical, data, commercial, and dependency risks plus mitigations.

**Update when:** A material risk appears, changes, is mitigated, or is retired.

**Check with:** the document/component responsible for the mitigation.

**Do not use for:** General brainstorming with no actionable project risk.

### `SECURITY_AND_DATA.md`
**Purpose:** Defines data classes, PHI boundaries, secret handling, repository safety, and future production-data requirements.

**Update when:** Data flow, storage, PHI handling, secret handling, integration, hosting, retention, or security assumptions change.

**Check with:** architecture, `.gitignore`, dependencies/integrations, risk register.

**Do not use for:** Billing-policy interpretation.

### `IMPLEMENTATION_STATUS.md`
**Purpose:** Single source of truth for current phase, current gate, allowed/blocked work, and actual component maturity.

**Update when:** Repository evidence changes what is built, integrated, verified, allowed, blocked, or the current phase/gate.

**Check with:** tests, benchmark evidence, `RELEASE_GATES.md`, active issue/PR.

**Do not use for:** Future plans, guesses, or proposed capabilities.

### `DECISIONS.md`
**Purpose:** Records settled product, architecture, governance, or other durable decisions.

**Update when:** The human owner explicitly settles a material question, or the entry is an exact consequence of already-settled project truth.

**Check with:** every document affected by the decision.

**Do not use for:** Unresolved alternatives, speculation, or silently inferred decisions.

### `OPEN_QUESTIONS.md`
**Purpose:** Preserves unresolved decisions and blockers so agents do not silently answer them in code.

**Update when:** A new material unresolved question appears, an existing one is explicitly resolved, or blocking relevance changes.

**Check with:** current phase/gate and the documents that the answer would affect.

**Do not use for:** Questions already settled in `DECISIONS.md`.

### `FILE_MAP.md`
**Purpose:** This maintenance key: where work belongs, which files depend on which changes, and what must be synchronized before completion.

**Update when:** A file/folder is added, removed, renamed, changes responsibility, or the repository maintenance/update rules change.

**Check with:** `docs/INDEX.md`, `AGENTS.md`, relevant `.agents/` skills, repository-wide path/reference search.

**Do not use for:** Product policy or implementation status itself.

## Root and folder ownership

### Root
- `README.md` — one-page identity and core signal flow.
- `ROADMAP.md` — high-level build order and milestones.
- `AGENTS.md` — mandatory instructions for AI coding/review agents.
- `requirements.txt` — Python dependencies once actually needed.
- `.env.example` — environment-variable names only, never secrets.
- `.gitignore` — source-control exclusions and PHI/secret guardrails.

### `docs/`
Project-truth layer. Start with `docs/INDEX.md`; use this file as the maintenance/update key.

### `src/claimlens/`
Runtime implementation owned by the ClaimLens product namespace.

- `main.py` — thin orchestration and sequencing.
- `encounter.py` — encounter input contract, normalization, validation, source preservation.
- `evidence.py` — structured evidence models/extraction interface, provenance, uncertainty, contradiction handling.
- `rules.py` — deterministic rule loading/evaluation interface and traceability.
- `compiler.py` — candidate-service/claim construction from evidence + rule results.
- `auditor.py` — independent adversarial review and audit findings.
- `payer.py` — payer-specific overlays after base support is established.
- `result.py` — final result/status structures, traceability, serialization/presentation boundary.

### `rules/`
Human-reviewable executable billing-rule definitions. See `rules/README.md` and `docs/RULE_GOVERNANCE.md`.

### `prompts/`
Versioned model instructions. Prompts interpret/extract/challenge; they are never authoritative billing rules.

### `data/`
Synthetic development and benchmark fixtures only. See `data/README.md`.

- `data/development_cases/` — cases agents may inspect, change, and tune against.
- `data/evaluation_cases/` — frozen known-answer holdout cases once a benchmark version is frozen.

### `tests/`
Automated behavioral checks. See `tests/README.md`.

### `output/`
Generated local results. Contents are ignored except repository placeholders.

### `.agents/`
Project-specific AI governance and workflow guidance.

- `.agents/AUTONOMY_POLICY.md` — autonomous work selection, authority, stop conditions.
- `.agents/ARCHITECTURE_STEWARD.md` — product/architecture boundary protection.
- `.agents/skills/` — reusable ClaimLens workflows.

## Completion rule

Before declaring a task complete, use the change matrix above to identify the affected set, synchronize those files, then search for stale references. If a relevant companion file is intentionally not changed, its existing truth must still remain accurate.
