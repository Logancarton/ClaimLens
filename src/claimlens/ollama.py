"""Local Ollama transport for Phase 1 model-backed evidence extraction."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
import re
from typing import Any, Callable, Mapping
from urllib import error as urlerror
from urllib import request as urlrequest

from .encounter import Encounter
from .evidence import (
    ConditionAddressed,
    EvaluationManagementEvidence,
    EvidenceItem,
    EvidenceState,
    MedicationActivity,
    SourceProvenance,
    StructuredEvidence,
    TemporalScope,
)

DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "medgemma1.5"
Transport = Callable[[str, Mapping[str, Any], float], Mapping[str, Any]]

MEDICATION_ACTIVITY_TYPES = (
    "start",
    "stop",
    "continue",
    "restart",
    "increase",
    "decrease",
    "reduce",
    "lower",
    "raise",
    "dose_change",
    "prescribe",
    "monitor",
    "adverse_effect_discussion",
    "adherence_discussion",
    "other_management",
)

ADDITIONAL_ITEM_CATEGORIES = (
    "medication_list_presence",
    "medication_linkage",
    "medication_contradiction",
    "medication_adverse_effect",
)

_ACTION_SOURCE_PATTERNS = {
    "start": r"\b(start|started|begin|began|initiate|initiated)\b",
    "stop": r"\b(stop|stopped|discontinue|discontinued)\b",
    "continue": r"\b(continue|continued|continuing)\b",
    "restart": r"\b(restart|restarted|resume|resumed)\b",
    "increase": r"\b(increase|increased|raise|raised)\b",
    "decrease": r"\b(decrease|decreased|reduce|reduced|lower|lowered)\b",
    "reduce": r"\b(reduce|reduced|decrease|decreased|lower|lowered)\b",
    "lower": r"\b(lower|lowered|decrease|decreased|reduce|reduced)\b",
    "raise": r"\b(raise|raised|increase|increased)\b",
    "dose_change": r"\b(dose|change|changed|increase|increased|decrease|decreased|reduce|reduced|lower|lowered|raise|raised)\b",
    "prescribe": r"\b(prescribe|prescribed|prescription)\b",
    "monitor": r"\b(monitor|monitored|monitoring)\b",
    "adverse_effect_discussion": r"\b(side effects?|adverse effects?|tolerat(?:e|ed|ing|ion))\b",
    "adherence_discussion": r"\b(adherence|adherent|compliance|compliant|taking as prescribed)\b",
    "other_management": r"\b(manage|managed|management|plan|discussed|reviewed)\b",
}

_HISTORICAL_CHANGE_RE = re.compile(
    r"\b([A-Za-z][A-Za-z0-9-]*)\s+was\s+"
    r"(increased|decreased|reduced|lowered|raised)\b",
    re.IGNORECASE,
)

SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "conditions_addressed": {
            "type": "array",
            "description": "Problems explicitly addressed in the encounter.",
            "items": {
                "type": "object",
                "properties": {
                    "condition": {"type": "string"},
                    "state": {"type": "string", "enum": [x.value for x in EvidenceState]},
                    "temporal_scope": {"type": "string", "enum": [x.value for x in TemporalScope]},
                    "source_quotes": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                },
                "required": ["condition", "state", "temporal_scope", "source_quotes"],
                "additionalProperties": False,
            },
        },
        "medication_activities": {
            "type": "array",
            "description": (
                "Explicit medication-management actions only. Medication-list presence, taking status, "
                "and generic unlinked medication wording do not belong in this array."
            ),
            "items": {
                "type": "object",
                "properties": {
                    "medication": {"type": "string"},
                    "activity_type": {
                        "type": "string",
                        "enum": list(MEDICATION_ACTIVITY_TYPES),
                        "description": "A documented management action, never a status label such as current/listed/taking.",
                    },
                    "state": {"type": "string", "enum": [x.value for x in EvidenceState]},
                    "temporal_scope": {"type": "string", "enum": [x.value for x in TemporalScope]},
                    "source_quotes": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                },
                "required": ["medication", "activity_type", "state", "temporal_scope", "source_quotes"],
                "additionalProperties": False,
            },
        },
        "additional_items": {
            "type": "array",
            "description": "Medication-list presence, unresolved linkage, contradiction, and adverse-effect evidence.",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "enum": list(ADDITIONAL_ITEM_CATEGORIES)},
                    "state": {"type": "string", "enum": [x.value for x in EvidenceState]},
                    "normalized_value": {"type": ["string", "null"]},
                    "temporal_scope": {"type": "string", "enum": [x.value for x in TemporalScope]},
                    "source_quotes": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                },
                "required": ["category", "state", "normalized_value", "temporal_scope", "source_quotes"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["conditions_addressed", "medication_activities", "additional_items"],
    "additionalProperties": False,
}


@dataclass(frozen=True)
class OllamaEvidenceExtractor:
    model: str = DEFAULT_OLLAMA_MODEL
    base_url: str = DEFAULT_OLLAMA_BASE_URL
    timeout_seconds: float = 180.0
    extraction_prompt: str = ""
    transport: Transport | None = None

    @classmethod
    def from_environment(cls, *, extraction_prompt: str = "") -> "OllamaEvidenceExtractor":
        return cls(
            model=os.getenv("CLAIMLENS_OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL),
            base_url=os.getenv("CLAIMLENS_OLLAMA_BASE_URL", DEFAULT_OLLAMA_BASE_URL),
            extraction_prompt=extraction_prompt,
        )

    def extract(self, encounter: Encounter) -> StructuredEvidence:
        response = (self.transport or _post_json)(
            f"{self.base_url.rstrip('/')}/api/chat",
            self._payload(encounter),
            self.timeout_seconds,
        )
        return _to_evidence(_content_json(response), encounter)

    def _payload(self, encounter: Encounter) -> dict[str, Any]:
        schema_text = json.dumps(SCHEMA, separators=(",", ":"))
        prompt = self.extraction_prompt.strip()
        if prompt:
            prompt += "\n\n"
        prompt += (
            "Return only JSON matching the supplied schema. Every source_quotes value must be "
            "an exact contiguous substring of the encounter note. A named medication activity must "
            "be supported by source text that explicitly contains both the medication and its action. "
            "Medication-list presence belongs only in additional_items and only when the source "
            "explicitly identifies a medication list. Do not turn medication status, historical text, "
            "or hypothetical/future language into a current medication action. Preserve historical "
            "actions as HISTORICAL and retain both sides of explicit contradictions.\n\n"
            f"SCHEMA:\n{schema_text}\n\n"
            f"WORKFLOW_STAGE: {encounter.metadata.workflow_stage.value}\n"
            f"PROVIDER_CLASS: {encounter.metadata.provider_class.value}\n"
            f"ENCOUNTER:\n{encounter.raw_note_text}"
        )
        return {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "format": SCHEMA,
            "options": {"temperature": 0},
        }


def _post_json(url: str, payload: Mapping[str, Any], timeout: float) -> Mapping[str, Any]:
    req = urlrequest.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlrequest.urlopen(req, timeout=timeout) as response:
            parsed = json.loads(response.read().decode("utf-8"))
    except (urlerror.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Ollama request failed: {exc}") from exc
    if not isinstance(parsed, Mapping):
        raise RuntimeError("Ollama response must be an object")
    return parsed


def _content_json(response: Mapping[str, Any]) -> Mapping[str, Any]:
    message = response.get("message")
    if not isinstance(message, Mapping) or not isinstance(message.get("content"), str):
        raise RuntimeError("Ollama response is missing message.content")
    try:
        parsed = json.loads(message["content"])
    except json.JSONDecodeError as exc:
        raise RuntimeError("Ollama returned invalid structured JSON") from exc
    if not isinstance(parsed, Mapping):
        raise RuntimeError("Ollama structured output must be an object")
    return parsed


def _to_evidence(payload: Mapping[str, Any], encounter: Encounter) -> StructuredEvidence:
    conditions: list[ConditionAddressed] = []
    medications: list[MedicationActivity] = []
    additional: list[EvidenceItem] = []

    for raw in _objects(payload, "conditions_addressed"):
        sources = _sources(encounter, raw)
        state = EvidenceState(str(raw["state"]))
        temporal = TemporalScope(str(raw["temporal_scope"]))
        value = str(raw["condition"]).strip().lower()
        if not value:
            raise ValueError("condition cannot be blank")
        conditions.append(
            ConditionAddressed(
                condition=EvidenceItem("condition", state, value, temporal, sources),
                addressed=EvidenceItem("condition_addressed", state, True, temporal, sources),
            )
        )

    for raw in _objects(payload, "medication_activities"):
        sources = _sources(encounter, raw)
        state = EvidenceState(str(raw["state"]))
        temporal = TemporalScope(str(raw["temporal_scope"]))
        medication = str(raw["medication"]).strip().lower()
        action = str(raw["activity_type"]).strip().lower()
        if not medication or not action:
            raise ValueError("medication activity requires medication and activity_type")
        if action not in MEDICATION_ACTIVITY_TYPES:
            raise ValueError(f"unsupported medication activity_type: {action}")
        if not _explicit_named_action_source(medication, action, sources):
            _append_unique_additional(
                additional,
                EvidenceItem(
                    category="medication_linkage",
                    state=EvidenceState.AMBIGUOUS,
                    normalized_value=f"{medication}: {action}",
                    temporal_scope=temporal,
                    provenance=sources,
                ),
            )
            continue
        medications.append(
            MedicationActivity(
                medication=EvidenceItem("medication", state, medication, temporal, sources),
                activity_type=EvidenceItem("medication_activity_type", state, action, temporal, sources),
            )
        )

    for raw in _objects(payload, "additional_items"):
        sources = _sources(encounter, raw)
        category = str(raw["category"]).strip()
        if not category:
            raise ValueError("additional evidence category cannot be blank")
        if category not in ADDITIONAL_ITEM_CATEGORIES:
            raise ValueError(f"unsupported additional evidence category: {category}")
        if category == "medication_list_presence" and not _explicit_medication_list_source(sources):
            continue
        _append_unique_additional(
            additional,
            EvidenceItem(
                category,
                EvidenceState(str(raw["state"])),
                raw.get("normalized_value"),
                TemporalScope(str(raw["temporal_scope"])),
                sources,
            ),
        )

    _append_source_guardrails(encounter, medications, additional)
    _append_derived_medication_contradictions(medications, additional)

    return StructuredEvidence(
        encounter_id=encounter.encounter_id,
        workflow_stage=encounter.metadata.workflow_stage,
        provider_class=encounter.metadata.provider_class,
        conditions_addressed=tuple(conditions),
        medication_activities=tuple(medications),
        evaluation_management=EvaluationManagementEvidence(
            problems_addressed=tuple(conditions),
            management_activities=tuple(
                x for x in medications
                if x.activity_type.temporal_scope is TemporalScope.CURRENT_ENCOUNTER
            ),
        ),
        additional_items=tuple(additional),
    )


def _objects(payload: Mapping[str, Any], key: str) -> list[Mapping[str, Any]]:
    value = payload.get(key)
    if not isinstance(value, list) or any(not isinstance(x, Mapping) for x in value):
        raise ValueError(f"{key} must be a list of objects")
    return value


def _sources(encounter: Encounter, raw: Mapping[str, Any]) -> tuple[SourceProvenance, ...]:
    quotes = raw.get("source_quotes")
    if not isinstance(quotes, list) or not quotes:
        raise ValueError("source_quotes must contain at least one exact quote")
    return tuple(SourceProvenance.from_note(encounter, str(quote)) for quote in quotes)


def _explicit_named_action_source(
    medication: str,
    action: str,
    sources: tuple[SourceProvenance, ...],
) -> bool:
    action_pattern = _ACTION_SOURCE_PATTERNS[action]
    medication_pattern = re.compile(rf"\b{re.escape(medication)}\b", re.IGNORECASE)
    return any(
        medication_pattern.search(source.quote)
        and re.search(action_pattern, source.quote, re.IGNORECASE)
        for source in sources
    )


def _explicit_medication_list_source(sources: tuple[SourceProvenance, ...]) -> bool:
    return any(
        re.search(r"\bmedication\s+list\b", source.quote, re.IGNORECASE)
        for source in sources
    )


def _append_source_guardrails(
    encounter: Encounter,
    activities: list[MedicationActivity],
    additional_items: list[EvidenceItem],
) -> None:
    for sentence, start in _sentence_spans(encounter.raw_note_text):
        clean = sentence.strip()
        if not clean:
            continue
        provenance = SourceProvenance.from_note(encounter, sentence, start_char=start)
        temporal = _guardrail_temporal_scope(clean)

        if re.search(r"\bmedication\s+list\b", clean, re.IGNORECASE):
            _append_unique_additional(
                additional_items,
                EvidenceItem(
                    category="medication_list_presence",
                    state=EvidenceState.PRESENT,
                    normalized_value=clean,
                    temporal_scope=temporal,
                    provenance=(provenance,),
                ),
            )

        if re.search(r"\bcontinue\s+current\s+medications\b", clean, re.IGNORECASE):
            _append_unique_additional(
                additional_items,
                EvidenceItem(
                    category="medication_linkage",
                    state=EvidenceState.AMBIGUOUS,
                    normalized_value="continue current medications",
                    temporal_scope=temporal,
                    provenance=(provenance,),
                ),
            )

        if not _has_historical_cue(clean):
            continue
        historical_match = _HISTORICAL_CHANGE_RE.search(clean)
        if not historical_match:
            continue
        medication, action = historical_match.groups()
        normalized_action = {
            "increased": "increase",
            "decreased": "decrease",
            "reduced": "reduce",
            "lowered": "lower",
            "raised": "raise",
        }[action.lower()]
        medication = medication.lower()
        if any(
            item.medication is not None
            and str(item.medication.normalized_value).lower() == medication
            and str(item.activity_type.normalized_value).lower() == normalized_action
            and item.activity_type.temporal_scope is TemporalScope.HISTORICAL
            for item in activities
        ):
            continue
        activities.append(
            MedicationActivity(
                medication=EvidenceItem(
                    category="medication",
                    state=EvidenceState.PRESENT,
                    normalized_value=medication,
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


def _append_derived_medication_contradictions(
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
        if any(
            item.state is EvidenceState.CONTRADICTORY
            and medication in str(item.normalized_value).lower()
            for item in additional_items
        ):
            continue
        provenance: list[SourceProvenance] = []
        for item in grouped:
            provenance.extend(item.activity_type.provenance)
        _append_unique_additional(
            additional_items,
            EvidenceItem(
                category="medication_contradiction",
                state=EvidenceState.CONTRADICTORY,
                normalized_value=f"{medication}: {', '.join(sorted(actions))}",
                temporal_scope=TemporalScope.CURRENT_ENCOUNTER,
                provenance=tuple(dict.fromkeys(provenance)),
            ),
        )


def _append_unique_additional(
    additional_items: list[EvidenceItem],
    candidate: EvidenceItem,
) -> None:
    candidate_quotes = tuple(source.quote for source in candidate.provenance)
    if any(
        item.category == candidate.category
        and item.state is candidate.state
        and tuple(source.quote for source in item.provenance) == candidate_quotes
        for item in additional_items
    ):
        return
    additional_items.append(candidate)


def _sentence_spans(text: str):
    for match in re.finditer(r"[^.!?\n]+(?:[.!?]|(?=\n|$))", text):
        sentence = match.group(0)
        if sentence.strip():
            yield sentence, match.start()


def _has_historical_cue(sentence: str) -> bool:
    return bool(
        re.search(
            r"\b(prior[- ]visit|previous appointment|previous visit|copied|histor(?:y|ical))\b",
            sentence,
            re.IGNORECASE,
        )
    )


def _guardrail_temporal_scope(sentence: str) -> TemporalScope:
    if _has_historical_cue(sentence):
        return TemporalScope.HISTORICAL
    if re.search(
        r"\b(today|for now|current|plan|assessment|continue|stop|start|reports?|remains?|discussed|stable|improved)\b",
        sentence,
        re.IGNORECASE,
    ):
        return TemporalScope.CURRENT_ENCOUNTER
    return TemporalScope.UNCLEAR
