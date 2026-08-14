import unittest

from claimlens.encounter import Encounter, ProviderClass
from claimlens.evidence import StructuredEvidence
from claimlens.rules import (
    RuleDecision,
    RuleDefinition,
    RuleEngine,
    RuleLifecycle,
    RuleMetadata,
    RuleOutcome,
    RuleSource,
)


def _encounter(encounter_id="RULE-TEST", provider_class="PMHNP_NP"):
    return Encounter.from_dict(
        {
            "metadata": {
                "encounter_id": encounter_id,
                "workflow_stage": "PRE_SUBMIT",
                "provider_class": provider_class,
            },
            "raw_note_text": "Synthetic outpatient psychiatry note.",
        }
    )


def _evidence(encounter):
    return StructuredEvidence(
        encounter_id=encounter.encounter_id,
        workflow_stage=encounter.metadata.workflow_stage,
        provider_class=encounter.metadata.provider_class,
    )


def _source(source_id="AUTH-1", reference="authoritative://source/1"):
    return RuleSource(
        source_id=source_id,
        authority="Authoritative Test Authority",
        title="Synthetic authoritative source",
        reference=reference,
        verified_date="2026-08-13",
        version="v1",
    )


def _definition(
    *,
    rule_id="RULE-1",
    outcome=RuleOutcome.SUPPORTED,
    lifecycle=RuleLifecycle.IMPLEMENTED,
    source=None,
    provider_classes=(),
):
    source = source or _source()

    def evaluator(encounter, evidence):
        return RuleDecision(
            outcome=outcome,
            reason=f"synthetic {outcome.value.lower()} decision",
            evidence_references=(evidence.encounter_id,),
        )

    return RuleDefinition(
        metadata=RuleMetadata(
            rule_id=rule_id,
            title="Synthetic rule",
            jurisdiction="TEST",
            service_family="OUTPATIENT_EM_MEDICATION_MANAGEMENT",
            sources=(source,),
            lifecycle=lifecycle,
            provider_classes=provider_classes,
        ),
        evaluator=evaluator,
    )


class RuleContractTests(unittest.TestCase):
    def test_rule_metadata_requires_authoritative_source(self):
        with self.assertRaises(ValueError):
            RuleMetadata(
                rule_id="RULE-NO-SOURCE",
                title="Missing source",
                jurisdiction="TEST",
                service_family="OUTPATIENT_EM_MEDICATION_MANAGEMENT",
                sources=(),
                lifecycle=RuleLifecycle.IMPLEMENTED,
            )

    def test_engine_preserves_rule_source_and_evidence_traceability(self):
        encounter = _encounter()
        evidence = _evidence(encounter)
        source = _source(reference="https://example.test/authority")
        evaluation = RuleEngine((_definition(source=source),)).evaluate(encounter, evidence)[0]

        self.assertIs(evaluation.outcome, RuleOutcome.SUPPORTED)
        self.assertEqual(evaluation.rule_id, "RULE-1")
        self.assertEqual(evaluation.source_references, ("https://example.test/authority",))
        self.assertEqual(evaluation.evidence_references, (encounter.encounter_id,))
        self.assertFalse(evaluation.requires_review)

    def test_engine_preserves_supported_unsupported_and_review_outcomes(self):
        encounter = _encounter()
        evidence = _evidence(encounter)
        definitions = (
            _definition(rule_id="SUPPORTED", outcome=RuleOutcome.SUPPORTED),
            _definition(
                rule_id="UNSUPPORTED",
                outcome=RuleOutcome.UNSUPPORTED,
                source=_source("AUTH-2", "authoritative://source/2"),
            ),
            _definition(
                rule_id="REVIEW",
                outcome=RuleOutcome.REVIEW,
                source=_source("AUTH-3", "authoritative://source/3"),
            ),
        )

        evaluations = {item.rule_id: item for item in RuleEngine(definitions).evaluate(encounter, evidence)}
        self.assertIs(evaluations["SUPPORTED"].outcome, RuleOutcome.SUPPORTED)
        self.assertIs(evaluations["UNSUPPORTED"].outcome, RuleOutcome.UNSUPPORTED)
        self.assertIs(evaluations["REVIEW"].outcome, RuleOutcome.REVIEW)
        self.assertTrue(evaluations["REVIEW"].requires_review)

    def test_conflicting_rule_definitions_fail_closed_to_review(self):
        encounter = _encounter()
        evidence = _evidence(encounter)
        definitions = (
            _definition(
                rule_id="CONFLICT",
                source=_source("AUTH-A", "authoritative://source/a"),
            ),
            _definition(
                rule_id="CONFLICT",
                outcome=RuleOutcome.UNSUPPORTED,
                source=_source("AUTH-B", "authoritative://source/b"),
            ),
        )

        evaluation = RuleEngine(definitions).evaluate(encounter, evidence)[0]
        self.assertIs(evaluation.outcome, RuleOutcome.REVIEW)
        self.assertIn("conflicting rule definitions", evaluation.reason)
        self.assertEqual(
            evaluation.source_references,
            ("authoritative://source/a", "authoritative://source/b"),
        )

    def test_unimplemented_source_verified_rule_cannot_create_support(self):
        encounter = _encounter()
        evidence = _evidence(encounter)
        definition = _definition(lifecycle=RuleLifecycle.SOURCE_VERIFIED)

        evaluation = RuleEngine((definition,)).evaluate(encounter, evidence)[0]
        self.assertIs(evaluation.outcome, RuleOutcome.REVIEW)
        self.assertIn("not in an executable lifecycle state", evaluation.reason)

    def test_provider_specific_rule_is_not_applied_to_other_provider_class(self):
        encounter = _encounter(provider_class="PSYCHIATRIST")
        evidence = _evidence(encounter)
        definition = _definition(provider_classes=(ProviderClass.PMHNP_NP,))

        evaluation = RuleEngine((definition,)).evaluate(encounter, evidence)[0]
        self.assertIs(evaluation.outcome, RuleOutcome.NOT_APPLICABLE)

    def test_rule_engine_rejects_cross_encounter_evidence(self):
        encounter = _encounter(encounter_id="RULE-A")
        other = _encounter(encounter_id="RULE-B")
        with self.assertRaises(ValueError):
            RuleEngine((_definition(),)).evaluate(encounter, _evidence(other))


if __name__ == "__main__":
    unittest.main()
