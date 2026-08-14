import json
import unittest
from dataclasses import replace
from pathlib import Path

from claimlens.encounter import Encounter
from claimlens.evidence import (
    ConditionAddressed,
    EvaluationManagementEvidence,
    EvidenceItem,
    EvidenceState,
    MedicationActivity,
    SourceProvenance,
    StructuredEvidence,
)
from claimlens.rules import (
    OUTPATIENT_EM_ESTABLISHED_99214_STABLE_CHRONIC_MEDICATION_PATHWAY,
    RuleDecision,
    RuleDefinition,
    RuleEngine,
    RuleOutcome,
    RuleSource,
    outpatient_em_medication_management_rules,
)


_CASES_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "development_cases"
    / "phase2_outpatient_em_rule_cases.json"
)


def _load_cases():
    with _CASES_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _build_case(payload):
    note_parts = []
    condition_quotes = []
    for condition in payload["conditions"]:
        quote = (
            f"{condition['name']} addressed with status "
            f"{condition['status_value']} ({condition['status_state']})."
        )
        note_parts.append(quote)
        condition_quotes.append(quote)

    medication = payload["medication"]
    medication_quote = f"{medication['action']} {medication['name']}."
    note_parts.append(medication_quote)
    raw_note = " ".join(note_parts)

    encounter = Encounter.from_dict(
        {
            "metadata": {
                "encounter_id": payload["case_id"],
                "workflow_stage": "PRE_SUBMIT",
                "provider_class": payload["provider_class"],
                "patient_status": payload["patient_status"],
                "place_of_service": payload["place_of_service"],
            },
            "raw_note_text": raw_note,
        }
    )

    problems = []
    for condition, quote in zip(payload["conditions"], condition_quotes):
        provenance = SourceProvenance.from_note(encounter, quote)
        problems.append(
            ConditionAddressed(
                condition=EvidenceItem(
                    category="condition",
                    state=EvidenceState.PRESENT,
                    normalized_value=condition["name"],
                    provenance=(provenance,),
                ),
                addressed=EvidenceItem(
                    category="condition_addressed",
                    state=EvidenceState.PRESENT,
                    normalized_value=True,
                    provenance=(provenance,),
                ),
                status_complexity=(
                    EvidenceItem(
                        category="condition_status",
                        state=EvidenceState(condition["status_state"]),
                        normalized_value=condition["status_value"],
                        provenance=(provenance,),
                    ),
                ),
            )
        )

    medication_provenance = SourceProvenance.from_note(encounter, medication_quote)
    management = MedicationActivity(
        medication=EvidenceItem(
            category="medication",
            state=EvidenceState.PRESENT,
            normalized_value=medication["name"],
            provenance=(medication_provenance,),
        ),
        activity_type=EvidenceItem(
            category="medication_activity_type",
            state=EvidenceState.PRESENT,
            normalized_value=medication["action"],
            provenance=(medication_provenance,),
        ),
    )

    evidence = StructuredEvidence(
        encounter_id=encounter.encounter_id,
        workflow_stage=encounter.metadata.workflow_stage,
        provider_class=encounter.metadata.provider_class,
        conditions_addressed=tuple(problems),
        medication_activities=(management,),
        evaluation_management=EvaluationManagementEvidence(
            problems_addressed=tuple(problems),
            management_activities=(management,),
        ),
    )
    return encounter, evidence


class OutpatientEMMedicationManagementRuleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = _load_cases()
        cls.definition = outpatient_em_medication_management_rules()[0]

    def test_fixture_targets_the_implemented_rule(self):
        self.assertEqual(
            self.fixture["rule_id"],
            OUTPATIENT_EM_ESTABLISHED_99214_STABLE_CHRONIC_MEDICATION_PATHWAY,
        )

    def test_known_answer_cases(self):
        engine = RuleEngine((self.definition,))
        for payload in self.fixture["cases"]:
            with self.subTest(case_id=payload["case_id"]):
                encounter, evidence = _build_case(payload)
                evaluation = engine.evaluate(encounter, evidence)[0]
                self.assertIs(evaluation.outcome, RuleOutcome(payload["expected_outcome"]))
                self.assertTrue(evaluation.source_references)
                if evaluation.outcome is RuleOutcome.SUPPORTED:
                    self.assertTrue(evaluation.evidence_references)

    def test_rule_metadata_uses_current_primary_ama_sources(self):
        metadata = self.definition.metadata
        self.assertEqual(
            metadata.rule_id,
            OUTPATIENT_EM_ESTABLISHED_99214_STABLE_CHRONIC_MEDICATION_PATHWAY,
        )
        self.assertEqual(metadata.jurisdiction, "CPT_BASE")
        self.assertEqual(metadata.service_family, "OUTPATIENT_EM_MEDICATION_MANAGEMENT")
        self.assertEqual({source.authority for source in metadata.sources}, {"American Medical Association"})
        references = {source.reference for source in metadata.sources}
        self.assertIn("https://edhub.ama-assn.org/steps-forward/module/2844245", references)
        self.assertTrue(any("cpt-code-99214" in reference for reference in references))

    def test_supported_result_does_not_depend_on_provider_class_difference(self):
        engine = RuleEngine((self.definition,))
        supported_case = dict(self.fixture["cases"][0])
        for provider_class in ("PMHNP_NP", "PSYCHIATRIST"):
            with self.subTest(provider_class=provider_class):
                payload = dict(supported_case)
                payload["provider_class"] = provider_class
                payload["case_id"] = f"P2-PROVIDER-{provider_class}"
                encounter, evidence = _build_case(payload)
                evaluation = engine.evaluate(encounter, evidence)[0]
                self.assertIs(evaluation.outcome, RuleOutcome.SUPPORTED)

    def test_duplicate_actual_rule_id_fails_closed_to_review(self):
        encounter, evidence = _build_case(self.fixture["cases"][0])
        alternate_source = RuleSource(
            source_id="AMA-EM-OVERVIEW-2026",
            authority="American Medical Association",
            title="CPT Evaluation and Management",
            reference="https://www.ama-assn.org/practice-management/cpt/cpt-evaluation-and-management",
            verified_date="2026-08-13",
            version="Updated 2026-01-26",
        )
        conflicting_metadata = replace(self.definition.metadata, sources=(alternate_source,))

        def conflicting_evaluator(encounter, evidence):
            return RuleDecision(
                outcome=RuleOutcome.UNSUPPORTED,
                reason="synthetic conflicting implementation",
            )

        conflicting_definition = RuleDefinition(
            metadata=conflicting_metadata,
            evaluator=conflicting_evaluator,
        )
        evaluation = RuleEngine((self.definition, conflicting_definition)).evaluate(
            encounter, evidence
        )[0]

        self.assertIs(evaluation.outcome, RuleOutcome.REVIEW)
        self.assertIn("conflicting rule definitions", evaluation.reason)
        self.assertGreaterEqual(len(evaluation.source_references), 2)


if __name__ == "__main__":
    unittest.main()
