"""ClaimLens runtime orchestration entry point.

PURPOSE
    Sequence approved ClaimLens components through the canonical workflow.

OWNS
    Thin runtime orchestration and handoff order only.

DOES NOT OWN
    Evidence interpretation, billing rules, claim decisions, auditing logic,
    payer policy, or presentation rules.

SIGNAL FLOW
    Encounter → Evidence → Rules → Candidate Claim → Audit → Payer → Result

STATUS
    Phase 0 structural placeholder. Do not implement runtime behavior before Gate 0.
"""
