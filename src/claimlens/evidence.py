"""Structured evidence contract and Phase 1 development extraction baseline.

The evidence layer answers only: what does the supplied encounter document?
It never selects billing codes or treats probabilistic confidence as billing authority.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
import re
from typing import Any, Iterable, Protocol

from .encounter import Encounter, ProviderClass, WorkflowStage


class EvidenceState(str, Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    AMBIGUOUS = "AMBIGUOUS"
    CONTRADICTORY = "CONTRADICTORY"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class TemporalScope(str, Enum):
    CURRENT_ENCOUNTER = "CURRENT_ENCOUNTER"
    HISTORICAL = "HISTORICAL"
    UNCLEAR = "UNCLEAR"


class SourceKind(str, Enum):
    NOTE = "NOTE"
    METADATA = "METADATA"


@dataclass(frozen=True)
class SourceProvenance:
    source_kind: SourceKind
    encounter_id: str
    field_name: str
    quote: str
    start_char: int | None = None
    end_char: int | None = None

    @classmethod
    def from_note(
        cls,
        encounter: Encounter,
        quote: str,
        *,
        start_char: int | None = None,
    ) -> "SourceProvenance":
        if not quote:
            raise ValueError("note provenance quote cannot be blank")
        if start_char is None:
            start_char = encounter.raw_note_text.find(quote)
        if start_char < 0:
            raise ValueError("provenance quote is not present in source note")
        end_char = start_char + len(quote)
        if encounter.raw_note_text[start_char:end_char] != quote:
            raise ValueError("provenance span does not match source note")
        return cls(
            source_kind=SourceKind.NOTE,
            encounter_id=encounter.encounter_id,
            field_name="raw_note_text",
            quote=quote,
            start_char=start_char,
            end_char=end_char,
        )

    @classmethod
    def from_metadata(cls, encounter: Encounter, field_name: str) -> "SourceProvenance":
        if not hasattr(encounter.metadata, field_name):
            raise ValueError(f"unknown encounter metadata field: {field_name}")
        value = getattr(encounter.metadata, field_name)
        if isinstance(value, Enum):
            value = value.value
        return cls(
            source_kind=SourceKind.METADATA,
            encounter_id=encounter.encounter_id,
            field_name=field_name,
            quote="" if value is None else str(value),
        )


@dataclass(frozen=True)
class EvidenceItem:
    category: str
    state: EvidenceState
    normalized_value: Any = None
    temporal_scope: TemporalScope = TemporalScope.CURRENT_ENCOUNTER
    provenance: tuple[SourceProvenance, ...] = ()
    confidence: float | None = None
    material: bool = True

    def __post_init__(self) -> None:
        if not self.category or not self.category.strip():
            raise ValueError("evidence category is required")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if self.state is not EvidenceState.NOT_APPLICABLE and not self.provenance:
            raise ValueError("evidence assertions require provenance")

    @property
    def requires_review(self) -> bool:
        if not self.material:
            return False
        return (
            self.state in {EvidenceState.AMBIGUOUS, EvidenceState.CONTRADICTORY}
            or self.temporal_scope is TemporalScope.UNCLEAR
        )


@dataclass(frozen=True)
class ConditionAddressed:
    condition: EvidenceItem
    addressed: EvidenceItem
    status_complexity: tuple[EvidenceItem, ...] = ()
    assessment_plan: tuple[EvidenceItem, ...] = ()


@dataclass(frozen=True)
class DataActivity:
    activity_type: EvidenceItem
    object_source: EvidenceItem | None = None
    result_interpretation: EvidenceItem | None = None


@dataclass(frozen=True)
class MedicationActivity:
    medication: EvidenceItem | None
    activity_type: EvidenceItem
    associated_condition: EvidenceItem | None = None
    rationale: EvidenceItem | None = None


@dataclass(frozen=True)
class EvaluationManagementEvidence:
    problems_addressed: tuple[ConditionAddressed, ...] = ()
    data_activities: tuple[DataActivity, ...] = ()
    management_activities: tuple[MedicationActivity, ...] = ()
    practitioner_time_minutes: EvidenceItem | None = None
    time_documentation_type: EvidenceItem | None = None


@dataclass(frozen=True)
class PsychiatricEvaluationEvidence:
    reason_for_evaluation: EvidenceItem | None = None
    referral_source: EvidenceItem | None = None
    history_present_illness: EvidenceItem | None = None
    past_psychiatric_history: EvidenceItem | None = None
    significant_medical_history: EvidenceItem | None = None
    current_medications: tuple[EvidenceItem, ...] = ()
    social_history: EvidenceItem | None = None
    family_history: EvidenceItem | None = None
    mental_status_examination: EvidenceItem | None = None
    diagnostic_impression: EvidenceItem | None = None
    treatment_plan_goals: EvidenceItem | None = None
    medical_assessment_management: EvidenceItem | None = None
    information_source: EvidenceItem | None = None


@dataclass(frozen=True)
class PsychotherapyEvidence:
    psychotherapy_state: EvidenceItem | None = None
    psychotherapy_time_minutes: EvidenceItem | None = None
    time_documentation_type: EvidenceItem | None = None
    intervention_method: EvidenceItem | None = None
    target_problem_goal: EvidenceItem | None = None
    patient_participation: EvidenceItem | None = None
    response_progress: EvidenceItem | None = None
    treatment_plan_relationship: EvidenceItem | None = None
    separate_identifiability: EvidenceItem | None = None


@dataclass(frozen=True)
class StructuredEvidence:
    encounter_id: str
    workflow_stage: WorkflowStage
    provider_class: ProviderClass
    conditions_addressed: tuple[ConditionAddressed, ...] = ()
    medication_activities: tuple[MedicationActivity, ...] = ()
    data_activities: tuple[DataActivity, ...] = ()
    evaluation_management: EvaluationManagementEvidence = EvaluationManagementEvidence()
    psychiatric_evaluation: PsychiatricEvaluationEvidence = PsychiatricEvaluationEvidence()
    psychotherapy: PsychotherapyEvidence = PsychotherapyEvidence()
    additional_items: tuple[EvidenceItem, ...] = ()

    def iter_items(self) -> Iterable[EvidenceItem]:
        yield from _iter_evidence_items(self)

    @property
    def review_reasons(self) -> tuple[EvidenceItem, ...]:
        return tuple(item for item in self.iter_items() if item.requires_review)


class EvidenceExtractor(Protocol):
    def extract(self, encounter: Encounter) -> StructuredEvidence:
        """Return structured evidence without making billing decisions."""


def validate_structured_evidence(evidence: StructuredEvidence, encounter: Encounter) -> None:
    if evidence.encounter_id != encounter.encounter_id:
        raise ValueError("evidence encounter_id does not match source encounter")
    if evidence.workflow_stage is not encounter.metadata.workflow_stage:
        raise ValueError("evidence workflow_stage does not match source encounter")
    if evidence.provider_class is not encounter.metadata.provider_class:
        raise ValueError("evidence provider_class does not match source encounter")

    for item in evidence.iter_items():
        for source in item.provenance:
            if source.encounter_id != encounter.encounter_id:
                raise ValueError("evidence provenance belongs to another encounter")
            if source.source_kind is SourceKind.NOTE:
                if source.start_char is None or source.end_char is None:
                    raise ValueError("note provenance requires character offsets")
                actual = encounter.raw_note_text[source.start_char:source.end_char]
                if actual != source.quote:
                    raise ValueError("note provenance no longer matches source text")
            elif source.source_kind is SourceKind.METADATA:
                if not hasattr(encounter.metadata, source.field_name):
                    raise ValueError("metadata provenance references unknown field")
                value = getattr(encounter.metadata, source.field_name)
                if isinstance(value, Enum):
                    value = value.value
                expected = "" if value is None else str(value)
                if source.quote != expected:
                    raise ValueError("metadata provenance does not match source metadata")


def extract_evidence(encounter: Encounter, extractor: EvidenceExtractor) -> StructuredEvidence:
    evidence = extractor.extract(encounter)
    validate_structured_evidence(evidence, encounter)
    return evidence


class DevelopmentPatternExtractor:
    """Small deterministic baseline for synthetic Phase 1 development cases.

    This is not a production NLP system and is not billing authority. It exists to
    exercise the frozen evidence contract and establish measurable known-answer
    behavior before a model adapter is selected.
    """

    _ACTION_RE = re.compile(
        r"\b(continue|stop|start|restart|increase|decrease|reduce|lower|raise)\s+"
        r"([A-Za-z][A-Za-z0-9-]*)"
        r"(?:\s+(\d+(?:\.\d+)?\s*mg))?",
        flags=re.IGNORECASE,
    )
    _PAST_CHANGE_RE = re.compile(
        r"\b([A-Za-z][A-Za-z0-9-]*)\s+was\s+(increased|decreased|reduced|lowered|raised)\b",
        flags=re.IGNORECASE,
    )
    _MED_LIST_RE = re.compile(
        r"(?:current\s+)?medication\s+list\s*:\s*([A-Za-z][A-Za-z0-9-]*)"
        r"(?:\s+([A-Za-z]{1,4}))?\s+(\d+(?:\.\d+)?\s*mg)",
        flags=re.IGNORECASE,
    )
    _MED_LIST_APPEARS_RE = re.compile(
        r"\b([A-Za-z][A-Za-z0-9-]*)"
        r"(?:\s+([A-Za-z]{1,4}))?\s+(\d+(?:\.\d+)?\s*mg)"
        r"(?:\s+\w+){0,3}\s+appears\s+on\s+the\s+(?:current\s+)?medication\s+list\b",
        flags=re.IGNORECASE,
    )
    _CONDITION_RE = re.compile(
        r"^\s*([A-Z][A-Za-z /-]{2,60}?)\s+"
        r"(?:has|have|is|are|remains|remain|was|were)\b",
    )
    _GENERIC_CONDITIONS = {"the patient", "assessment", "plan", "today", "symptoms"}

    def extract(self, encounter: Encounter) -> StructuredEvidence:
        conditions: list[ConditionAddressed] = []
        medication_activities: list[MedicationActivity] = []
        additional_items: list[EvidenceItem] = []

        sentences = list(_sentence_spans(encounter.raw_note_text))
        for sentence, start in sentences:
            clean = sentence.strip()
            if not clean:
                continue
            temporal = _temporal_scope(clean)
            provenance = SourceProvenance.from_note(encounter, sentence, start_char=start)

            condition_match = self._CONDITION_RE.search(clean)
            if condition_match:
                condition = condition_match.group(1).strip().rstrip(":")
                if condition.lower() not in self._GENERIC_CONDITIONS:
                    condition_item = EvidenceItem(
                        category="condition",
                        state=EvidenceState.PRESENT,
                        normalized_value=condition.lower(),
                        temporal_scope=temporal,
                        provenance=(provenance,),
                    )
                    conditions.append(
                        ConditionAddressed(
                            condition=condition_item,
                            addressed=EvidenceItem(
                                category="condition_addressed",
                                state=EvidenceState.PRESENT,
                                normalized_value=True,
                                temporal_scope=temporal,
                                provenance=(provenance,),
                            ),
                        )
                    )

            list_match = self._MED_LIST_RE.search(clean) or self._MED_LIST_APPEARS_RE.search(clean)
            if list_match:
                med_name = list_match.group(1)
                formulation = list_match.group(2)
                dose = list_match.group(3)
                value = " ".join(part for part in (med_name, formulation, dose) if part)
                additional_items.append(
                    EvidenceItem(
                        category="medication_list_presence",
                        state=EvidenceState.PRESENT,
                        normalized_value=value.lower(),
                        temporal_scope=temporal,
                        provenance=(provenance,),
                    )
                )

            future_or_conditional = bool(
                re.search(r"\b(could|may|might|consider|future|if)\b", clean, re.IGNORECASE)
            )

            for match in self._ACTION_RE.finditer(clean):
                action, medication, dose = match.groups()
                action_lower = action.lower()
                if medication.lower() == "current" and re.search(
                    r"\bcontinue current medications\b", clean, re.IGNORECASE
                ):
                    continue
                if future_or_conditional and action_lower in {
                    "increase",
                    "decrease",
                    "reduce",
                    "lower",
                    "raise",
                }:
                    continue
                medication_activities.append(
                    MedicationActivity(
                        medication=EvidenceItem(
                            category="medication",
                            state=EvidenceState.PRESENT,
                            normalized_value=medication.lower(),
                            temporal_scope=temporal,
                            provenance=(provenance,),
                        ),
                        activity_type=EvidenceItem(
                            category="medication_activity_type",
                            state=EvidenceState.PRESENT,
                            normalized_value=action_lower,
                            temporal_scope=temporal,
                            provenance=(provenance,),
                        ),
                        rationale=(
                            EvidenceItem(
                                category="medication_activity_detail",
                                state=EvidenceState.PRESENT,
                                normalized_value=dose.lower() if dose else None,
                                temporal_scope=temporal,
                                provenance=(provenance,),
                            )
                            if dose
                            else None
                        ),
                    )
                )

            for match in self._PAST_CHANGE_RE.finditer(clean):
                medication, action = match.groups()
                normalized_action = {
                    "increased": "increase",
                    "decreased": "decrease",
                    "reduced": "reduce",
                    "lowered": "lower",
                    "raised": "raise",
                }[action.lower()]
                medication_activities.append(
                    MedicationActivity(
                        medication=EvidenceItem(
                            category="medication",
                            state=EvidenceState.PRESENT,
                            normalized_value=medication.lower(),
                            temporal_scope=TemporalScope.HISTORICAL,
                            provenance=(provenance,),
                        ),
                        activity_type=EvidenceItem(
                            category="medication_activity_type",
                            state=EvidenceState.PRESENT,
                            normalized_value=normalized_action,
                            temporal_scope=TemporalScope.HISTORICAL,
                            provenance=(provenance,),
                        ),
                    )
                )

            generic_continue = re.search(r"\bcontinue current medications\b", clean, re.IGNORECASE)
            if generic_continue:
                additional_items.append(
                    EvidenceItem(
                        category="medication_linkage",
                        state=EvidenceState.AMBIGUOUS,
                        normalized_value="continue current medications",
                        temporal_scope=temporal,
                        provenance=(provenance,),
                    )
                )

            no_side_effects = re.search(
                r"\bno (?:new )?(?:medication )?(?:side effects|adverse effects)\b",
                clean,
                re.IGNORECASE,
            )
            if no_side_effects:
                additional_items.append(
                    EvidenceItem(
                        category="medication_adverse_effect",
                        state=EvidenceState.ABSENT,
                        normalized_value=None,
                        temporal_scope=temporal,
                        provenance=(provenance,),
                    )
                )
            elif re.search(r"\bpersistent nausea\b", clean, re.IGNORECASE):
                additional_items.append(
                    EvidenceItem(
                        category="medication_adverse_effect",
                        state=EvidenceState.PRESENT,
                        normalized_value="nausea",
                        temporal_scope=temporal,
                        provenance=(provenance,),
                    )
                )

        _append_medication_contradictions(medication_activities, additional_items)

        evidence = StructuredEvidence(
            encounter_id=encounter.encounter_id,
            workflow_stage=encounter.metadata.workflow_stage,
            provider_class=encounter.metadata.provider_class,
            conditions_addressed=tuple(conditions),
            medication_activities=tuple(medication_activities),
            evaluation_management=EvaluationManagementEvidence(
                problems_addressed=tuple(conditions),
                management_activities=tuple(
                    activity
                    for activity in medication_activities
                    if activity.activity_type.temporal_scope is TemporalScope.CURRENT_ENCOUNTER
                ),
            ),
            additional_items=tuple(additional_items),
        )
        validate_structured_evidence(evidence, encounter)
        return evidence


def _append_medication_contradictions(
    activities: list[MedicationActivity],
    additional_items: list[EvidenceItem],
) -> None:
    by_medication: dict[str, list[MedicationActivity]] = {}
    for activity in activities:
        if activity.medication is None:
            continue
        if activity.activity_type.temporal_scope is not TemporalScope.CURRENT_ENCOUNTER:
            continue
        medication = str(activity.medication.normalized_value)
        by_medication.setdefault(medication, []).append(activity)

    for medication, grouped in by_medication.items():
        actions = {str(item.activity_type.normalized_value) for item in grouped}
        if len(actions) <= 1:
            continue
        provenance: list[SourceProvenance] = []
        for item in grouped:
            provenance.extend(item.activity_type.provenance)
        additional_items.append(
            EvidenceItem(
                category="medication_plan_consistency",
                state=EvidenceState.CONTRADICTORY,
                normalized_value={"medication": medication, "actions": sorted(actions)},
                temporal_scope=TemporalScope.CURRENT_ENCOUNTER,
                provenance=tuple(dict.fromkeys(provenance)),
            )
        )


def _sentence_spans(text: str) -> Iterable[tuple[str, int]]:
    for match in re.finditer(r"[^.!?\n]+(?:[.!?]|(?=\n|$))", text):
        sentence = match.group(0)
        if sentence.strip():
            yield sentence, match.start()


def _temporal_scope(sentence: str) -> TemporalScope:
    if re.search(
        r"\b(prior[- ]visit|previous appointment|previous visit|copied|histor(?:y|ical))\b",
        sentence,
        re.IGNORECASE,
    ):
        return TemporalScope.HISTORICAL
    if re.search(
        r"\b(today|for now|current|plan|assessment|continue|stop|start|reports?|remains?|discussed|stable|improved)\b",
        sentence,
        re.IGNORECASE,
    ):
        return TemporalScope.CURRENT_ENCOUNTER
    return TemporalScope.UNCLEAR


def _iter_evidence_items(value: Any) -> Iterable[EvidenceItem]:
    if isinstance(value, EvidenceItem):
        yield value
        return
    if isinstance(value, (str, bytes, Enum)) or value is None:
        return
    if isinstance(value, (tuple, list)):
        for item in value:
            yield from _iter_evidence_items(item)
        return
    if is_dataclass(value):
        for field in fields(value):
            if field.name in {"encounter_id", "workflow_stage", "provider_class"}:
                continue
            yield from _iter_evidence_items(getattr(value, field.name))
