import json
from pathlib import Path
import unittest

from claimlens.encounter import Encounter
from claimlens.evidence import (
    DevelopmentPatternExtractor,
    EvidenceItem,
    EvidenceState,
    SourceProvenance,
    StructuredEvidence,
    TemporalScope,
    extract_evidence,
    validate_structured_evidence,
)

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "data/development_cases/phase1_baseline_cases.json").read_text())


class EvidenceContractTests(unittest.TestCase):
    def test_note_provenance_requires_exact_source_text(self):
        encounter = Encounter.from_dict(CASES[0])
        source = SourceProvenance.from_note(encounter, "Continue sertraline 50 mg daily.")
        self.assertEqual(encounter.raw_note_text[source.start_char:source.end_char], source.quote)
        with self.assertRaises(ValueError):
            SourceProvenance.from_note(encounter, "Continue sertraline 100 mg daily.")

    def test_material_uncertainty_is_preserved_for_review(self):
        encounter = Encounter.from_dict(CASES[0])
        source = SourceProvenance.from_note(encounter, "Continue sertraline 50 mg daily.")
        item = EvidenceItem(
            category="test",
            state=EvidenceState.AMBIGUOUS,
            temporal_scope=TemporalScope.CURRENT_ENCOUNTER,
            provenance=(source,),
        )
        evidence = StructuredEvidence(
            encounter_id=encounter.encounter_id,
            workflow_stage=encounter.metadata.workflow_stage,
            provider_class=encounter.metadata.provider_class,
            additional_items=(item,),
        )
        self.assertEqual(len(evidence.review_reasons), 1)

    def test_validator_rejects_cross_encounter_provenance(self):
        first = Encounter.from_dict(CASES[0])
        second_payload = dict(CASES[0])
        second_payload["metadata"] = dict(second_payload["metadata"])
        second_payload["metadata"]["encounter_id"] = "OTHER"
        second = Encounter.from_dict(second_payload)
        source = SourceProvenance.from_note(first, "Continue sertraline 50 mg daily.")
        item = EvidenceItem(category="test", state=EvidenceState.PRESENT, provenance=(source,))
        evidence = StructuredEvidence(
            encounter_id=second.encounter_id,
            workflow_stage=second.metadata.workflow_stage,
            provider_class=second.metadata.provider_class,
            additional_items=(item,),
        )
        with self.assertRaises(ValueError):
            validate_structured_evidence(evidence, second)


class DevelopmentBaselineTests(unittest.TestCase):
    def test_seed_cases_match_phase1_expected_behavior(self):
        extractor = DevelopmentPatternExtractor()
        for case in CASES:
            with self.subTest(case=case["case_id"]):
                encounter = Encounter.from_dict(case)
                evidence = extract_evidence(encounter, extractor)
                expected = case["expected"]

                current = sorted(
                    [
                        [activity.medication.normalized_value, activity.activity_type.normalized_value]
                        for activity in evidence.medication_activities
                        if activity.medication is not None
                        and activity.activity_type.temporal_scope is TemporalScope.CURRENT_ENCOUNTER
                    ]
                )
                historical = sorted(
                    [
                        [activity.medication.normalized_value, activity.activity_type.normalized_value]
                        for activity in evidence.medication_activities
                        if activity.medication is not None
                        and activity.activity_type.temporal_scope is TemporalScope.HISTORICAL
                    ]
                )
                medication_list_presence = sum(
                    1 for item in evidence.additional_items if item.category == "medication_list_presence"
                )
                contradictions = sum(
                    1 for item in evidence.additional_items if item.state is EvidenceState.CONTRADICTORY
                )

                self.assertEqual(current, sorted(expected["current_medication_actions"]))
                self.assertEqual(historical, sorted(expected["historical_medication_actions"]))
                self.assertEqual(bool(evidence.review_reasons), expected["requires_review"])
                self.assertEqual(medication_list_presence, expected["medication_list_presence"])
                self.assertEqual(contradictions, expected["contradictions"])


if __name__ == "__main__":
    unittest.main()
