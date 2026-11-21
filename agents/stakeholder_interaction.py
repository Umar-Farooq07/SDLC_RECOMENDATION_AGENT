from __future__ import annotations

from typing import Any

from agents.common import as_state, audit
from schemas.models import ProjectState

INTERVIEW_TEMPLATES = {
    "Product Owner": ["What business outcome and activation SLA are required?",
                      "Which user journeys and exception paths must be supported?",
                      "What are the transaction limits and integration expectations?"],
    "Compliance Officer": ["Which KYC obligations and evidence must be satisfied before activation?",
                           "What are the retention, consent, and reporting requirements?"],
    "InfoSec Architect": ["Which authentication, encryption, RBAC, and audit controls are mandatory?",
                         "What threat, availability, and incident-response requirements apply?"],
    "Software Architect": ["Which systems, APIs, data contracts, and failure modes are in scope?",
                           "What are the integration and performance constraints?"],
    "Operations Lead": ["What are the support, monitoring, recovery, and service-level expectations?",
                        "Which operational handoffs and reconciliation windows apply?"],
}


def stakeholder_interaction(state: ProjectState | dict[str, Any]) -> dict[str, Any]:
    current = as_state(state)
    questions = INTERVIEW_TEMPLATES.get(current.active_stakeholder_role, INTERVIEW_TEMPLATES["Product Owner"])
    audit(current, "stakeholder_interaction", "Ingested supplied stakeholder material",
          evidence="\n".join(current.raw_inputs)[:1000])
    return {"follow_up_questions": questions if current.interactive_mode else []}


def get_interview_questions(role: str) -> list[str]:
    return INTERVIEW_TEMPLATES.get(role, INTERVIEW_TEMPLATES["Product Owner"]).copy()
