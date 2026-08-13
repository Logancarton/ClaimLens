import unittest

from claimlens.encounter import Encounter, EncounterMetadata, PatientStatus, ProviderClass, WorkflowStage


class EncounterContractTests(unittest.TestCase):
    def test_preserves_explicit_workflow_and_provider_class(self):
        encounter = Encounter(
            metadata=EncounterMetadata(
                encounter_id="E-1",
                workflow_stage=WorkflowStage.PRE_SIGN,
                provider_class=ProviderClass.PMHNP_NP,
                patient_status=PatientStatus.ESTABLISHED,
            ),
            raw_note_text="Synthetic note text.",
        )
        self.assertEqual(encounter.metadata.workflow_stage, WorkflowStage.PRE_SIGN)
        self.assertEqual(encounter.metadata.provider_class, ProviderClass.PMHNP_NP)

    def test_round_trip_keeps_unknown_optional_metadata_unknown(self):
        payload = {
            "metadata": {
                "encounter_id": "E-2",
                "workflow_stage": "PRE_SUBMIT",
                "provider_class": "PSYCHIATRIST",
                "patient_status": "UNKNOWN",
            },
            "raw_note_text": "Synthetic finalized note.",
        }
        serialized = Encounter.from_dict(payload).to_dict()
        self.assertEqual(serialized["metadata"]["patient_status"], "UNKNOWN")
        self.assertIsNone(serialized["metadata"]["date_of_service"])
        self.assertIsNone(serialized["metadata"]["place_of_service"])

    def test_rejects_blank_source_note(self):
        with self.assertRaises(ValueError):
            Encounter(
                metadata=EncounterMetadata(
                    encounter_id="E-3",
                    workflow_stage=WorkflowStage.PRE_SIGN,
                    provider_class=ProviderClass.PMHNP_NP,
                ),
                raw_note_text="   ",
            )


if __name__ == "__main__":
    unittest.main()
