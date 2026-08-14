"""ClaimLens runtime orchestration entry point.

Phase 1 currently exposes only the encounter/evidence development baseline. Later
rules, compiler, auditor, payer, and final-result stages remain gate-blocked.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

from .encounter import Encounter
from .evidence import EvidenceState, TemporalScope, extract_evidence
from .ollama import OllamaEvidenceExtractor

ROOT = Path(__file__).resolve().parents[2]
CASES_PATH = ROOT / "data" / "development_cases" / "phase1_baseline_cases.json"
PROMPT_PATH = ROOT / "prompts" / "extract_evidence.txt"
OUTPUT_PATH = ROOT / "output" / "phase1_medgemma_baseline.json"


def run_phase1_baseline(*, limit: int | None = None) -> dict:
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    if limit is not None:
        if limit < 1:
            raise ValueError("limit must be at least 1")
        cases = cases[:limit]

    extractor = OllamaEvidenceExtractor.from_environment(
        extraction_prompt=PROMPT_PATH.read_text(encoding="utf-8")
    )
    rows = []
    valid = exact = review_correct = 0
    current_tp = current_fp = current_fn = 0
    historical_tp = historical_fp = historical_fn = 0
    run_started = time.perf_counter()

    for index, case in enumerate(cases, start=1):
        expected = case["expected"]
        case_id = case["case_id"]
        row = {"case_id": case_id}
        case_started = time.perf_counter()
        print(
            f"[{index}/{len(cases)}] Running {case_id}...",
            file=sys.stderr,
            flush=True,
        )
        try:
            evidence = extract_evidence(Encounter.from_dict(case), extractor)
            valid += 1
            current = _action_pairs(evidence, TemporalScope.CURRENT_ENCOUNTER)
            historical = _action_pairs(evidence, TemporalScope.HISTORICAL)
            expected_current = _pairs(expected["current_medication_actions"])
            expected_historical = _pairs(expected["historical_medication_actions"])
            current_tp += len(current & expected_current)
            current_fp += len(current - expected_current)
            current_fn += len(expected_current - current)
            historical_tp += len(historical & expected_historical)
            historical_fp += len(historical - expected_historical)
            historical_fn += len(expected_historical - historical)

            review = bool(evidence.review_reasons)
            expected_review = bool(expected["requires_review"])
            review_ok = review == expected_review
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
                and historical == expected_historical
                and review_ok
                and med_list == expected["medication_list_presence"]
                and contradictions == expected["contradictions"]
            )
            exact += int(case_exact)
            row.update(
                {
                    "status": "ok",
                    "exact_match": case_exact,
                    "duration_seconds": round(time.perf_counter() - case_started, 3),
                    "current_actions": _sorted_pairs(current),
                    "expected_current_actions": _sorted_pairs(expected_current),
                    "historical_actions": _sorted_pairs(historical),
                    "expected_historical_actions": _sorted_pairs(expected_historical),
                    "requires_review": review,
                    "expected_requires_review": expected_review,
                    "medication_list_presence": med_list,
                    "expected_medication_list_presence": expected["medication_list_presence"],
                    "contradictions": contradictions,
                    "expected_contradictions": expected["contradictions"],
                }
            )
            print(
                f"[{index}/{len(cases)}] {case_id}: "
                f"{'MATCH' if case_exact else 'MISMATCH'} "
                f"({row['duration_seconds']}s)",
                file=sys.stderr,
                flush=True,
            )
        except Exception as exc:
            row.update(
                {
                    "status": "error",
                    "duration_seconds": round(time.perf_counter() - case_started, 3),
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
            print(
                f"[{index}/{len(cases)}] {case_id}: ERROR "
                f"({row['duration_seconds']}s) {row['error']}",
                file=sys.stderr,
                flush=True,
            )
        rows.append(row)

    count = len(cases)
    report = {
        "runtime": "Ollama local API",
        "model": extractor.model,
        "cases": count,
        "duration_seconds": round(time.perf_counter() - run_started, 3),
        "metrics": {
            "valid_output_rate": _ratio(valid, count),
            "exact_case_rate": _ratio(exact, count),
            "review_accuracy": _ratio(review_correct, count),
            "current_action_precision": _precision(current_tp, current_fp),
            "current_action_recall": _recall(current_tp, current_fn),
            "historical_action_precision": _precision(historical_tp, historical_fp),
            "historical_action_recall": _recall(historical_tp, historical_fn),
            "unsupported_current_actions": current_fp,
            "missed_current_actions": current_fn,
        },
        "results": rows,
    }

    output_path = (
        OUTPUT_PATH
        if limit is None
        else OUTPUT_PATH.with_name(f"phase1_medgemma_baseline_limit{limit}.json")
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
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


def _sorted_pairs(values):
    return sorted([list(value) for value in values])


def _ratio(a, b):
    return None if b == 0 else round(a / b, 4)


def _precision(tp, fp):
    return None if tp + fp == 0 else round(tp / (tp + fp), 4)


def _recall(tp, fn):
    return None if tp + fn == 0 else round(tp / (tp + fn), 4)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--phase1-baseline",
        action="store_true",
        help="Run the local MedGemma/Ollama evidence baseline.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Run only the first N development cases for a quick diagnostic.",
    )
    args = parser.parse_args()
    if not args.phase1_baseline:
        parser.error("Phase 1 currently supports only --phase1-baseline")
    print(json.dumps(run_phase1_baseline(limit=args.limit), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
