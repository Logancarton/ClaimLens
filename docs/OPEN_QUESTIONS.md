# Open Questions

These questions are intentionally unresolved. Do not silently decide them inside implementation code.

## Product

- Is the first paid user an individual psychiatric clinician, a group practice, a billing company, or a health system?
- Is ClaimLens first sold as software, an AI-assisted audit service, or both?
- Does the first workflow run before note signing, before claim submission, or both?

## Billing scope

- Which exact service/code families constitute the first benchmark?
- Which provider types are in scope for version 1?
- Which payer is the first payer-specific overlay after base logic?

## Evidence

- What is the minimum evidence schema for the first supported service family?
- How should copied-forward historical content be distinguished from current encounter evidence?
- What confidence/ambiguity states should trigger mandatory human review?

## AI

- Which local model becomes the first baseline evidence extractor?
- Should the auditor use the same model with a separate prompt or a genuinely independent model/process?
- At what measured failure point would fine-tuning be justified?

## Product operations

- What result format is most useful to clinicians/billers?
- How will rule updates be reviewed and released?
- What customer-level ROI metric becomes the primary commercial proof?

## Deferred integration

- Which clearinghouse/eligibility integration is most practical for insurance verification?
- How will provider network participation be sourced authoritatively?
