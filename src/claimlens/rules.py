"""Deterministic billing-rule evaluation boundary.

PURPOSE
    Evaluate structured evidence against source-verified billing requirements.

SIGNAL FLOW
    Structured Evidence + Encounter Metadata → Rule Engine → Rule Evaluations

BOUNDARY
    This module provides generic rule mechanics only. Authoritative billing-rule
    content belongs under ``rules/`` with source/version metadata. Prompts and
    model output are never rule authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Iterable

from .encounter import Encounter, ProviderClass
from .evidence import StructuredEvidence


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
