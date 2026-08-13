# ClaimLens

ClaimLens is a healthcare claim-compilation and pre-submission audit system.

Its core purpose is to determine what a clinical encounter actually supports, convert that evidence into a defensible candidate claim, and challenge the claim before a human approves it.

## Core signal flow

Clinical encounter → evidence extraction → structured evidence → billing rules → candidate claim → adversarial audit → payer validation → human review.

## Initial product boundary

ClaimLens starts with outpatient psychiatric billing. The first version focuses on evidence extraction, rule-based claim support, candidate claim compilation, and audit findings. It does not diagnose patients, recommend treatment, invent missing documentation, maximize billing regardless of support, submit claims autonomously, or handle live insurance eligibility.

## Repository truth

Read these before changing architecture:

1. `docs/PRODUCT_SCOPE.md`
2. `docs/ARCHITECTURE.md`
3. `docs/BILLING_SCOPE.md`
4. `docs/DATA_MODEL.md`
5. `docs/IMPLEMENTATION_STATUS.md`
6. `docs/DECISIONS.md`
7. `AGENTS.md`
8. `.agents/skills/claimlens-development-workflow/SKILL.md`

## Development rule

ClaimLens only earns complexity when a demonstrated billing problem requires it. The first objective is not a custom AI architecture. The first objective is a reliable, measurable claim-compilation workflow.
