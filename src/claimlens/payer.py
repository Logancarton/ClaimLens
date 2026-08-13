"""Payer-specific validation boundary.

PURPOSE
    Apply versioned payer-specific overlays after base evidence and billing-rule
    support have been established.

OWNS
    Payer-profile requirements, payer-specific conflicts, and overlay results.

DOES NOT OWN
    Altering source evidence, redefining base billing logic, live eligibility,
    network verification, or unsupported payer assumptions.

SIGNAL FLOW
    Audited Candidate Claim → Payer Validation → Payer Findings

STATUS
    Phase 0 structural placeholder. Payer overlays are deferred and not implemented.
"""
