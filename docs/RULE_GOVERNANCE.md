# Rule Governance

Billing rules are executable policy knowledge. They require stronger provenance than prompts or model output.

## Source hierarchy

Prefer authoritative primary sources for production rules. Secondary summaries may help interpretation but must not silently become the authoritative basis of an executable rule.

## Minimum metadata for a production rule

Every production rule should eventually identify:

- Rule ID.
- Rule title/purpose.
- Jurisdiction or payer.
- Service/code family affected.
- Applicable provider class and care setting when relevant.
- Authoritative source reference.
- Source version/effective date when available.
- Date ClaimLens verified the source.
- Logical conditions.
- Result when conditions pass/fail/are ambiguous.
- Tests exercising the rule.

## Rule states

A rule may be:

- Draft.
- Source Verified.
- Implemented.
- Tested.
- Active.
- Superseded.

## AI boundary

A language model may extract evidence, explain a rule, or help translate a source into a draft representation. It is not itself the authoritative rule source.

## Conflict handling

When two sources appear to conflict, ClaimLens must not silently choose. Record the conflict, identify scope/effective-date differences if known, and require resolution before activating the rule.

## Licensed/proprietary material

Do not commit proprietary or licensed coding content merely because it is accessible to a developer. Only include material ClaimLens has the right to store/use. Rule logic and source references should be separated from licensed display content where appropriate.
