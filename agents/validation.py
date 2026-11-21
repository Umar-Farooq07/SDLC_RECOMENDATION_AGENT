from __future__ import annotations

from typing import Any

from agents.common import as_state, audit
from rag.retriever import KnowledgeBaseRetriever
from schemas.models import ProjectState, ValidationReport


def validate_project(state: ProjectState) -> ValidationReport:
    ids = {item.req_id for item in state.requirements}
    retriever = KnowledgeBaseRetriever()
    grounded_citations = True
    for item in state.requirements:
        retrieved = retriever.retrieve(item.statement + " " + item.source_quote, k=4)
        allowed = {(match.metadata.get("source", ""), match.text) for match in retrieved}
        for citation in item.applicable_regulations:
            if (citation.source_id, citation.supporting_evidence) not in allowed:
                grounded_citations = False
    checks = {
        "requirements_present": bool(ids),
        "all_requirements_have_acceptance_criteria": all(item.acceptance_criteria for item in state.requirements),
        "requirements_in_srs": all(req_id in state.artifacts.get("srs.md", "") for req_id in ids),
        "requirements_in_rtm": all(req_id in state.artifacts.get("rtm.md", "") for req_id in ids),
        "requirements_in_compliance_matrix": all(
            req_id in state.artifacts.get("compliance_matrix.md", "") for req_id in ids
        ),
        "citations_grounded_in_retrieval": grounded_citations,
        "high_severity_conflicts_flagged": all(
            conflict.requires_human_resolution for conflict in state.conflicts
            if conflict.severity in {"Critical", "High"}
        ),
        "sdlc_recommendation_present": bool(state.sdlc_recommendation.selected_model),
    }
    issues = [name for name, passed in checks.items() if not passed]
    return ValidationReport(passed=not issues, checks=checks,
                            quality_score=sum(checks.values()) / max(len(checks), 1), issues=issues)


def validation(state: ProjectState | dict[str, Any]) -> dict[str, Any]:
    current = as_state(state)
    report = validate_project(current)
    audit(current, "validation", "Completed artifact consistency and citation checks",
          confidence=report.quality_score, evidence="; ".join(report.issues) or "All validation checks passed")
    return {"validation_report": report.model_dump(mode="json")}
