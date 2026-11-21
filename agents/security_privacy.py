from __future__ import annotations

from typing import Any

from agents.common import as_state, audit
from schemas.models import ProjectState, RequirementItem

MANDATORY_CONTROLS = [
    "TLS 1.3 for data in transit", "AES-256 encryption at rest", "MFA/step-up authentication",
    "Role-based access control (RBAC)", "15-minute idle session timeout",
    "Consent capture and purpose limitation", "Immutable audit-trail logging to SIEM",
    "Data minimization and controlled retention",
]


def apply_security_controls(requirements: list[RequirementItem]) -> list[RequirementItem]:
    for item in requirements:
        item.security_controls = list(MANDATORY_CONTROLS)
        item.assumptions.append("Control applicability and implementation details require bank security/privacy review.")
    return requirements


def security_privacy(state: ProjectState | dict[str, Any]) -> dict[str, Any]:
    current = as_state(state)
    reqs = apply_security_controls([RequirementItem.model_validate(item) for item in current.requirements])
    audit(current, "security_privacy", "Attached mandatory security and privacy control baseline",
          evidence="; ".join(MANDATORY_CONTROLS))
    return {"security_results": [item.model_dump(mode="json") for item in reqs]}
