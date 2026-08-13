# Use Cases

## UC-1 — Pre-sign evidence audit

A clinician provides an encounter before signing. ClaimLens identifies the billing-relevant evidence actually present, missing, ambiguous, contradictory, or temporally unclear.

Value: surface documentation weakness while the clinician still controls the note, without inventing or proposing unsupported facts.

## UC-2 — Pre-submit claim-readiness audit

A clinician or billing reviewer provides the finalized encounter before claim submission. ClaimLens evaluates what the signed record actually supports and identifies missing support, ambiguity, contradictions, or rule conflicts.

Value: prevent unsupported or avoidably weak claims from being submitted.

## UC-3 — Candidate claim compilation

ClaimLens converts supported evidence plus validated rules into a candidate claim and shows the evidence/rules supporting each candidate service.

Value: reduce manual coding effort while preserving defensibility.

## UC-4 — Claim challenge

An independent auditor challenges the compiled claim and can downgrade it to review when support is weak, contradictory, incomplete, or temporally unclear.

Value: reduce unsupported billing and audit exposure.

## UC-5 — Missed supported-service detection

ClaimLens may identify a documented service that appears supported but was omitted from the proposed claim. It must show the evidence rather than simply recommending the highest-paying option.

Value: reduce preventable underbilling without turning ClaimLens into a revenue maximizer.

## UC-6 — Payer-specific validation

After the base compiler is reliable, ClaimLens applies a payer-specific overlay and identifies additional requirements or conflicts.

Value: reduce payer-specific denials.

## Deferred use cases

### Insurance intake and verification
Insurance-card/ID extraction, payer resolution, provider-network matching, and live eligibility.

### Denial root-cause analysis
Analyze claim outcomes and denial reasons to find repeated preventable failure patterns.

### EHR / clearinghouse integration
Receive encounter data and return claim-readiness information within an operational workflow.
