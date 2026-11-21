from __future__ import annotations

from typing import Any

from agents.common import as_state, audit
from schemas.models import ProjectState, RequirementItem


def assess_risks(requirements: list[RequirementItem]) -> list[RequirementItem]:
    for item in requirements:
        text = f"{item.statement} {item.source_quote}".lower()
        sensitive = any(term in text for term in ("kyc", "identity", "video", "consent", "activation", "security"))
        item.likelihood = 4 if sensitive else 3
        item.impact = 5 if any(term in text for term in ("activation", "retention", "kyc", "security")) else 3
        score = item.likelihood * item.impact
        item.risk_level = "Critical" if score >= 20 else "High" if score >= 15 else "Medium" if score >= 8 else "Low"
        item.failure_consequences = ["Regulatory breach, customer harm, or onboarding failure"]
        item.mitigations = ["Enforce preventive controls, test failure paths, monitor evidence, and require accountable sign-off"]
    return requirements


def risk_analysis(state: ProjectState | dict[str, Any]) -> dict[str, Any]:
    current = as_state(state)
    reqs = assess_risks([RequirementItem.model_validate(item) for item in current.requirements])
    audit(current, "risk_analysis", "Scored business, technical, operational, security, and compliance risk")
    return {"risk_results": [item.model_dump(mode="json") for item in reqs]}
