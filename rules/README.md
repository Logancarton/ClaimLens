# Rules

This directory is the single repository home for human-reviewable billing and payer rule definitions.

- `medicare/` — Medicare-specific rules.
- `arizona/` — Arizona-specific requirements that materially affect ClaimLens behavior, including AHCCCS where applicable.
- `commercial/` — commercial payer overlays, separated by payer only after a payer is deliberately selected.

See `docs/RULE_GOVERNANCE.md` before adding production rules.

Prompts are not rules. Model output is not a rule source.

## What this README is

This file is a **source-discovery and rule-challenge map**. It identifies authoritative or first-party places to research a proposed rule. A source being listed here does **not** mean:

- the source applies to every plan, provider, service, or date of service;
- a specific rule has been source verified;
- a service or code family has been selected for the v0.1 benchmark;
- a commercial payer has been selected for an active overlay; or
- the source may be copied into ClaimLens without regard to licensing or access restrictions.

Every executable rule still needs the provenance and lifecycle metadata required by `docs/RULE_GOVERNANCE.md`.

**Source-map verification date:** 2026-08-12. Individual rule effective dates must be verified separately.

## Rule challenge checklist

Before a proposed rule can move beyond `Draft`, challenge it against these questions:

1. **Authority:** Is the source the organization that actually owns or administers the requirement, rather than a blog, coding summary, search result, or AI answer?
2. **Applicability:** Does it apply to the exact payer/program, product or plan, jurisdiction, provider type, service family, place of service, and modality being evaluated?
3. **Effective date:** Was the source in force for the date of service, and has it been revised, replaced, archived, or superseded?
4. **Rule type:** Is the source describing coding, coverage, medical necessity, reimbursement, claims processing, authorization, or a contractual requirement? Do not silently treat one category as another.
5. **Higher-priority terms:** For commercial coverage, does a member-specific plan document, provider contract, state/federal law, or product-specific policy control over a general policy?
6. **Conflicts:** Does another authoritative source disagree? If so, preserve the conflict and require human resolution before activation.
7. **Licensing/access:** Is the underlying content public and reusable, or is it licensed, copyrighted, contract-restricted, or portal-restricted?
8. **Traceability:** Can ClaimLens record the source URL/reference, title, version/effective date, verification date, and the exact proposition the source supports?

If any material answer is unknown, the rule remains `Draft` or produces `REVIEW`; uncertainty is not permission to infer a billing requirement.

## Cross-payer coding authorities

These sources help establish the underlying coding vocabulary before payer-specific overlays are considered.

### American Medical Association — CPT

- CPT coding resources: https://www.ama-assn.org/practice-management/cpt/cpt-coding-resources
- CPT licensing FAQ: https://www.ama-assn.org/practice-management/cpt/cpt-licensing-frequently-asked-questions-faqs

CPT content is copyrighted/licensed material. Do not copy a CPT data file, descriptors, or other licensed content into this repository merely because ClaimLens needs to reason about CPT-coded services. Licensing must be resolved for the intended product use before restricted CPT content is incorporated.

### CMS — HCPCS and Medicare coding infrastructure

- CMS HCPCS quarterly updates: https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system/quarterly-update
- CMS Internet-Only Manuals: https://www.cms.gov/medicare/regulations-guidance/manuals/internet-only-manuals-ioms

## Medicare sources — `rules/medicare/`

Use CMS first, then the applicable Medicare Administrative Contractor (MAC) when local Medicare guidance is relevant. Do not use a commercial payer's interpretation as the authority for a Medicare rule.

### Claims processing and payment

- Medicare Claims Processing Manual, Publication 100-04, including Chapter 12 for physicians/nonphysician practitioners: https://www.cms.gov/regulations-and-guidance/guidance/manuals/internet-only-manuals-ioms-items/cms018912
- Medicare Physician Fee Schedule Look-Up Tool: https://www.cms.gov/medicare/physician-fee-schedule/search
- CMS Physician Information Center: https://www.cms.gov/physician-information-center

### Coverage and local policy

- Medicare Coverage Database (NCDs, LCDs, and related articles): https://www.cms.gov/medicare-coverage-database/search.aspx
- CMS Medicare Administrative Contractor information: https://www.cms.gov/medicare/coding-billing/medicare-administrative-contractors-macs/who-are-macs
- Arizona is in A/B MAC Jurisdiction F; use the CMS Jurisdiction F page to verify the current contractor before relying on MAC-local guidance: https://www.cms.gov/medicare/medicare-contracting/medicare-administrative-contractors/who-are-the-macs-a-b-mac-jurisdiction-f-jf

### Correct-coding edits

- Medicare NCCI overview: https://www.cms.gov/medicare/coding-billing/national-correct-coding-initiative-ncci-edits
- Medicare NCCI Procedure-to-Procedure (PTP) edits: https://www.cms.gov/medicare/coding-billing/national-correct-coding-initiative-ncci-edits/medicare-ncci-procedure-procedure-ptp-edits
- Medicare NCCI Medically Unlikely Edits (MUEs): https://www.cms.gov/medicare/coding-billing/national-correct-coding-initiative-ncci-edits/medicare-ncci-medically-unlikely-edits-mues
- Medicare NCCI Add-on Code edits: https://www.cms.gov/medicare/coding-billing/national-correct-coding-initiative-ncci-edits/medicare-ncci-add-code-edits
- Medicare NCCI FAQ library: https://www.cms.gov/medicare/coding-billing/national-correct-coding-initiative-ncci-edits/medicare-ncci-faq-library

NCCI is a correct-coding layer, not a substitute for coverage or medical-necessity policy. Current-quarter edit files must be matched to the relevant date of service.

## Arizona sources — `rules/arizona/`

Arizona research has two distinct layers that must not be collapsed together: **AHCCCS/Arizona Medicaid** requirements and **Arizona insurance/statutory** requirements. Determine which layer governs the encounter before encoding a rule.

### AHCCCS / Arizona Medicaid

- AHCCCS provider manuals hub: https://www.azahcccs.gov/PlansProviders/RatesAndBilling/ProviderManuals/
- AHCCCS Fee-For-Service Provider Billing Manual: https://www.azahcccs.gov/PlansProviders/RatesAndBilling/FFS/providermanual.html
- AHCCCS Medical Policy Manual (AMPM): https://www.azahcccs.gov/shared/MedicalPolicyManual/
- AHCCCS guides and manuals for health plans/providers: https://www.azahcccs.gov/Resources/GuidesManualsPolicies/index.html
- AHCCCS Behavioral Health FFS Rates & Codes: https://www.azahcccs.gov/PlansProviders/RatesAndBilling/FFS/BehavioralHealthrates.html
- AHCCCS Physician Fee Schedules: https://www.azahcccs.gov/PlansProviders/RatesAndBilling/FFS/Physicianrates/index.html
- CMS Medicaid NCCI overview: https://www.cms.gov/medicare/coding-billing/ncci-medicaid
- CMS Medicaid NCCI edit files: https://www.cms.gov/medicare/coding-billing/ncci-medicaid/medicaid-ncci-edit-files

A fee-schedule listing is not itself proof of AHCCCS coverage. Validate coverage and service requirements against the applicable AHCCCS policy/manual and enrollment context. Public CMS Medicaid NCCI files are useful research references, but state Medicaid adjudication uses the applicable state implementation; do not infer AHCCCS coverage from an NCCI entry.

### Arizona law and insurance regulation

These are primary entry points for Arizona requirements that may affect claims or payer behavior. They do not automatically apply to Medicare, AHCCCS, self-funded employer plans, or every commercial product.

- Arizona Department of Insurance and Financial Institutions (DIFI) — healthcare provider grievance and timely-pay resources: https://difi.az.gov/health-care-providers
- A.R.S. § 20-3102 — timely payment of health care provider claims and grievances: https://www.azleg.gov/ars/20/03102.htm
- A.R.S. § 20-841.09 — telehealth coverage requirements for the insurer/corporation category governed by that section: https://www.azleg.gov/ars/20/00841-09.htm

Before converting an Arizona statute into a ClaimLens rule, verify the statute's exact title/article applicability, definitions, plan type, effective law, and whether federal law or a different Arizona provision controls the product being evaluated.

## Commercial payer sources — `rules/commercial/`

**No commercial payer is selected or activated by this list.** These are candidate first-party research entry points for a future payer overlay. When a payer is deliberately selected, create a payer-specific rule area and record the exact product/plan scope rather than treating the payer name as one universal rule set.

### UnitedHealthcare

- Commercial policy landing page: https://www.uhcprovider.com/en/policies-protocols/commercial-policies.html
- Commercial reimbursement policies: https://www.uhcprovider.com/en/policies-protocols/commercial-policies/commercial-reimbursement-policies.html

### Aetna

- Provider manuals, including provider/behavioral-health manuals: https://www.aetna.com/health-care-professionals/provider-education-manuals/provider-manuals.html
- Clinical Policy Bulletins: https://www.aetna.com/health-care-professionals/clinical-policy-bulletins.html

### Cigna Healthcare

- Coverage and claims resources: https://www.cigna.com/health-care-providers/coverage-and-claims
- Coverage policies: https://www.cigna.com/health-care-providers/coverage-and-claims/policies

Cigna explicitly notes that member-specific coverage-plan terms may control over a standard coverage policy. Treat this as a general commercial-payer challenge pattern: always resolve the exact plan/product before promoting a general policy into an active rule.

### Blue Cross Blue Shield of Arizona / AZ Blue

- Provider resources: https://www.azblue.com/provider/resources
- Claims and remits, including claim-submission/coding resources: https://www.azblue.com/provider/resources/claims-and-remits

Some AZ Blue provider operating guides, code-edit tools, and pricing materials are portal- or contract-restricted. Record the existence and provenance of a restricted source without copying proprietary content into Git unless ClaimLens has explicit rights to do so.

## Commercial rule activation checklist

When the human owner selects the first commercial overlay, do not begin with "payer = X" alone. Record at minimum:

- payer organization;
- product/line of business and plan/network when relevant;
- state/jurisdiction;
- provider type;
- service/code family;
- place of service and telehealth modality when relevant;
- authoritative policy/manual/contract source;
- source publication/effective date and date of service applicability;
- source verification date;
- whether the source is public, licensed, portal-restricted, or contract-specific;
- conflicts or plan-specific exceptions; and
- tests/known-answer cases required before activation.

Do not assume a private payer implements Medicare NCCI edits identically. If a commercial payer adopts or modifies an NCCI-like edit, the payer's own current policy must establish how that payer applies it.

## Research-to-rule handoff

Finding a source is the beginning of rule work, not the end. For each proposed rule:

`source discovery → applicability check → effective-date check → proposition extraction → conflict check → human review when needed → source-verified rule metadata → deterministic tests → activation`

This keeps ClaimLens able to challenge both overcoding and under-detection without allowing an AI summary, fee schedule, search result, or generic payer policy to become billing authority by accident.
