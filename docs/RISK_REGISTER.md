# Risk Register

This is a living list of failure modes that could make ClaimLens unsafe, commercially weak, or untrustworthy.

| Risk | Why it matters | Primary control |
|---|---|---|
| Hallucinated evidence | Could support a claim with facts absent from the record | Structured extraction, provenance, ambiguity states, benchmark hallucination rate |
| Overcoding bias | Commercial incentives could push the system toward unsupported higher billing | Objective is defensibility, not maximum payment; independent auditor |
| Undercoding / missed support | Product may fail to deliver financial value | Measure missed-supported-service rate |
| Stale billing rules | Correct behavior can become wrong over time | Rule provenance, effective dates, verification dates, superseded state |
| Payer variability | A generally correct claim may fail payer-specific requirements | Base rules separated from payer overlays |
| Rule/model boundary collapse | Probabilistic output could masquerade as policy | Deterministic rule layer and rule governance |
| False confidence | Users may over-trust an uncertain output | Explicit review state and explainable support |
| PHI exposure | Could create severe operational/legal risk | Synthetic-only repo; production security designed before PHI |
| Proprietary/licensed content misuse | Could create product/legal problems | Store/use only material ClaimLens has rights to use |
| Benchmark leakage | Tuning against evaluation cases can create fake progress | Separate development and frozen evaluation sets |
| Scope drift | Project could become a general healthcare AI before core value is proven | Product scope, MVP definition, architecture steward |
| Integration dependency | External APIs can dominate development before core value exists | Integrations deferred until compiler is verified |
| Model dependency | Product may become tied to one vendor/model | Constrained model interface and benchmark-based model replacement |
| Poor commercial ROI | Technically correct product may still not be worth buying | Measure denial risk reduction, review time, supported revenue capture, and operational savings |

Add a risk when a new failure mode is discovered; do not hide it inside implementation notes.
