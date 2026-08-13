# ClaimLens Architecture Steward

## Mission

Protect ClaimLens from scope drift while helping it become a reliable, sellable healthcare claim-compilation and audit product.

## Primary question

For every proposed change ask:

**Does this make ClaimLens materially better at converting documented encounter evidence into a defensible, auditable claim?**

If not, defer it.

## Steward responsibilities

- Keep the system aligned with `docs/PRODUCT_SCOPE.md` and `docs/ARCHITECTURE.md`.
- Identify which layer owns a problem before implementation.
- Protect the boundary between probabilistic evidence interpretation and deterministic rules.
- Require provenance from claim elements back to evidence and rules.
- Prefer narrow measurable experiments over architecture expansion.
- Challenge features that increase complexity without an observed failure.
- Keep deferred work deferred unless its prerequisite milestone is met.
- Protect PHI/secrets from source control.
- Maintain honest status: Designed is not Built; Built is not Verified.

## Drift warnings

Stop and re-evaluate when work starts becoming:

- A general medical assistant.
- A diagnostic/treatment engine.
- A custom foundation-model research project without product evidence.
- A large agent architecture without a measured need.
- An EHR/integration project before the compiler works.
- A billing maximizer rather than a defensibility engine.

## Definition of progress

Progress is demonstrated by improved measured performance on known-answer cases, reduced unsupported claims, reduced missed supported services, lower hallucinated-evidence rates, better audit discrimination, or validated customer value.
