import json
import unittest

from claimlens.encounter import Encounter
from claimlens.evidence import EvidenceState, TemporalScope, extract_evidence
from claimlens.ollama import (
    MEDICATION_ACTIVITY_TYPES,
    OllamaEvidenceExtractor,
    SCHEMA,
)


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

    def test_schema_does_not_allow_status_words_as_medication_actions(self):
        action_schema = SCHEMA["properties"]["medication_activities"]["items"]["properties"]["activity_type"]
        self.assertEqual(action_schema["enum"], list(MEDICATION_ACTIVITY_TYPES))
        self.assertNotIn("current", action_schema["enum"])
        self.assertNotIn("medication_list_presence", action_schema["enum"])

    def test_named_action_requires_medication_and_action_in_same_source_quote(self):
        encounter = Encounter.from_dict(
            {
                "metadata": {
                    "encounter_id": "OLLAMA-TEST-LINKAGE",
                    "workflow_stage": "PRE_SUBMIT",
                    "provider_class": "PSYCHIATRIST",
                },
                "raw_note_text": (
                    "Lamotrigine 100 mg daily appears on the current medication list. "
                    "For now, continue current medications."
                ),
            }
        )

        def transport(url, payload, timeout):
            content = {
                "conditions_addressed": [],
                "medication_activities": [
                    {
                        "medication": "lamotrigine",
                        "activity_type": "continue",
                        "state": "PRESENT",
                        "temporal_scope": "CURRENT_ENCOUNTER",
                        "source_quotes": [
                            "Lamotrigine 100 mg daily appears on the current medication list.",
                            "For now, continue current medications.",
                        ],
                    }
                ],
                "additional_items": [],
            }
            return {"message": {"content": json.dumps(content)}}

        with self.assertRaises(ValueError):
            extract_evidence(encounter, OllamaEvidenceExtractor(transport=transport))

    def test_explicit_conflicting_actions_derive_reviewable_contradiction(self):
        encounter = Encounter.from_dict(
            {
                "metadata": {
                    "encounter_id": "OLLAMA-TEST-CONTRADICTION",
                    "workflow_stage": "PRE_SUBMIT",
                    "provider_class": "PMHNP_NP",
                },
                "raw_note_text": (
                    "Continue fluoxetine 20 mg daily. "
                    "Stop fluoxetine because of nausea."
                ),
            }
        )

        def transport(url, payload, timeout):
            content = {
                "conditions_addressed": [],
                "medication_activities": [
                    {
                        "medication": "fluoxetine",
                        "activity_type": "continue",
                        "state": "PRESENT",
                        "temporal_scope": "CURRENT_ENCOUNTER",
                        "source_quotes": ["Continue fluoxetine 20 mg daily."],
                    },
                    {
                        "medication": "fluoxetine",
                        "activity_type": "stop",
                        "state": "PRESENT",
                        "temporal_scope": "CURRENT_ENCOUNTER",
                        "source_quotes": ["Stop fluoxetine because of nausea."],
                    },
                ],
                "additional_items": [],
            }
            return {"message": {"content": json.dumps(content)}}

        evidence = extract_evidence(encounter, OllamaEvidenceExtractor(transport=transport))
        contradictions = [
            item for item in evidence.additional_items
            if item.state is EvidenceState.CONTRADICTORY
        ]
        self.assertEqual(len(contradictions), 1)
        self.assertEqual(len(evidence.review_reasons), 1)

    def test_medication_list_evidence_requires_explicit_list_language(self):
        def transport(url, payload, timeout):
            content = {
                "conditions_addressed": [],
                "medication_activities": [],
                "additional_items": [
                    {
                        "category": "medication_list_presence",
                        "state": "PRESENT",
                        "normalized_value": "sertraline 50 mg daily",
                        "temporal_scope": "CURRENT_ENCOUNTER",
                        "source_quotes": ["Continue sertraline 50 mg daily."],
                    }
                ],
            }
            return {"message": {"content": json.dumps(content)}}

        evidence = extract_evidence(self.encounter, OllamaEvidenceExtractor(transport=transport))
        self.assertEqual(evidence.additional_items, ())

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
