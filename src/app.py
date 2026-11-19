import os
import sys
import streamlit as st
import docx
import PyPDF2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from src.agents.orchestrator import pipeline

load_dotenv()

st.set_page_config(page_title="Agentic Req System", page_icon="🤖", layout="wide")

st.title("🤖 Agentic AI Requirement & SDLC Pipeline")
st.markdown("Powered by **LangGraph** + Open-Source LLM (Mistral via Hugging Face)")

# ── Session state init ────────────────────────────────────────────────────────
if "pipeline_result" not in st.session_state:
    st.session_state.pipeline_result = None
if "waiting_for_clarification" not in st.session_state:
    st.session_state.waiting_for_clarification = False
if "raw_input" not in st.session_state:
    st.session_state.raw_input = ""

# ── File parser ───────────────────────────────────────────────────────────────
def extract_text_from_file(uploaded_file):
    text = ""
    try:
        if uploaded_file.name.endswith(".txt"):
            text = uploaded_file.getvalue().decode("utf-8")
        elif uploaded_file.name.endswith(".docx"):
            doc = docx.Document(uploaded_file)
            text = "\n".join([p.text for p in doc.paragraphs])
        elif uploaded_file.name.endswith(".pdf"):
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        st.error(f"Error reading file: {e}")
    return text

# ── Input Section ─────────────────────────────────────────────────────────────
st.subheader("1. Provide Stakeholder Inputs")
st.write("Upload documents (PDF, DOCX, TXT) and/or type notes below.")

uploaded_files = st.file_uploader(
    "Upload requirement documents", type=["txt", "pdf", "docx"], accept_multiple_files=True
)

default_input = """Project: Digital Wallet Update
Stakeholder: Risk & Product Teams

Notes:
We are upgrading our digital wallet. We need real-time payment processing (under 1 second). All user logins must require two-factor authentication using an authenticator app, SMS is no longer allowed. We need an extensive audit trail of every financial transaction to comply with the new Banking Authority regulations. The system must be highly available (99.99% uptime). Also, users need to be able to export their transaction history as a CSV file."""

user_input = st.text_area("Or paste Stakeholder Notes here:", value=default_input, height=150)

# ── Run button ────────────────────────────────────────────────────────────────
if st.button("▶ Run AI Pipeline", type="primary"):
    # Combine all inputs
    final_text = ""
    if uploaded_files:
        for f in uploaded_files:
            file_text = extract_text_from_file(f)
            st.info(f"Extracted {len(file_text)} characters from {f.name}")
            final_text += f"\n--- Source: {f.name} ---\n{file_text}\n\n"

    if user_input.strip() != default_input.strip() or not uploaded_files:
        final_text += f"\n--- Source: Manual Input ---\n{user_input}"

    if not final_text.strip():
        st.warning("Please provide some text or upload a document.")
    else:
        st.session_state.raw_input = final_text
        st.session_state.waiting_for_clarification = False
        st.session_state.pipeline_result = None

        with st.spinner("LangGraph pipeline running..."):
            initial_state = {
                "raw_input": final_text,
                "clarification_answers": None,
                "requirements": None,
                "quality": None,
                "compliance": None,
                "artifacts": None,
                "sdlc": None,
                "needs_clarification": False,
            }
            result = pipeline.invoke(initial_state)
            st.session_state.pipeline_result = result

            # If pipeline stopped for clarification
            if result.get("needs_clarification") and not result.get("sdlc"):
                st.session_state.waiting_for_clarification = True

# ── Clarification Section (loop) ──────────────────────────────────────────────
if st.session_state.waiting_for_clarification and st.session_state.pipeline_result:
    result = st.session_state.pipeline_result
    quality = result.get("quality", {})

    st.markdown("---")
    st.subheader("🔍 Quality Agent stopped the pipeline — Clarification Required")
    st.warning("The AI found ambiguities and missing information in the stakeholder input. Please answer the questions below so the pipeline can continue.")

    st.write("**Missing Information Detected:**")
    for item in quality.get("missing_information", []):
        st.write(f"- {item}")

    st.write("**Please answer these clarification questions:**")
    answers = []
    for i, question in enumerate(quality.get("clarification_questions", [])):
        answer = st.text_input(f"Q{i+1}: {question}", key=f"clarification_{i}")
        if answer:
            answers.append(f"Q: {question}\nA: {answer}")

    if st.button("✅ Submit Clarifications & Resume Pipeline", type="primary"):
        if not answers:
            st.warning("Please answer at least one question before continuing.")
        else:
            combined_answers = "\n\n".join(answers)
            with st.spinner("Resuming pipeline with your clarifications..."):
                updated_state = {
                    **result,
                    "clarification_answers": combined_answers,
                    "needs_clarification": False,
                }
                final_result = pipeline.invoke(updated_state)
                st.session_state.pipeline_result = final_result
                st.session_state.waiting_for_clarification = False
                st.rerun()

# ── Results Section ───────────────────────────────────────────────────────────
result = st.session_state.pipeline_result
if result and result.get("sdlc"):
    st.markdown("---")
    st.success("✅ Pipeline Completed Successfully!")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📋 1. Extracted Requirements")
        reqs = result.get("requirements", {}).get("requirements", [])
        for req in reqs:
            with st.expander(f"{req.get('req_id')} — {req.get('category')}", expanded=True):
                st.write(f"**Priority:** {req.get('priority')} | **Risk:** {req.get('risk_level')} | **Confidence:** {req.get('confidence_score')}")
                st.write(f"**Statement:** {req.get('statement')}")
                st.write("**Acceptance Criteria:**")
                for c in req.get("acceptance_criteria", []):
                    st.write(f"  - {c}")

        st.subheader("🛡️ 2. Compliance Report")
        st.info(result.get("compliance", "No compliance report generated."))

    with col2:
        st.subheader("🔍 3. Quality Analysis")
        quality = result.get("quality", {})
        if quality.get("ambiguity_detected"):
            st.warning("⚠️ Ambiguities were detected but resolved via clarification.")
            for item in quality.get("missing_information", []):
                st.write(f"- {item}")
        else:
            st.success("✅ Requirements are clear and unambiguous.")

        st.subheader("📝 4. User Stories")
        stories = result.get("artifacts", {}).get("user_stories", [])
        for s in stories:
            st.markdown(f"**{s.get('story_id')}**: As a **{s.get('as_a')}**, I want to **{s.get('i_want_to')}**, so that **{s.get('so_that')}**.")

        st.subheader("⚙️ 5. SDLC Recommendation")
        sdlc = result.get("sdlc", {})
        if isinstance(sdlc, dict):
            st.success(f"**Model:** {sdlc.get('model_name')} — Confidence: {sdlc.get('confidence')}")
            st.write(f"**Justification:** {sdlc.get('justification')}")
            with st.expander("📄 View Full Development Plan"):
                st.info(sdlc.get("development_plan", "No plan generated."))

    st.markdown("---")
    st.subheader("🧑‍⚖️ 6. Human-in-the-Loop Validation (Required)")
    st.write("AI-generated plans must be reviewed and approved by an authorized stakeholder before execution.")
    approval = st.radio(
        "Do you approve this Requirement & SDLC Baseline?",
        ("Pending", "Approve ✅", "Reject & Request Clarification ❌")
    )
    if approval == "Approve ✅":
        st.success("🎉 Baseline Approved! The project is ready to move to the Architecture phase.")
    elif approval == "Reject & Request Clarification ❌":
        st.error("❌ Baseline Rejected. Please update the stakeholder notes and re-run the pipeline.")
