from __future__ import annotations

from typing import Any

from agents.common import as_state, audit
from config import DATABASE_PATH
from database.sqlite_manager import SQLiteManager
from exporters.artefact_exporter import build_artifacts, persist_artifacts
from schemas.models import (
    ApprovalItem, ConflictItem, ProjectState, RequirementItem, SDLCRecommendation, ValidationReport,
)
from agents.validation import validate_project


def human_approval(state: ProjectState | dict[str, Any]) -> dict[str, Any]:
    current = as_state(state)
    decision = current.human_decision or "Pending"
    requirements = [RequirementItem.model_validate(item) for item in current.requirements]
    conflicts = [ConflictItem.model_validate(item) for item in current.conflicts]
    recommendation = SDLCRecommendation.model_validate(current.sdlc_recommendation)
    targets = [
        *(("requirement", item.req_id) for item in requirements),
        *(("conflict", item.conflict_id) for item in conflicts if item.requires_human_resolution),
        *(("legal_signoff", item.req_id) for item in requirements if item.requires_legal_signoff),
        ("requirements_baseline", current.project_id),
        ("sdlc_selection", current.sdlc_recommendation.selected_model or "unselected"),
    ]
    manager = SQLiteManager(DATABASE_PATH)
    manager.save_project(current.project_id, current.project_name, current.domain)
    approvals: list[ApprovalItem] = []
    edited = False
    for approval_type, target in targets:
        key = f"{approval_type}:{target}"
        details = current.approval_decisions.get(key, {})
        action = details.get("action", decision)
        status = {
            "Approve": "Approved", "Edit": "Edited", "Reject": "Rejected",
            "Request Regeneration": "Regeneration Requested",
        }.get(action, action if action in {"Approved", "Edited", "Rejected"} else "Pending")
        edited_text = details.get("edited_text", "")
        if status == "Edited" and edited_text:
            if approval_type == "requirement":
                for requirement in requirements:
                    if requirement.req_id == target:
                        requirement.statement = edited_text
                        edited = True
            elif approval_type == "conflict":
                for conflict in conflicts:
                    if conflict.conflict_id == target:
                        conflict.suggested_resolution = edited_text
                        conflict.reviewer_decision = edited_text
                        edited = True
            elif approval_type == "sdlc_selection" and edited_text in {
                row["model"] for row in recommendation.rankings
            }:
                recommendation.selected_model = edited_text
                recommendation.rationale = f"Human reviewer selected {edited_text}."
                edited = True
        item = ApprovalItem(
            approval_type=approval_type, target_id=target, status=status,
            reviewer=details.get("reviewer", current.reviewer_identity),
            comments=details.get("comments", current.human_comments),
        )
        if edited_text:
            item.comments = f"{item.comments}\nEdited: {edited_text}".strip()
        approvals.append(item)
        manager.save_approval(current.project_id, approval_type, target, status,
                              item.reviewer, item.comments)
    updates: dict[str, Any] = {
        "approvals": [item.model_dump(mode="json") for item in approvals],
        "pipeline_status": "awaiting_approval" if decision == "Pending" else "completed",
    }
    if edited:
        manager.save_requirements(current.project_id, requirements)
        manager.save_conflicts(current.project_id, conflicts)
        manager.save_traceability_links(current.project_id, requirements)
        updates.update({
            "requirements": [item.model_dump(mode="json") for item in requirements],
            "conflicts": [item.model_dump(mode="json") for item in conflicts],
            "sdlc_recommendation": recommendation.model_dump(mode="json"),
        })
        edited_state = ProjectState.model_validate({**current.model_dump(mode="python"), **updates})
        updates["artifacts"] = build_artifacts(edited_state)
        updates["artifact_files"] = persist_artifacts(edited_state, updates["artifacts"])
        report_state = ProjectState.model_validate({
            **edited_state.model_dump(mode="python"), "artifacts": updates["artifacts"],
        })
        report = validate_project(report_state)
        updates["validation_report"] = report.model_dump(mode="json")
    audit(current, "human_approval", f"Approval gate status: {decision}",
          evidence=f"{len(targets)} approval decision(s) recorded",
          details={"decisions": [item.model_dump(mode="json") for item in approvals]})
    return updates
