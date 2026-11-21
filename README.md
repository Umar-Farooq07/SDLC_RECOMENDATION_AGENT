# Financial Requirements Engineering & SDLC Platform

An evidence-oriented agentic requirements engineering workbench for Digital Customer Onboarding and Video KYC, with a secondary instant digital personal-loan scenario. It extracts traceable requirements from stakeholder material, highlights ambiguity and conflicts, retrieves policy/regulatory evidence, scores a project-specific SDLC model, and generates reviewable engineering artefacts.

## Architecture

- **Persistence:** SQLite stores projects, structured requirement/conflict records, stakeholder-to-requirement/regulation/control/test traceability links, approvals, and agent audit events. LangGraph checkpoints use `SqliteSaver` at the configured database path.
- **Workflow:** 13 specialized nodes run elicitation, extraction, clarification, classification, conflict detection, parallel compliance/security/risk analysis, SDLC selection, documentation, validation, and HITL approval.
- **Knowledge base:** Markdown sources in `kb_docs/` can be chunked into a local ChromaDB collection. When Chroma is unavailable or not yet initialized, the retriever uses the same local Markdown sources with deterministic lexical retrieval.
- **LLM providers:** Configure `LLM_PROVIDER` and the matching environment credential. The deterministic mock path runs without credentials; no stakeholder data is sent to a model unless an LLM integration is explicitly invoked by the deployment.
- **Privacy:** Uploaded and pasted content is passed directly to the processing pipeline; this application does not implement PII masking.

## Setup

Requires Python 3.11 or newer. From this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python -m rag.ingest_kb
streamlit run app.py
```

Set `OPENAI_API_KEY`, `GOOGLE_API_KEY`, or `ANTHROPIC_API_KEY` in the environment when using a configured provider. `LLM_PROVIDER=mock` is the offline default. Set `DATABASE_PATH`, `CHROMA_PATH`, `KB_PATH`, and `ARTIFACT_PATH` to relocate local data.

## Usage

1. Load the sample KYC case study or upload `.txt`, `.md`, or `.docx` source files.
2. Select stakeholder role and scenario; add live interview turns and run the workflow.
3. Review extracted evidence, ambiguity flags, cross-stakeholder conflicts, citations, controls, and risk ratings.
4. Review the ranked SDLC recommendation and phase/gate workflow.
5. Record named individual requirement/conflict/SDLC decisions or approve/reject/request regeneration at the approval gate. Final regulatory interpretations require accountable legal/compliance review.
6. Download Markdown or DOCX artefacts, including SRS, user stories, RTM, compliance matrix, risk register, SDLC plan, and open issues.

Generated `.md` and `.docx` files are also persisted under `artifacts/<project-id>/`.

The knowledge documents are illustrative seed material and must not be treated as authoritative legal advice. Verify current primary-source regulations and bank-specific policies before production use.

## Evaluation and tests

```bash
python -m eval.run_eval
pytest -q
```

Evaluation reports requirement extraction precision/recall/F1, ambiguity and conflict detection, citation grounding, coverage, SDLC top-1 agreement, and end-to-end timing.
