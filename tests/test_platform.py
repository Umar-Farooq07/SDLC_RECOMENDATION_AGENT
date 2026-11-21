from __future__ import annotations

from pathlib import Path

import pytest

from agents.clarification import clarify_requirements
from agents.conflict_detection import detect_conflicts
from agents.requirement_extraction import extract_requirements
from config import create_chat_model
from database.sqlite_manager import SQLiteManager
from exporters.artefact_exporter import docx_bytes
from graph.workflow import create_workflow
from rag.ingest_kb import ingest_documents
from rag.retriever import KnowledgeBaseRetriever
from schemas.models import ProjectState, RequirementItem
from sdlc_engine.selector import FACTORS, select_sdlc


ROOT = Path(__file__).resolve().parents[1]


def test_requirement_schema_and_extraction() -> None:
    extracted = extract_requirements(["[Product Owner] The system shall complete a fast liveness check."])
    assert extracted
    assert extracted[0].req_id.startswith("FR-KYC-")
    assert extracted[0].source_quote == "The system shall complete a fast liveness check."
    assert ProjectState(requirements=extracted)


def test_ambiguity_and_conflict_detection() -> None:
    samples = [
        path.read_text(encoding="utf-8") for path in sorted((ROOT / "sample_inputs").glob("*.txt"))
        if path.name != "loan_origination_case.txt"
    ]
    requirements = extract_requirements(samples)
    clarified, questions = clarify_requirements(requirements)
    assert questions
    assert any(item.needs_clarification for item in clarified)
    assert len(detect_conflicts(clarified)) == 3


def test_loan_case_detects_kfs_disbursal_conflict() -> None:
    sample = (ROOT / "sample_inputs" / "loan_origination_case.txt").read_text(encoding="utf-8")
    conflicts = detect_conflicts(extract_requirements([sample]))
    assert len(conflicts) == 1
    assert "KFS" in conflicts[0].description


def test_retriever_returns_citations(tmp_path: Path) -> None:
    count = ingest_documents(ROOT / "kb_docs", tmp_path / "chroma")
    assert count >= 5
    results = KnowledgeBaseRetriever(ROOT / "kb_docs", tmp_path / "chroma").retrieve("PAN OVD verification before account activation")
    assert results
    assert results[0].metadata["source"]
    assert results[0].text


def test_sdlc_mcda_rankings_and_workflow() -> None:
    result = select_sdlc()
    assert set(result.factors) == set(FACTORS)
    assert len(result.rankings) == 6
    assert result.rankings[0]["model"] == result.selected_model
    assert result.workflow


def test_docx_export() -> None:
    payload = docx_bytes("# Sample SRS\n\nA traceable requirement.", "Sample SRS")
    assert payload.startswith(b"PK")


def test_llm_mock_and_missing_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert create_chat_model("mock") is None
    assert create_chat_model("openai", "gpt-4o") is None


def test_workflow_smoke() -> None:
    from graph.workflow import run_pipeline
    state = ProjectState(raw_inputs=["[Product Owner] The system shall verify PAN before account activation."])
    result = run_pipeline(state)
    assert result["requirements"]
    assert result["sdlc_recommendation"]["selected_model"]
    assert result["artifacts"]["srs.md"]
    assert result["validation_report"]["checks"]


def test_sqlite_structured_requirement_persistence(tmp_path: Path) -> None:
    manager = SQLiteManager(tmp_path / "requirements.db")
    manager.save_project("project-a", "Test project", "Financial Services")
    requirement = RequirementItem(req_id="FR-KYC-001", statement="Verify PAN before activation.")
    manager.save_requirements("project-a", [requirement])
    manager.save_traceability_links("project-a", [requirement])
    assert manager.rows("requirements", "project-a")[0]["req_id"] == "FR-KYC-001"
    assert manager.rows("traceability_links", "project-a")[0]["target_type"] == "stakeholder_evidence"


def test_langgraph_human_approval_interrupt_and_resume(tmp_path: Path) -> None:
    workflow = create_workflow(tmp_path / "checkpoints.db")
    if not getattr(workflow, "is_checkpointed", True):
        pytest.skip("LangGraph checkpoint package is not installed")
    config = {"configurable": {"thread_id": "approval-test"}}
    state = ProjectState(raw_inputs=["[Product Owner] The system shall verify PAN before account activation."])
    result = workflow.invoke(state.model_dump(mode="json"), config=config)
    assert "human_approval" in workflow.get_state(config).next
    workflow.update_state(config, {
        "human_decision": "Approved", "reviewer_identity": "test-reviewer",
        "human_comments": "Reviewed test baseline",
    })
    resumed = workflow.invoke(None, config=config)
    assert resumed["pipeline_status"] == "completed"
    assert resumed["approvals"]
    assert all(item["status"] == "Approved" for item in resumed["approvals"])


def test_individual_requirement_edit_regenerates_artifacts(monkeypatch: pytest.MonkeyPatch) -> None:
    import agents.human_approval as approval_agent
    from agents.human_approval import human_approval

    monkeypatch.setattr(approval_agent, "persist_artifacts", lambda state, artifacts: [])
    state = ProjectState(
        project_id="individual-edit-test",
        requirements=[RequirementItem(req_id="FR-KYC-010", statement="Original statement",
                                      source_quote="Original stakeholder evidence",
                                      acceptance_criteria=["Verify the revised statement"])],
        approval_decisions={
            "requirement:FR-KYC-010": {
                "action": "Edit", "edited_text": "The system shall capture explicit consent.",
            },
        },
    )
    result = human_approval(state)
    assert result["requirements"][0]["statement"] == "The system shall capture explicit consent."
    assert "The system shall capture explicit consent." in result["artifacts"]["srs.md"]
    assert any(item["status"] == "Edited" for item in result["approvals"])
