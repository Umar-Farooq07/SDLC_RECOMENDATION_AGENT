"""Streamlit dashboard for the financial requirements engineering workflow."""
from __future__ import annotations

from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent


def _read_upload(upload: Any) -> str:
    if upload.name.lower().endswith(".docx"):
        from docx import Document
        document = Document(upload)
        return "\n".join(paragraph.text for paragraph in document.paragraphs)
    return upload.getvalue().decode("utf-8", errors="replace")


def main() -> None:
    try:
        import streamlit as st
    except ImportError as exc:
        raise RuntimeError("The dashboard requires Streamlit. Install requirements.txt first.") from exc

    from config import DATABASE_PATH, LLM_MODEL, LLM_PROVIDER
    from config import create_chat_model
    from database.sqlite_manager import SQLiteManager
    from exporters.artefact_exporter import docx_bytes
    from graph.workflow import create_workflow
    from rag.ingest_kb import ingest_documents
    from schemas.models import ProjectState
    from agents.stakeholder_interaction import get_interview_questions

    st.set_page_config(page_title="FinReq Agentic Platform", page_icon="🏦", layout="wide")
    st.title("Financial Requirements Engineering & SDLC Platform")
    st.caption("Digital Customer Onboarding & Video KYC • Evidence-grounded • Human-approved")
    with st.sidebar:
        st.header("Project setup")
        project_id = st.text_input("Project ID", "kyc-onboarding")
        project_name = st.text_input("Project name", "Digital Customer Onboarding & Video KYC")
        scenario = st.selectbox("Evaluation scenario", ["onboarding", "instant_digital_personal_loan"])
        role = st.selectbox("Stakeholder role", [
            "Product Owner", "Compliance Officer", "InfoSec Architect", "Software Architect", "Operations Lead",
        ])
        providers = ["mock", "openai", "google", "anthropic"]
        provider_default = LLM_PROVIDER if LLM_PROVIDER in providers else "mock"
        provider = st.selectbox("LLM provider", providers, index=providers.index(provider_default))
        model_default = {"openai": "gpt-4o", "google": "gemini-2.5-pro",
                         "anthropic": "claude-3-7-sonnet-latest", "mock": LLM_MODEL}
        model = st.text_input("Model", LLM_MODEL if provider == provider_default else model_default[provider])
        st.caption("Provider credentials are read from environment variables. Mock mode is deterministic.")
        if st.button("Ingest knowledge base", use_container_width=True):
            try:
                count = ingest_documents()
                st.success(f"Indexed {count} knowledge chunks.")
            except Exception as exc:
                st.error(f"Knowledge-base ingestion failed: {exc}")

    if "raw_inputs" not in st.session_state:
        st.session_state.raw_inputs = []
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    if "pipeline_result" not in st.session_state:
        st.session_state.pipeline_result = None
    if "workflow" not in st.session_state:
        st.session_state.workflow = None
    if "pipeline_thread" not in st.session_state:
        st.session_state.pipeline_thread = project_id
    if "approval_decisions" not in st.session_state:
        st.session_state.approval_decisions = {}

    tabs = st.tabs([
        "Elicitation & Upload", "Requirements & Conflicts", "Compliance, Security & Risk",
        "SDLC Recommendation", "Human Approval", "Artefacts & Audit",
    ])
    with tabs[0]:
        st.subheader("Adaptive stakeholder elicitation")
        st.write(f"Interview prompts for **{role}**")
        question_col, _ = st.columns([1, 3])
        with question_col:
            generate_questions = st.button("Generate adaptive questions")
        questions = get_interview_questions(role)
        if generate_questions:
            try:
                chat_model = create_chat_model(provider, model)
                if chat_model is None:
                    st.info("No provider credential is configured; showing deterministic interview prompts.")
                else:
                    response = chat_model.invoke(
                        "Generate at most 5 concise follow-up questions for a financial-sector requirements "
                        "interview. Return one per line. Cover measurable acceptance criteria, exceptions, "
                        "data, security, service levels, and dependencies.\n"
                        f"Role: {role}\nEvidence:\n{chr(10).join(st.session_state.raw_inputs)[-6000:]}"
                    )
                    if isinstance(response.content, str):
                        generated = [line.strip("- •\t ") for line in response.content.splitlines() if line.strip()]
                        if generated:
                            questions = generated[:5]
            except Exception as exc:
                st.error(f"Could not generate adaptive interview questions: {exc}")
        for question in questions:
            st.markdown(f"- {question}")
        uploaded = st.file_uploader("Upload transcripts or policy documents", type=["txt", "md", "docx"],
                                    accept_multiple_files=True)
        if st.button("Load Sample KYC Case Study", type="secondary"):
            if scenario == "instant_digital_personal_loan":
                st.session_state.raw_inputs = [
                    (ROOT / "sample_inputs" / "loan_origination_case.txt").read_text(encoding="utf-8")
                ]
                st.success("Loaded the instant digital personal-loan case study.")
            else:
                st.session_state.raw_inputs = [
                    path.read_text(encoding="utf-8")
                    for path in sorted((ROOT / "sample_inputs").glob("*.txt"))
                    if path.name != "loan_origination_case.txt"
                ]
                st.success("Loaded Product Owner, Compliance Officer, and InfoSec/Architecture samples.")
        if uploaded:
            for file in uploaded:
                content = _read_upload(file)
                if content and content not in st.session_state.raw_inputs:
                    st.session_state.raw_inputs.append(content)
        with st.form("stakeholder_chat", clear_on_submit=True):
            message = st.text_area("Conversation turn", placeholder="Add stakeholder evidence or an answer to a clarification question")
            submitted = st.form_submit_button("Add interview turn")
        if submitted and message.strip():
            st.session_state.conversation.append({"role": role, "content": message.strip()})
            st.session_state.raw_inputs.append(f"[{role}] {message.strip()}")
        for turn in st.session_state.conversation:
            st.chat_message("user").write(f"**{turn['role']}:** {turn['content']}")
        st.caption(f"{len(st.session_state.raw_inputs)} source document(s)/turn(s) ready.")
        if st.button("Run requirements pipeline", type="primary", disabled=not st.session_state.raw_inputs):
            state = ProjectState(
                project_id=project_id, project_name=project_name, scenario=scenario,
                active_stakeholder_role=role, llm_provider=provider, llm_model=model,
                raw_inputs=st.session_state.raw_inputs,
                conversation_turns=st.session_state.conversation, interactive_mode=False,
                approval_decisions=st.session_state.approval_decisions,
            )
            st.session_state.pipeline_thread = project_id
            st.session_state.workflow = create_workflow(DATABASE_PATH)
            with st.spinner("Running requirements, governance, and SDLC agents..."):
                try:
                    st.session_state.pipeline_result = st.session_state.workflow.invoke(
                        state.model_dump(mode="json"),
                        config={"configurable": {"thread_id": project_id}},
                    )
                    st.success("Pipeline stages completed. Review the approval queue before baselining.")
                except Exception as exc:
                    st.error(f"Pipeline execution failed: {exc}")

    result = st.session_state.pipeline_result
    if result:
        with tabs[1]:
            requirements = result.get("requirements", [])
            st.subheader(f"Requirements ({len(requirements)})")
            priorities = st.multiselect("Filter by priority", ["High", "Medium", "Low"],
                                        default=["High", "Medium", "Low"])
            visible = [item for item in requirements if item.get("priority") in priorities]
            st.dataframe([{
                "ID": item["req_id"], "Statement": item["statement"], "Stakeholder": item["source_stakeholder"],
                "Priority": item["priority"], "Categories": ", ".join(item.get("categories", [])),
                "Confidence": item.get("confidence_score"), "Risk": item.get("risk_level"),
                "Clarification": item.get("needs_clarification", False),
            } for item in visible], use_container_width=True, hide_index=True)
            st.subheader(f"Cross-stakeholder conflicts ({len(result.get('conflicts', []))})")
            for conflict in result.get("conflicts", []):
                with st.container(border=True):
                    st.markdown(f"**{conflict['severity']} · {conflict['conflict_type']} · {conflict['conflict_id']}**")
                    st.write(conflict["description"])
                    st.caption(f"Suggested resolution: {conflict['suggested_resolution']}")

        with tabs[2]:
            for item in requirements:
                with st.expander(f"{item['req_id']} · {item['risk_level']} risk"):
                    st.write(item["statement"])
                    st.markdown("**Retrieved regulatory/policy citations**")
                    for citation in item.get("applicable_regulations", []):
                        st.markdown(f"- **{citation['document_title']} — {citation['section']}** "
                                    f"({citation['jurisdiction']}, {citation['version']})")
                        st.info(citation["supporting_evidence"])
                    if item.get("compliance_gaps"):
                        st.warning("Gaps: " + "; ".join(item["compliance_gaps"]))
                    st.markdown("**Security & privacy controls**")
                    st.write(", ".join(item.get("security_controls", [])))
                    st.markdown(f"**Likelihood / Impact:** {item['likelihood']} / {item['impact']}")
                    st.write("Mitigations: " + "; ".join(item.get("mitigations", [])))

        with tabs[3]:
            recommendation = result.get("sdlc_recommendation", {})
            st.subheader(f"Recommended: {recommendation.get('selected_model', 'Pending')}")
            st.write(recommendation.get("rationale", ""))
            st.bar_chart({entry["model"]: entry["score"] for entry in recommendation.get("rankings", [])})
            st.markdown("**Project decision factors (1–5)**")
            st.dataframe([{"Factor": key.replace("_", " ").title(), "Score": value}
                          for key, value in recommendation.get("factors", {}).items()],
                         use_container_width=True, hide_index=True)
            st.markdown("**Custom phases and gates**")
            st.dataframe(recommendation.get("workflow", []), use_container_width=True, hide_index=True)

        with tabs[4]:
            st.subheader("Human-in-the-loop approval queue")
            report = result.get("validation_report", {})
            st.metric("Validation quality", f"{report.get('quality_score', 0):.0%}",
                      "Passed" if report.get("passed") else "Review needed")
            if report.get("issues"):
                st.warning("Validation issues: " + ", ".join(report["issues"]))
            conflicts = result.get("conflicts", [])
            for item in conflicts:
                st.markdown(f"- **{item['conflict_id']} ({item['severity']})** — {item['description']}")
            st.markdown("**Individual review decision**")
            review_targets = [
                (f"requirement:{item['req_id']}", f"Requirement · {item['req_id']}")
                for item in result.get("requirements", [])
            ]
            review_targets.extend(
                (f"conflict:{item['conflict_id']}", f"Conflict · {item['conflict_id']}")
                for item in conflicts
            )
            review_targets.extend(
                (f"legal_signoff:{item['req_id']}", f"Legal sign-off · {item['req_id']}")
                for item in result.get("requirements", []) if item.get("requires_legal_signoff")
            )
            review_targets.extend([
                (f"requirements_baseline:{project_id}", "Final requirements baseline"),
                (f"sdlc_selection:{result.get('sdlc_recommendation', {}).get('selected_model', 'unselected')}",
                 "SDLC model selection"),
            ])
            target_key = st.selectbox("Review target", [key for key, _ in review_targets],
                                      format_func=lambda key: dict(review_targets)[key])
            action = st.selectbox("Decision", ["Approve", "Edit", "Reject", "Request Regeneration"])
            edited_text = ""
            if action == "Edit":
                kind, identifier = target_key.split(":", 1)
                if kind == "requirement":
                    original = next(item["statement"] for item in result["requirements"]
                                    if item["req_id"] == identifier)
                    edited_text = st.text_area("Revised requirement", value=original)
                elif kind == "conflict":
                    original = next(item["suggested_resolution"] for item in conflicts
                                    if item["conflict_id"] == identifier)
                    edited_text = st.text_area("Revised conflict resolution", value=original)
                else:
                    options = [item["model"] for item in result.get("sdlc_recommendation", {}).get("rankings", [])]
                    edited_text = st.selectbox("Selected SDLC model", options)
            individual_comments = st.text_area("Decision comments", key="individual_comments")
            individual_submit = st.button("Submit individual decision")
            reviewer = st.text_input("Reviewer identity", key="reviewer")
            decision = st.text_area("Reviewer comments")
            col1, col2, col3 = st.columns(3)
            with col1:
                approve = st.button("Approve baseline", type="primary")
            with col2:
                reject = st.button("Reject")
            with col3:
                request_changes = st.button("Request changes")
            selected = ("Approved" if approve else "Rejected" if reject else
                        "Request Regeneration" if request_changes else "")
            if selected or individual_submit:
                workflow = st.session_state.workflow
                if workflow is None:
                    st.error("No resumable workflow checkpoint is available.")
                else:
                    try:
                        if individual_submit:
                            st.session_state.approval_decisions[target_key] = {
                                "action": action, "edited_text": edited_text,
                                "reviewer": reviewer, "comments": individual_comments,
                            }
                        if getattr(workflow, "is_checkpointed", True):
                            config = {"configurable": {"thread_id": st.session_state.pipeline_thread}}
                            snapshot = workflow.get_state(config)
                            if snapshot and snapshot.next:
                                workflow.update_state(config, {
                                    "human_decision": selected or "Pending", "reviewer_identity": reviewer,
                                    "human_comments": decision,
                                    "approval_decisions": st.session_state.approval_decisions,
                                })
                                updated = workflow.invoke(None, config=config)
                            else:
                                resumed_state = ProjectState(
                                    project_id=project_id, project_name=project_name, scenario=scenario,
                                    active_stakeholder_role=role, llm_provider=provider, llm_model=model,
                                    raw_inputs=st.session_state.raw_inputs,
                                    conversation_turns=st.session_state.conversation,
                                    human_decision=selected or "Pending", reviewer_identity=reviewer,
                                    human_comments=decision,
                                    approval_decisions=st.session_state.approval_decisions,
                                )
                                updated = workflow.invoke(resumed_state.model_dump(mode="json"), config=config)
                        else:
                            resumed_state = ProjectState(
                                project_id=project_id, project_name=project_name, scenario=scenario,
                                active_stakeholder_role=role, llm_provider=provider, llm_model=model,
                                raw_inputs=st.session_state.raw_inputs,
                                conversation_turns=st.session_state.conversation,
                                human_decision=selected or "Pending", reviewer_identity=reviewer,
                                human_comments=decision,
                                approval_decisions=st.session_state.approval_decisions,
                            )
                            updated = workflow.invoke(resumed_state.model_dump(mode="json"))
                        st.session_state.pipeline_result = updated
                        st.success(f"Recorded {(selected or action).lower()} decision.")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Could not resume approval checkpoint: {exc}")
            st.caption("Approval is recorded to the SQLite audit trail; legal sign-off remains an accountable human decision.")

        with tabs[5]:
            st.subheader("Generated engineering artefacts")
            artifacts = result.get("artifacts", {})
            names = list(artifacts)
            if names:
                selected_artifact = st.selectbox("Artefact", names)
                content = artifacts[selected_artifact]
                if result.get("artifact_files"):
                    st.caption("Persisted files: " + ", ".join(result["artifact_files"]))
                st.markdown(content)
                st.download_button("Download Markdown", content, file_name=selected_artifact, mime="text/markdown")
                st.download_button("Download DOCX", docx_bytes(content, selected_artifact),
                                   file_name=selected_artifact.replace(".md", ".docx"),
                                   mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            st.subheader("SQLite agent audit trail")
            try:
                logs = SQLiteManager(DATABASE_PATH).rows("audit_logs", project_id)
                st.dataframe(logs, use_container_width=True, hide_index=True)
            except Exception as exc:
                st.error(f"Could not load audit trail: {exc}")
    else:
        with tabs[1]:
            st.info("Run the pipeline to explore extracted requirements and conflicts.")
        with tabs[2]:
            st.info("Compliance, security, and risk mappings appear after pipeline execution.")
        with tabs[3]:
            st.info("The project-specific SDLC recommendation appears after pipeline execution.")
        with tabs[4]:
            st.info("The HITL queue opens after validation.")
        with tabs[5]:
            st.info("Generated artefacts and audit events appear after pipeline execution.")


if __name__ == "__main__":
    main()
