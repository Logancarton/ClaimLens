# ClaimLens

ClaimLens is a healthcare claim-compilation and pre-submission audit system.

Its core purpose is to determine what a clinical encounter actually supports, convert that evidence into a defensible candidate claim, and challenge the claim before a human approves it.

## Core signal flow

Clinical encounter → evidence extraction → structured evidence → billing rules → candidate claim → adversarial audit → payer validation → human review.

## Initial product boundary

ClaimLens starts with outpatient psychiatric billing. The first version focuses on evidence extraction, rule-based claim support, candidate claim compilation, and audit findings. It does not diagnose patients, recommend treatment, invent missing documentation, maximize billing regardless of support, submit claims autonomously, or handle live insurance eligibility.

## Project truth

Start with `docs/INDEX.md`. It defines the reading order for scope, MVP, requirements, architecture, rules, benchmarks, release gates, risks, security, status, and decisions.

## Development rule

ClaimLens only earns complexity when a demonstrated billing problem requires it. The first objective is not a custom AI architecture. The first objective is a reliable, measurable claim-compilation workflow.

## v0.1 finish line

One synthetic outpatient psychiatric encounter can travel through:

`Encounter → Evidence → Rules → Candidate Claim → Audit → Result`

with traceable support, safe uncertainty, and reproducible known-answer verification.
