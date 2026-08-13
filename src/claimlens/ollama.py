"""Local Ollama transport for Phase 1 model-backed evidence extraction."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
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

SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "conditions_addressed": {
            "type": "array",
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
            "items": {
                "type": "object",
                "properties": {
                    "medication": {"type": "string"},
                    "activity_type": {"type": "string"},
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
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
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
            "an exact contiguous substring of the encounter note. Do not turn medication-list "
            "presence, historical text, or hypothetical/future language into a current medication "
            "action. Preserve ambiguity and contradiction.\n\n"
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
    conditions = []
    medications = []
    additional = []

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
        additional.append(
            EvidenceItem(
                category,
                EvidenceState(str(raw["state"])),
                raw.get("normalized_value"),
                TemporalScope(str(raw["temporal_scope"])),
                sources,
            )
        )

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
