from __future__ import annotations

from typing import Any

from config import DATABASE_PATH
from database.sqlite_manager import SQLiteManager
from schemas.models import ProjectState


def as_state(state: ProjectState | dict[str, Any]) -> ProjectState:
    return state if isinstance(state, ProjectState) else ProjectState.model_validate(state)


def audit(state: ProjectState, agent: str, action: str, confidence: float = 0.9,
          evidence: str = "", details: dict[str, Any] | None = None) -> dict[str, Any]:
    manager = SQLiteManager(DATABASE_PATH)
    manager.save_project(state.project_id, state.project_name, state.domain)
    manager.log(
        state.project_id, agent, action, confidence, evidence, details
    )
    return {"agent": agent, "action": action, "confidence": confidence, "evidence": evidence}
