import json
import unittest

from claimlens.encounter import Encounter
from claimlens.evidence import EvidenceState, TemporalScope, extract_evidence
from claimlens.ollama import OllamaEvidenceExtractor, SCHEMA


class OllamaEvidenceExtractorTests(unittest.TestCase):
    def setUp(self):
        self.encounter = Encounter.from_dict(
            {
                "metadata": {
                    "encounter_id": "OLLAMA-TEST-001",
                    "workflow_stage": "PRE_SIGN",
                    "provider_class": "PMHNP_NP",
                },
                "raw_note_text": (
                    "Anxiety remains symptomatic. "
                    "Continue sertraline 50 mg daily. "
                    "No medication side effects."
                ),
            }
        )

    def test_structured_response_maps_to_frozen_evidence_contract(self):
        captured = {}

        def transport(url, payload, timeout):
            captured["url"] = url
            captured["payload"] = payload
            content = {
                "conditions_addressed": [
                    {
                        "condition": "anxiety",
                        "state": "PRESENT",
                        "temporal_scope": "CURRENT_ENCOUNTER",
                        "source_quotes": ["Anxiety remains symptomatic."],
                    }
                ],
                "medication_activities": [
                    {
                        "medication": "sertraline",
                        "activity_type": "continue",
                        "state": "PRESENT",
                        "temporal_scope": "CURRENT_ENCOUNTER",
                        "source_quotes": ["Continue sertraline 50 mg daily."],
                    }
                ],
                "additional_items": [
                    {
                        "category": "medication_adverse_effect",
                        "state": "ABSENT",
                        "normalized_value": None,
                        "temporal_scope": "CURRENT_ENCOUNTER",
                        "source_quotes": ["No medication side effects."],
                    }
                ],
            }
            return {"message": {"content": json.dumps(content)}}

        extractor = OllamaEvidenceExtractor(transport=transport)
        evidence = extract_evidence(self.encounter, extractor)

        self.assertEqual(captured["url"], "http://localhost:11434/api/chat")
        self.assertEqual(captured["payload"]["model"], "medgemma1.5")
        self.assertFalse(captured["payload"]["stream"])
        self.assertEqual(captured["payload"]["format"], SCHEMA)
        self.assertEqual(captured["payload"]["options"]["temperature"], 0)
        self.assertEqual(
            evidence.medication_activities[0].activity_type.normalized_value,
            "continue",
        )
        self.assertIs(
            evidence.medication_activities[0].activity_type.temporal_scope,
            TemporalScope.CURRENT_ENCOUNTER,
        )
        self.assertIs(evidence.additional_items[0].state, EvidenceState.ABSENT)

    def test_untraceable_model_quote_fails_closed(self):
        def transport(url, payload, timeout):
            content = {
                "conditions_addressed": [],
                "medication_activities": [
                    {
                        "medication": "sertraline",
                        "activity_type": "continue",
                        "state": "PRESENT",
                        "temporal_scope": "CURRENT_ENCOUNTER",
                        "source_quotes": ["Continue sertraline 100 mg daily."],
                    }
                ],
                "additional_items": [],
            }
            return {"message": {"content": json.dumps(content)}}

        with self.assertRaises(ValueError):
            extract_evidence(
                self.encounter,
                OllamaEvidenceExtractor(transport=transport),
            )

    def test_malformed_ollama_content_fails_closed(self):
        def transport(url, payload, timeout):
            return {"message": {"content": "not-json"}}

        with self.assertRaises(RuntimeError):
            extract_evidence(
                self.encounter,
                OllamaEvidenceExtractor(transport=transport),
            )


if __name__ == "__main__":
    unittest.main()
