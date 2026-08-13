"""Encounter input contract for ClaimLens Phase 1.

This module owns source-note preservation and explicitly supplied encounter metadata.
It does not infer billing facts, provider credentials, patient status, or place of service.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
from enum import Enum
from typing import Any, Mapping


class WorkflowStage(str, Enum):
    PRE_SIGN = "PRE_SIGN"
    PRE_SUBMIT = "PRE_SUBMIT"


class ProviderClass(str, Enum):
    PMHNP_NP = "PMHNP_NP"
    PSYCHIATRIST = "PSYCHIATRIST"


class PatientStatus(str, Enum):
    NEW = "NEW"
    ESTABLISHED = "ESTABLISHED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class EncounterMetadata:
    encounter_id: str
    workflow_stage: WorkflowStage
    provider_class: ProviderClass
    date_of_service: str | None = None
    patient_status: PatientStatus = PatientStatus.UNKNOWN
    place_of_service: str | None = None

    def __post_init__(self) -> None:
        if not self.encounter_id or not self.encounter_id.strip():
            raise ValueError("encounter_id is required")
        if self.date_of_service is not None:
            try:
                date.fromisoformat(self.date_of_service)
            except ValueError as exc:
                raise ValueError("date_of_service must use YYYY-MM-DD") from exc
        if self.place_of_service is not None and not self.place_of_service.strip():
            raise ValueError("place_of_service cannot be blank")

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["workflow_stage"] = self.workflow_stage.value
        result["provider_class"] = self.provider_class.value
        result["patient_status"] = self.patient_status.value
        return result

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "EncounterMetadata":
        return cls(
            encounter_id=str(payload["encounter_id"]),
            workflow_stage=WorkflowStage(str(payload["workflow_stage"])),
            provider_class=ProviderClass(str(payload["provider_class"])),
            date_of_service=(
                str(payload["date_of_service"])
                if payload.get("date_of_service") is not None
                else None
            ),
            patient_status=PatientStatus(str(payload.get("patient_status", "UNKNOWN"))),
            place_of_service=(
                str(payload["place_of_service"])
                if payload.get("place_of_service") is not None
                else None
            ),
        )


@dataclass(frozen=True)
class Encounter:
    metadata: EncounterMetadata
    raw_note_text: str

    def __post_init__(self) -> None:
        if not self.raw_note_text or not self.raw_note_text.strip():
            raise ValueError("raw_note_text is required")

    @property
    def encounter_id(self) -> str:
        return self.metadata.encounter_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "metadata": self.metadata.to_dict(),
            "raw_note_text": self.raw_note_text,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "Encounter":
        metadata = payload.get("metadata")
        if not isinstance(metadata, Mapping):
            raise ValueError("metadata must be an object")
        return cls(
            metadata=EncounterMetadata.from_dict(metadata),
            raw_note_text=str(payload["raw_note_text"]),
        )
