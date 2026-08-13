"""ClaimLens runtime orchestration entry point.

Phase 1 currently exposes only the encounter/evidence development baseline. Later
rules, compiler, auditor, payer, and final-result stages remain gate-blocked.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .encounter import Encounter
from .evidence import EvidenceState, TemporalScope, extract_evidence
from .ollama import OllamaEvidenceExtractor

ROOT = Path(__file__).resolve().parents[2]
CASES_PATH = ROOT / "data" / "development_cases" / "phase1_baseline_cases.json"
PROMPT_PATH = ROOT / "prompts" / "extract_evidence.txt"
OUTPUT_PATH = ROOT / "output" / "phase1_medgemma_baseline.json"


def run_phase1_baseline() -> dict:
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    extractor = OllamaEvidenceExtractor.from_environment(
        extraction_prompt=PROMPT_PATH.read_text(encoding="utf-8")
    )
    rows = []
    valid = exact = review_correct = 0
    current_tp = current_fp = current_fn = 0

    for case in cases:
        expected = case["expected"]
        row = {"case_id": case["case_id"]}
        try:
            evidence = extract_evidence(Encounter.from_dict(case), extractor)
            valid += 1
            current = _action_pairs(evidence, TemporalScope.CURRENT_ENCOUNTER)
            expected_current = _pairs(expected["current_medication_actions"])
            current_tp += len(current & expected_current)
            current_fp += len(current - expected_current)
            current_fn += len(expected_current - current)
            review = bool(evidence.review_reasons)
            review_ok = review == expected["requires_review"]
            review_correct += int(review_ok)
            med_list = sum(
                item.category == "medication_list_presence"
                for item in evidence.additional_items
            )
            contradictions = sum(
                item.state is EvidenceState.CONTRADICTORY
                for item in evidence.additional_items
            )
            case_exact = (
                current == expected_current
                and review_ok
                and med_list == expected["medication_list_presence"]
                and contradictions == expected["contradictions"]
            )
            exact += int(case_exact)
            row.update({"status": "ok", "exact_match": case_exact})
        except Exception as exc:
            row.update({"status": "error", "error": f"{type(exc).__name__}: {exc}"})
        rows.append(row)

    count = len(cases)
    report = {
        "runtime": "Ollama local API",
        "model": extractor.model,
        "cases": count,
        "metrics": {
            "valid_output_rate": _ratio(valid, count),
            "exact_case_rate": _ratio(exact, count),
            "review_accuracy": _ratio(review_correct, count),
            "current_action_precision": _precision(current_tp, current_fp),
            "current_action_recall": _recall(current_tp, current_fn),
            "unsupported_current_actions": current_fp,
            "missed_current_actions": current_fn,
        },
        "results": rows,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def _action_pairs(evidence, scope):
    return {
        (
            str(activity.medication.normalized_value).lower(),
            str(activity.activity_type.normalized_value).lower(),
        )
        for activity in evidence.medication_activities
        if activity.medication is not None
        and activity.activity_type.temporal_scope is scope
    }


def _pairs(values):
    return {(str(a).lower(), str(b).lower()) for a, b in values}


def _ratio(a, b):
    return 0.0 if b == 0 else round(a / b, 4)


def _precision(tp, fp):
    return 1.0 if tp + fp == 0 else round(tp / (tp + fp), 4)


def _recall(tp, fn):
    return 1.0 if tp + fn == 0 else round(tp / (tp + fn), 4)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--phase1-baseline",
        action="store_true",
        help="Run the local MedGemma/Ollama evidence baseline.",
    )
    args = parser.parse_args()
    if not args.phase1_baseline:
        parser.error("Phase 1 currently supports only --phase1-baseline")
    print(json.dumps(run_phase1_baseline(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
