from __future__ import annotations

from typing import Any

from agents.common import as_state, audit
from rag.retriever import KnowledgeBaseRetriever
from schemas.models import Citation, ProjectState, RequirementItem


def map_compliance(requirements: list[RequirementItem], retriever: KnowledgeBaseRetriever | None = None) -> list[RequirementItem]:
    retriever = retriever or KnowledgeBaseRetriever()
    for item in requirements:
        matches = retriever.retrieve(item.statement + " " + item.source_quote, k=3)
        citations: list[Citation] = []
        for match in matches:
            citations.append(Citation(
                document_title=match.metadata.get("title", match.metadata.get("source", "Knowledge base")),
                section=match.metadata.get("section", "Unspecified"),
                jurisdiction=match.metadata.get("jurisdiction", "India"),
                version=match.metadata.get("version", "2025"),
                effective_date=match.metadata.get("effective_date", "2025-01-01"),
                supporting_evidence=match.text, source_id=match.metadata.get("source", ""),
            ))
        item.applicable_regulations = citations
        query = (item.statement + " " + item.source_quote).lower()
        high_impact = any(term in query for term in
                          ("kyc", "activation", "consent", "retention", "disbursal", "account opening"))
        item.requires_legal_signoff = not citations or item.confidence_score < 0.75 or high_impact
        if "activation" in query and not any("audit" in c.supporting_evidence.lower() for c in citations):
            item.compliance_gaps.append("Confirm applicable pre-activation verification and audit evidence.")
        if any(word in query for word in ("retain", "retention", "indefinite")):
            item.retention_or_reporting_obligation = "Apply purpose-specific retention and any statutory banking retention override."
        if not citations:
            item.compliance_gaps.append("No grounded knowledge-base citation found; legal review required.")
    return requirements


def compliance(state: ProjectState | dict[str, Any]) -> dict[str, Any]:
    current = as_state(state)
    reqs = map_compliance([RequirementItem.model_validate(item) for item in current.requirements])
    evidence = "; ".join(c.document_title for item in reqs for c in item.applicable_regulations[:1])
    audit(current, "compliance", "Retrieved regulatory and internal policy evidence",
          evidence=evidence[:1000], details={"mapped_requirements": len(reqs)})
    return {"compliance_results": [item.model_dump(mode="json") for item in reqs]}
