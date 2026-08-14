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

    def test_unlinked_named_action_is_removed_and_escalated(self):
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

        evidence = extract_evidence(encounter, OllamaEvidenceExtractor(transport=transport))
        self.assertEqual(evidence.medication_activities, ())
        self.assertTrue(evidence.review_reasons)
        self.assertTrue(
            any(item.category == "medication_linkage" for item in evidence.additional_items)
        )
        self.assertTrue(
            any(item.category == "medication_list_presence" for item in evidence.additional_items)
        )

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

    def test_explicit_medication_list_is_preserved_when_model_omits_it(self):
        encounter = Encounter.from_dict(
            {
                "metadata": {
                    "encounter_id": "OLLAMA-TEST-LIST",
                    "workflow_stage": "PRE_SIGN",
                    "provider_class": "PMHNP_NP",
                },
                "raw_note_text": "Current medication list: bupropion XL 150 mg daily.",
            }
        )

        def transport(url, payload, timeout):
            return {
                "message": {
                    "content": json.dumps(
                        {
                            "conditions_addressed": [],
                            "medication_activities": [],
                            "additional_items": [],
                        }
                    )
                }
            }

        evidence = extract_evidence(encounter, OllamaEvidenceExtractor(transport=transport))
        self.assertEqual(
            sum(item.category == "medication_list_presence" for item in evidence.additional_items),
            1,
        )

    def test_generic_continue_current_medications_is_ambiguous_even_if_model_omits_it(self):
        encounter = Encounter.from_dict(
            {
                "metadata": {
                    "encounter_id": "OLLAMA-TEST-GENERIC",
                    "workflow_stage": "PRE_SUBMIT",
                    "provider_class": "PSYCHIATRIST",
                },
                "raw_note_text": "For now, continue current medications.",
            }
        )

        def transport(url, payload, timeout):
            return {
                "message": {
                    "content": json.dumps(
                        {
                            "conditions_addressed": [],
                            "medication_activities": [],
                            "additional_items": [],
                        }
                    )
                }
            }

        evidence = extract_evidence(encounter, OllamaEvidenceExtractor(transport=transport))
        self.assertTrue(evidence.review_reasons)
        self.assertTrue(
            any(item.category == "medication_linkage" for item in evidence.additional_items)
        )

    def test_explicit_historical_change_is_preserved_when_model_omits_it(self):
        encounter = Encounter.from_dict(
            {
                "metadata": {
                    "encounter_id": "OLLAMA-TEST-HISTORY",
                    "workflow_stage": "PRE_SIGN",
                    "provider_class": "PSYCHIATRIST",
                },
                "raw_note_text": (
                    "Prior-visit history copied into today's note: aripiprazole was increased "
                    "from 5 mg to 10 mg daily at the previous appointment."
                ),
            }
        )

        def transport(url, payload, timeout):
            return {
                "message": {
                    "content": json.dumps(
                        {
                            "conditions_addressed": [],
                            "medication_activities": [],
                            "additional_items": [],
                        }
                    )
                }
            }

        evidence = extract_evidence(encounter, OllamaEvidenceExtractor(transport=transport))
        historical = [
            activity for activity in evidence.medication_activities
            if activity.activity_type.temporal_scope is TemporalScope.HISTORICAL
        ]
        self.assertEqual(len(historical), 1)
        self.assertEqual(historical[0].medication.normalized_value, "aripiprazole")
        self.assertEqual(historical[0].activity_type.normalized_value, "increase")

    def test_explicit_current_actions_are_preserved_when_model_omits_one_side(self):
        encounter = Encounter.from_dict(
            {
                "metadata": {
                    "encounter_id": "OLLAMA-TEST-CURRENT-GUARDRAIL",
                    "workflow_stage": "PRE_SUBMIT",
                    "provider_class": "PMHNP_NP",
                },
                "raw_note_text": (
                    "Assessment: continue fluoxetine 20 mg daily. "
                    "Plan: stop fluoxetine because of nausea and reassess at follow-up."
                ),
            }
        )

        def transport(url, payload, timeout):
            content = {
                "conditions_addressed": [],
                "medication_activities": [
                    {
                        "medication": "fluoxetine",
                        "activity_type": "stop",
                        "state": "PRESENT",
                        "temporal_scope": "CURRENT_ENCOUNTER",
                        "source_quotes": [
                            "Plan: stop fluoxetine because of nausea and reassess at follow-up."
                        ],
                    }
                ],
                "additional_items": [],
            }
            return {"message": {"content": json.dumps(content)}}

        evidence = extract_evidence(encounter, OllamaEvidenceExtractor(transport=transport))
        actions = {
            (
                activity.medication.normalized_value,
                activity.activity_type.normalized_value,
            )
            for activity in evidence.medication_activities
        }
        self.assertEqual(
            actions,
            {("fluoxetine", "continue"), ("fluoxetine", "stop")},
        )
        self.assertEqual(
            sum(item.state is EvidenceState.CONTRADICTORY for item in evidence.additional_items),
            1,
        )
        self.assertTrue(evidence.review_reasons)

    def test_conditional_named_action_is_not_promoted_by_guardrail(self):
        encounter = Encounter.from_dict(
            {
                "metadata": {
                    "encounter_id": "OLLAMA-TEST-CONDITIONAL-GUARDRAIL",
                    "workflow_stage": "PRE_SIGN",
                    "provider_class": "PMHNP_NP",
                },
                "raw_note_text": "Today we could increase fluoxetine next month if symptoms worsen.",
            }
        )

        def transport(url, payload, timeout):
            return {
                "message": {
                    "content": json.dumps(
                        {
                            "conditions_addressed": [],
                            "medication_activities": [],
                            "additional_items": [],
                        }
                    )
                }
            }

        evidence = extract_evidence(encounter, OllamaEvidenceExtractor(transport=transport))
        self.assertEqual(evidence.medication_activities, ())

    def test_medication_list_presence_deduplicates_overlapping_source_quotes(self):
        encounter = Encounter.from_dict(
            {
                "metadata": {
                    "encounter_id": "OLLAMA-TEST-LIST-DEDUP",
                    "workflow_stage": "PRE_SIGN",
                    "provider_class": "PMHNP_NP",
                },
                "raw_note_text": "Current medication list: bupropion XL 150 mg daily.",
            }
        )

        def transport(url, payload, timeout):
            content = {
                "conditions_addressed": [],
                "medication_activities": [],
                "additional_items": [
                    {
                        "category": "medication_list_presence",
                        "state": "PRESENT",
                        "normalized_value": "bupropion xl 150 mg daily",
                        "temporal_scope": "CURRENT_ENCOUNTER",
                        "source_quotes": [
                            "Current medication list: bupropion XL 150 mg daily"
                        ],
                    }
                ],
            }
            return {"message": {"content": json.dumps(content)}}

        evidence = extract_evidence(encounter, OllamaEvidenceExtractor(transport=transport))
        self.assertEqual(
            sum(item.category == "medication_list_presence" for item in evidence.additional_items),
            1,
        )

    def test_separate_medication_list_statements_remain_separate(self):
        encounter = Encounter.from_dict(
            {
                "metadata": {
                    "encounter_id": "OLLAMA-TEST-LIST-SEPARATE",
                    "workflow_stage": "PRE_SIGN",
                    "provider_class": "PMHNP_NP",
                },
                "raw_note_text": (
                    "Current medication list: bupropion XL 150 mg daily. "
                    "Current medication list: buspirone 10 mg twice daily."
                ),
            }
        )

        def transport(url, payload, timeout):
            return {
                "message": {
                    "content": json.dumps(
                        {
                            "conditions_addressed": [],
                            "medication_activities": [],
                            "additional_items": [],
                        }
                    )
                }
            }

        evidence = extract_evidence(encounter, OllamaEvidenceExtractor(transport=transport))
        self.assertEqual(
            sum(item.category == "medication_list_presence" for item in evidence.additional_items),
            2,
        )

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
