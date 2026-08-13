"""Independent adversarial claim-audit boundary.

PURPOSE
    Challenge a compiled candidate claim for unsupported assumptions, missing
    requirements, contradictions, weak evidence, and rule conflicts.

OWNS
    Structured audit findings, defect categorization, and downgrade/escalation
    recommendations such as REVIEW when support is not defensible.

DOES NOT OWN
    Repairing missing documentation, inventing evidence, silently changing rules,
    or rebuilding the candidate claim to force a supported result.

SIGNAL FLOW
    Candidate Claim → Adversarial Audit → Audit Findings

STATUS
    Phase 0 structural placeholder. Audit behavior is not implemented yet.
"""
