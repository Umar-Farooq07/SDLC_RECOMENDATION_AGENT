"""LangGraph workflow with a durable SQLite checkpoint and offline fallback."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from agents.classification import classification
from agents.clarification import clarification
from agents.compliance import compliance
from agents.conflict_detection import conflict_detection
from agents.coordinator import coordinator
from agents.documentation import documentation
from agents.human_approval import human_approval
from agents.requirement_extraction import requirement_extraction
from agents.risk_analysis import risk_analysis
from agents.sdlc_selection import sdlc_selection
from agents.security_privacy import security_privacy
from agents.stakeholder_interaction import stakeholder_interaction
from agents.validation import validation
from config import DATABASE_PATH
from database.sqlite_manager import SQLiteManager
from schemas.models import ProjectState, RequirementItem

try:
    from langgraph.graph import END, START, StateGraph
    from langgraph.checkpoint.sqlite import SqliteSaver
except ImportError:
    END = START = StateGraph = SqliteSaver = None


def _merge_governance(state: ProjectState | dict[str, Any]) -> dict[str, Any]:
    current = state if isinstance(state, ProjectState) else ProjectState.model_validate(state)
    base = {item.req_id: item for item in
            [RequirementItem.model_validate(item) for item in current.requirements]}
    for raw in current.compliance_results:
        result = RequirementItem.model_validate(raw)
        if result.req_id in base:
            base[result.req_id].applicable_regulations = result.applicable_regulations
            base[result.req_id].compliance_gaps = result.compliance_gaps
            base[result.req_id].retention_or_reporting_obligation = result.retention_or_reporting_obligation
            base[result.req_id].requires_legal_signoff = result.requires_legal_signoff
    for raw in current.security_results:
        result = RequirementItem.model_validate(raw)
        if result.req_id in base:
            base[result.req_id].security_controls = result.security_controls
            base[result.req_id].assumptions = result.assumptions
    for raw in current.risk_results:
        result = RequirementItem.model_validate(raw)
        if result.req_id in base:
            base[result.req_id].likelihood = result.likelihood
            base[result.req_id].impact = result.impact
            base[result.req_id].risk_level = result.risk_level
            base[result.req_id].failure_consequences = result.failure_consequences
            base[result.req_id].mitigations = result.mitigations
    merged = list(base.values())
    manager = SQLiteManager(DATABASE_PATH)
    manager.save_requirements(current.project_id, merged)
    manager.save_traceability_links(current.project_id, merged)
    return {"requirements": [item.model_dump(mode="json") for item in merged]}


def _clarification_route(state: ProjectState | dict[str, Any]) -> str:
    current = state if isinstance(state, ProjectState) else ProjectState.model_validate(state)
    if current.has_ambiguities and current.interactive_mode and (
        current.clarification_round < current.max_clarification_rounds
    ):
        return "stakeholder_interaction"
    return "classification"


def create_workflow(database_path: str | Path = DATABASE_PATH) -> Any:
    if StateGraph is None:
        return _FallbackWorkflow()
    builder = StateGraph(ProjectState)
    for name, node in (
        ("coordinator", coordinator), ("stakeholder_interaction", stakeholder_interaction),
        ("requirement_extraction", requirement_extraction), ("clarification", clarification),
        ("classification", classification), ("conflict_detection", conflict_detection),
        ("compliance", compliance), ("security_privacy", security_privacy),
        ("risk_analysis", risk_analysis), ("merge_governance", _merge_governance),
        ("sdlc_selection", sdlc_selection), ("documentation", documentation),
        ("validation", validation), ("human_approval", human_approval),
    ):
        builder.add_node(name, node)
    builder.add_edge(START, "coordinator")
    builder.add_edge("coordinator", "stakeholder_interaction")
    builder.add_edge("stakeholder_interaction", "requirement_extraction")
    builder.add_edge("requirement_extraction", "clarification")
    builder.add_conditional_edges("clarification", _clarification_route, {
        "stakeholder_interaction": "stakeholder_interaction", "classification": "classification",
    })
    builder.add_edge("classification", "conflict_detection")
    builder.add_edge("conflict_detection", "compliance")
    builder.add_edge("conflict_detection", "security_privacy")
    builder.add_edge("conflict_detection", "risk_analysis")
    builder.add_edge(["compliance", "security_privacy", "risk_analysis"], "merge_governance")
    builder.add_edge("merge_governance", "sdlc_selection")
    builder.add_edge("sdlc_selection", "documentation")
    builder.add_edge("documentation", "validation")
    builder.add_edge("validation", "human_approval")
    builder.add_edge("human_approval", END)
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(path), check_same_thread=False)
    saver = SqliteSaver(connection)
    return builder.compile(checkpointer=saver, interrupt_before=["human_approval"])


class _FallbackWorkflow:
    """Runs the same stages deterministically when LangGraph is not installed."""
    is_checkpointed = False

    def invoke(self, input_state: dict[str, Any], config: dict[str, Any] | None = None) -> dict[str, Any]:
        state = ProjectState.model_validate(input_state)
        def apply(node: Any) -> None:
            nonlocal state
            state = ProjectState.model_validate({**state.model_dump(mode="python"), **node(state)})

        for node in (coordinator, stakeholder_interaction, requirement_extraction, clarification,
                     classification, conflict_detection):
            apply(node)
        for node, field in ((compliance, "compliance_results"),
                            (security_privacy, "security_results"), (risk_analysis, "risk_results")):
            apply(node)
        state = ProjectState.model_validate({**state.model_dump(mode="python"), **_merge_governance(state)})
        for node in (sdlc_selection, documentation, validation):
            apply(node)
        apply(human_approval)
        return state.model_dump(mode="json")

    def get_state(self, config: dict[str, Any]) -> Any:
        return None

    def update_state(self, config: dict[str, Any], values: dict[str, Any]) -> None:
        raise RuntimeError("HITL resume requires LangGraph and its SQLite checkpoint package.")


def run_pipeline(state: ProjectState | dict[str, Any], thread_id: str | None = None) -> dict[str, Any]:
    workflow = create_workflow()
    initial = state.model_dump(mode="json") if isinstance(state, ProjectState) else state
    return workflow.invoke(initial, config={"configurable": {"thread_id": thread_id or initial.get("project_id", "default")}})


def resume_pipeline(workflow: Any, thread_id: str, decision: str, reviewer: str = "",
                    comments: str = "") -> dict[str, Any]:
    config = {"configurable": {"thread_id": thread_id}}
    if isinstance(workflow, _FallbackWorkflow):
        raise RuntimeError("Cannot resume a checkpoint: install LangGraph and langgraph-checkpoint-sqlite.")
    workflow.update_state(config, {"human_decision": decision, "reviewer_identity": reviewer,
                                   "human_comments": comments})
    result = workflow.invoke(None, config=config)
    return result
