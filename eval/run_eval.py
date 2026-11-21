"""Evaluate the deterministic KYC demo against its compact gold standard."""
from __future__ import annotations

import json
import time
import sys
from pathlib import Path

from graph.workflow import run_pipeline
from schemas.models import ProjectState, RequirementItem

ROOT = Path(__file__).resolve().parents[1]


def _sample_inputs(scenario: str) -> list[str]:
    if scenario == "loan":
        return [(ROOT / "sample_inputs" / "loan_origination_case.txt").read_text(encoding="utf-8")]
    return [
        path.read_text(encoding="utf-8")
        for path in sorted((ROOT / "sample_inputs").glob("*.txt"))
        if path.name != "loan_origination_case.txt"
    ]


def _f1(precision: float, recall: float) -> float:
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0


def evaluate(scenario: str = "onboarding") -> dict[str, float | int | str]:
    gold_file = "gold_standard_loan.json" if scenario == "loan" else "gold_standard_kyc.json"
    gold = json.loads((Path(__file__).parent / gold_file).read_text(encoding="utf-8"))
    started = time.perf_counter()
    result = run_pipeline(ProjectState(
        scenario="instant_digital_personal_loan" if scenario == "loan" else "onboarding",
        project_id=f"{scenario}-evaluation", raw_inputs=_sample_inputs(scenario),
    ).model_dump(mode="json"))
    elapsed = time.perf_counter() - started
    requirements = [RequirementItem.model_validate(item) for item in result["requirements"]]
    quotes = " ".join(item.source_quote.lower() for item in requirements)
    expected = [term.lower() for term in gold["expected_requirement_terms"]]
    true_positive = sum(term in quotes for term in expected)
    matched_requirements = sum(
        any(term in item.source_quote.lower() for term in expected) for item in requirements
    )
    precision = matched_requirements / max(len(requirements), 1)
    recall = true_positive / max(len(expected), 1)
    ambiguity_hits = sum(
        any(term in item.source_quote.lower() for item in requirements if item.needs_clarification)
        for term in gold["expected_ambiguity_terms"]
    )
    conflicts = result.get("conflicts", [])
    expected_docs = set(gold["expected_citation_documents"])
    mapped_docs = {citation["document_title"] for item in result["requirements"]
                   for citation in item.get("applicable_regulations", [])}
    citations = [citation for item in result["requirements"] for citation in item.get("applicable_regulations", [])]
    grounded = sum(bool(citation.get("supporting_evidence") and citation.get("source_id")) for citation in citations)
    rankings = result["sdlc_recommendation"]["rankings"]
    expected_conflicts = [marker.lower() for marker in gold.get("expected_conflict_markers", [])]
    matched_conflicts = sum(
        any(marker in conflict["description"].lower() for conflict in conflicts)
        for marker in expected_conflicts
    )
    conflict_precision = matched_conflicts / max(len(conflicts), 1)
    conflict_recall = matched_conflicts / max(gold["expected_conflict_count"], 1)
    conflict_f1 = _f1(conflict_precision, conflict_recall)
    metrics: dict[str, float | int | str] = {
        "requirement_extraction_precision": round(precision, 3),
        "requirement_extraction_recall": round(recall, 3),
        "requirement_extraction_f1": round(_f1(precision, recall), 3),
        "ambiguity_detection_accuracy": round(ambiguity_hits / max(len(gold["expected_ambiguity_terms"]), 1), 3),
        "conflict_detection_accuracy": round(conflict_f1, 3),
        "regulatory_control_coverage": round(len(mapped_docs & expected_docs) / max(len(expected_docs), 1), 3),
        "citation_grounding_rate": round(grounded / max(len(citations), 1), 3),
        "hallucination_rate": round(1 - grounded / max(len(citations), 1), 3),
        "sdlc_top1_agreement": int(bool(rankings) and rankings[0]["model"] == gold["expected_sdlc_model"]),
        "end_to_end_seconds": round(elapsed, 3),
        "requirements_count": len(requirements),
        "conflicts_found": len(conflicts),
    }
    return metrics


if __name__ == "__main__":
    scenario_arg = sys.argv[1] if len(sys.argv) > 1 else "onboarding"
    if scenario_arg not in {"onboarding", "loan"}:
        raise SystemExit("Usage: python -m eval.run_eval [onboarding|loan]")
    for name, value in evaluate(scenario_arg).items():
        print(f"{name.replace('_', ' ').title():38} {value}")
