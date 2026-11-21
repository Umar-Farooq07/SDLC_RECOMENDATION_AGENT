from __future__ import annotations

from typing import Any

from agents.common import as_state, audit
from schemas.models import ProjectState


def coordinator(state: ProjectState | dict[str, Any]) -> dict[str, Any]:
    current = as_state(state)
    audit(current, "coordinator", "Initialized workflow and selected elicitation route")
    return {"pipeline_status": "processing", "max_clarification_rounds": current.max_clarification_rounds}
