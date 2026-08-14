"""Deterministic billing-rule evaluation boundary.

PURPOSE
    Evaluate structured evidence against source-verified billing requirements.

SIGNAL FLOW
    Structured Evidence + Encounter Metadata → Rule Engine → Rule Evaluations

BOUNDARY
    Generic rule mechanics live here. Human-reviewable authoritative rule
    definitions and source propositions live under ``rules/``. The executable
    service-family helpers in this module implement only propositions already
    recorded there; prompts and model output are never rule authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Iterable

from .encounter import Encounter, PatientStatus, ProviderClass
from .evidence import EvidenceItem, EvidenceState, StructuredEvidence, TemporalScope


class RuleOutcome(str, Enum):
    """Deterministic result of evaluating one rule."""

    SUPPORTED = "SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"
    REVIEW = "REVIEW"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class RuleLifecycle(str, Enum):
    """Governance lifecycle from source discovery through activation."""

    DRAFT = "DRAFT"
    SOURCE_VERIFIED = "SOURCE_VERIFIED"
    IMPLEMENTED = "IMPLEMENTED"
    TESTED = "TESTED"
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"


@dataclass(frozen=True)
class RuleSource:
    """Traceable authoritative source metadata for a rule."""

    source_id: str
    authority: str
    title: str
    reference: str
    verified_date: str
    version: str | None = None
    effective_date: str | None = None

    def __post_init__(self) -> None:
        for name in ("source_id", "authority", "title", "reference", "verified_date"):
            value = getattr(self, name)
            if not value or not value.strip():
                raise ValueError(f"{name} is required")


@dataclass(frozen=True)
class RuleMetadata:
    """Human-reviewable identity, scope, provenance, and lifecycle for a rule."""

    rule_id: str
    title: str
    jurisdiction: str
    service_family: str
    sources: tuple[RuleSource, ...]
    lifecycle: RuleLifecycle
    provider_classes: tuple[ProviderClass, ...] = ()

    def __post_init__(self) -> None:
        for name in ("rule_id", "title", "jurisdiction", "service_family"):
            value = getattr(self, name)
            if not value or not value.strip():
                raise ValueError(f"{name} is required")
        if not self.sources:
            raise ValueError("a rule requires at least one authoritative source")
        source_ids = [source.source_id for source in self.sources]
        if len(source_ids) != len(set(source_ids)):
            raise ValueError("rule source_id values must be unique")


@dataclass(frozen=True)
class RuleDecision:
    """Evaluator-owned decision before the engine adds rule/source traceability."""

    outcome: RuleOutcome
    reason: str
    evidence_references: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.reason or not self.reason.strip():
            raise ValueError("rule decision reason is required")


@dataclass(frozen=True)
class RuleEvaluation:
    """Traceable public result of applying one deterministic rule."""

    rule_id: str
    outcome: RuleOutcome
    reason: str
    source_references: tuple[str, ...]
    evidence_references: tuple[str, ...] = ()

    @property
    def requires_review(self) -> bool:
        return self.outcome is RuleOutcome.REVIEW


RuleEvaluator = Callable[[Encounter, StructuredEvidence], RuleDecision]


@dataclass(frozen=True)
class RuleDefinition:
    """Executable rule mechanics paired with governed metadata."""

    metadata: RuleMetadata
    evaluator: RuleEvaluator


_EXECUTABLE_LIFECYCLES = {
    RuleLifecycle.IMPLEMENTED,
    RuleLifecycle.TESTED,
    RuleLifecycle.ACTIVE,
}


class RuleEngine:
    """Small fail-closed deterministic rule evaluator.

    The engine intentionally does not interpret clinical prose, choose billing
    policy from model output, or resolve conflicting rule definitions. A
    duplicate rule ID is treated as a material rule-source conflict and returns
    REVIEW rather than silently choosing one definition.
    """

    def __init__(self, definitions: Iterable[RuleDefinition]):
        self._definitions = tuple(definitions)

    @property
    def definitions(self) -> tuple[RuleDefinition, ...]:
        return self._definitions

    def evaluate(
        self,
        encounter: Encounter,
        evidence: StructuredEvidence,
    ) -> tuple[RuleEvaluation, ...]:
        if evidence.encounter_id != encounter.encounter_id:
            raise ValueError("rule evaluation evidence belongs to another encounter")

        grouped: dict[str, list[RuleDefinition]] = {}
        for definition in self._definitions:
            grouped.setdefault(definition.metadata.rule_id, []).append(definition)

        evaluations: list[RuleEvaluation] = []
        for rule_id in sorted(grouped):
            definitions = grouped[rule_id]
            if len(definitions) != 1:
                source_references = tuple(
                    sorted(
                        {
                            source.reference
                            for definition in definitions
                            for source in definition.metadata.sources
                        }
                    )
                )
                evaluations.append(
                    RuleEvaluation(
                        rule_id=rule_id,
                        outcome=RuleOutcome.REVIEW,
                        reason="conflicting rule definitions share the same rule_id",
                        source_references=source_references,
                    )
                )
                continue

            definition = definitions[0]
            metadata = definition.metadata
            source_references = tuple(source.reference for source in metadata.sources)

            if metadata.lifecycle is RuleLifecycle.SUPERSEDED:
                evaluations.append(
                    RuleEvaluation(
                        rule_id=metadata.rule_id,
                        outcome=RuleOutcome.NOT_APPLICABLE,
                        reason="rule is superseded and cannot be used for current support",
                        source_references=source_references,
                    )
                )
                continue

            if metadata.lifecycle not in _EXECUTABLE_LIFECYCLES:
                evaluations.append(
                    RuleEvaluation(
                        rule_id=metadata.rule_id,
                        outcome=RuleOutcome.REVIEW,
                        reason=(
                            "rule is not in an executable lifecycle state; "
                            "do not infer billing support from an unimplemented rule"
                        ),
                        source_references=source_references,
                    )
                )
                continue

            if metadata.provider_classes and encounter.metadata.provider_class not in metadata.provider_classes:
                evaluations.append(
                    RuleEvaluation(
                        rule_id=metadata.rule_id,
                        outcome=RuleOutcome.NOT_APPLICABLE,
                        reason="rule does not apply to the supplied provider class",
                        source_references=source_references,
                    )
                )
                continue

            decision = definition.evaluator(encounter, evidence)
            evaluations.append(
                RuleEvaluation(
                    rule_id=metadata.rule_id,
                    outcome=decision.outcome,
                    reason=decision.reason,
                    source_references=source_references,
                    evidence_references=decision.evidence_references,
                )
            )

        return tuple(evaluations)


OUTPATIENT_EM_SERVICE_FAMILY = "OUTPATIENT_EM_MEDICATION_MANAGEMENT"
OUTPATIENT_EM_ESTABLISHED_99214_STABLE_CHRONIC_MEDICATION_PATHWAY = (
    "OUTPATIENT_EM_ESTABLISHED_99214_STABLE_CHRONIC_MEDICATION_PATHWAY"
)

_AMA_OUTPATIENT_TOOLKIT = RuleSource(
    source_id="AMA-OUTPATIENT-TOOLKIT-2026-01-20",
    authority="American Medical Association",
    title="Simplified Outpatient Documentation and Coding",
    reference="https://edhub.ama-assn.org/steps-forward/module/2844245",
    verified_date="2026-08-13",
    version="Published online 2026-01-20",
    effective_date="2021-01-01",
)

_AMA_99214_PUBLIC_GUIDANCE = RuleSource(
    source_id="AMA-99214-PUBLIC-GUIDANCE-2026-01-26",
    authority="American Medical Association",
    title="CPT code 99214 public coding guidance",
    reference=(
        "https://www.ama-assn.org/practice-management/cpt/"
        "cpt-code-99214-established-patient-office-visit-30-39-minutes"
    ),
    verified_date="2026-08-13",
    version="Updated 2026-01-26",
)

_OFFICE_OUTPATIENT_SETTINGS = {
    "office",
    "outpatient",
    "office_outpatient",
    "office_or_other_outpatient",
}
_STABLE_CHRONIC_VALUES = {
    "stable_chronic",
    "stable_chronic_illness",
}
_SOURCE_VERIFIED_MEDICATION_ACTIONS = {"continue"}


def _normalized_token(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip().casefold().replace("-", "_").replace("/", "_").replace(" ", "_")


def _evidence_reference(item: EvidenceItem) -> tuple[str, ...]:
    references: list[str] = []
    for source in item.provenance:
        if source.start_char is not None and source.end_char is not None:
            references.append(
                f"{source.source_kind.value}:{source.field_name}:{source.start_char}:{source.end_char}"
            )
        else:
            references.append(f"{source.source_kind.value}:{source.field_name}")
    return tuple(references)


def _evaluate_established_99214_stable_chronic_medication_pathway(
    encounter: Encounter,
    evidence: StructuredEvidence,
) -> RuleDecision:
    """Evaluate one narrow public-AMA moderate-MDM pathway.

    This does not attempt to reproduce the full CPT MDM table. It implements the
    specific public AMA example in which an established office/outpatient visit
    addressing at least two stable chronic conditions plus current medication
    continuation supports moderate MDM / 99214. Failure of this pathway does not
    mean that another MDM or time pathway cannot support 99214.
    """

    if encounter.metadata.patient_status is PatientStatus.UNKNOWN:
        return RuleDecision(
            outcome=RuleOutcome.REVIEW,
            reason="patient status is unknown; this source-verified pathway applies only to established patients",
            evidence_references=("metadata:patient_status",),
        )
    if encounter.metadata.patient_status is PatientStatus.NEW:
        return RuleDecision(
            outcome=RuleOutcome.NOT_APPLICABLE,
            reason="this source-verified pathway is defined for an established patient",
            evidence_references=("metadata:patient_status",),
        )

    place_of_service = encounter.metadata.place_of_service
    if place_of_service is None:
        return RuleDecision(
            outcome=RuleOutcome.REVIEW,
            reason="office/outpatient setting is not explicitly supplied",
            evidence_references=("metadata:place_of_service",),
        )
    if _normalized_token(place_of_service) not in _OFFICE_OUTPATIENT_SETTINGS:
        return RuleDecision(
            outcome=RuleOutcome.NOT_APPLICABLE,
            reason="this rule applies only to the office/outpatient service family",
            evidence_references=("metadata:place_of_service",),
        )

    evidence_references: list[str] = ["metadata:patient_status", "metadata:place_of_service"]
    stable_chronic_count = 0

    for problem in evidence.evaluation_management.problems_addressed:
        if problem.condition.requires_review or problem.addressed.requires_review:
            return RuleDecision(
                outcome=RuleOutcome.REVIEW,
                reason="material uncertainty in a problem addressed could change this MDM pathway",
                evidence_references=tuple(
                    dict.fromkeys(
                        evidence_references
                        + list(_evidence_reference(problem.condition))
                        + list(_evidence_reference(problem.addressed))
                    )
                ),
            )

        if (
            problem.addressed.state is not EvidenceState.PRESENT
            or problem.addressed.temporal_scope is not TemporalScope.CURRENT_ENCOUNTER
        ):
            continue

        qualifies_as_stable_chronic = False
        for status in problem.status_complexity:
            if status.requires_review:
                return RuleDecision(
                    outcome=RuleOutcome.REVIEW,
                    reason="condition stability is materially ambiguous, contradictory, or temporally unclear",
                    evidence_references=tuple(
                        dict.fromkeys(evidence_references + list(_evidence_reference(status)))
                    ),
                )
            if (
                status.state is EvidenceState.PRESENT
                and status.temporal_scope is TemporalScope.CURRENT_ENCOUNTER
                and _normalized_token(status.normalized_value) in _STABLE_CHRONIC_VALUES
            ):
                qualifies_as_stable_chronic = True
                evidence_references.extend(_evidence_reference(status))
                break

        if qualifies_as_stable_chronic:
            stable_chronic_count += 1
            evidence_references.extend(_evidence_reference(problem.condition))
            evidence_references.extend(_evidence_reference(problem.addressed))

    for item in evidence.additional_items:
        if item.category == "medication_linkage" and item.requires_review:
            return RuleDecision(
                outcome=RuleOutcome.REVIEW,
                reason="medication-management linkage is materially unresolved",
                evidence_references=tuple(
                    dict.fromkeys(evidence_references + list(_evidence_reference(item)))
                ),
            )

    has_current_medication_continuation = False
    for activity in evidence.evaluation_management.management_activities:
        if activity.activity_type.requires_review or (
            activity.medication is not None and activity.medication.requires_review
        ):
            refs = list(_evidence_reference(activity.activity_type))
            if activity.medication is not None:
                refs.extend(_evidence_reference(activity.medication))
            return RuleDecision(
                outcome=RuleOutcome.REVIEW,
                reason="material uncertainty in current medication management could change this pathway",
                evidence_references=tuple(dict.fromkeys(evidence_references + refs)),
            )

        if (
            activity.medication is not None
            and activity.medication.state is EvidenceState.PRESENT
            and activity.medication.temporal_scope is TemporalScope.CURRENT_ENCOUNTER
            and activity.activity_type.state is EvidenceState.PRESENT
            and activity.activity_type.temporal_scope is TemporalScope.CURRENT_ENCOUNTER
            and _normalized_token(activity.activity_type.normalized_value)
            in _SOURCE_VERIFIED_MEDICATION_ACTIONS
        ):
            has_current_medication_continuation = True
            evidence_references.extend(_evidence_reference(activity.medication))
            evidence_references.extend(_evidence_reference(activity.activity_type))
            break

    if stable_chronic_count >= 2 and has_current_medication_continuation:
        return RuleDecision(
            outcome=RuleOutcome.SUPPORTED,
            reason=(
                "the narrow public-AMA established-patient pathway is demonstrated: "
                "at least two explicitly stable chronic conditions were addressed and "
                "current medication continuation is documented"
            ),
            evidence_references=tuple(dict.fromkeys(evidence_references)),
        )

    return RuleDecision(
        outcome=RuleOutcome.UNSUPPORTED,
        reason=(
            "this narrow 99214 pathway is not fully demonstrated; this result does not determine "
            "whether another source-verified MDM or time pathway could support the service"
        ),
        evidence_references=tuple(dict.fromkeys(evidence_references)),
    )


def outpatient_em_medication_management_rules() -> tuple[RuleDefinition, ...]:
    """Return the currently implemented source-verified outpatient E/M rules."""

    return (
        RuleDefinition(
            metadata=RuleMetadata(
                rule_id=OUTPATIENT_EM_ESTABLISHED_99214_STABLE_CHRONIC_MEDICATION_PATHWAY,
                title="Established outpatient 99214 stable-chronic medication-management pathway",
                jurisdiction="CPT_BASE",
                service_family=OUTPATIENT_EM_SERVICE_FAMILY,
                sources=(_AMA_OUTPATIENT_TOOLKIT, _AMA_99214_PUBLIC_GUIDANCE),
                lifecycle=RuleLifecycle.IMPLEMENTED,
            ),
            evaluator=_evaluate_established_99214_stable_chronic_medication_pathway,
        ),
    )
