from __future__ import annotations

from typing import Any

from agents.common import as_state, audit
from schemas.models import ProjectState, RequirementItem
from sdlc_engine.selector import default_factors, select_sdlc


def sdlc_selection(state: ProjectState | dict[str, Any]) -> dict[str, Any]:
    current = as_state(state)
    recommendation = select_sdlc(default_factors(current.requirements), current.requirements)
    audit(current, "sdlc_selection", f"Recommended {recommendation.selected_model}",
          evidence=recommendation.rationale)
    return {"sdlc_recommendation": recommendation.model_dump(mode="json")}
