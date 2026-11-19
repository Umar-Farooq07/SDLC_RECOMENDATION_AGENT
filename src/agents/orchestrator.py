from langgraph.graph import StateGraph, END
from src.graph_state import PipelineState
from src.agents.extraction_agent import ExtractionAgent
from src.agents.quality_agent import QualityAgent
from src.agents.compliance_agent import ComplianceAgent
from src.agents.documentation_agent import DocumentationAgent
from src.agents.sdlc_agent import SDLCAgent

# Instantiate all agents
extractor = ExtractionAgent()
quality_checker = QualityAgent()
compliance_checker = ComplianceAgent()
documenter = DocumentationAgent()
sdlc_recommender = SDLCAgent()

# ── Node functions ────────────────────────────────────────────────────────────

def extraction_node(state: PipelineState) -> PipelineState:
    """
    Node 1: Merge the original input with any clarification answers
    provided by the user, then extract structured requirements.
    """
    combined_input = state["raw_input"]
    if state.get("clarification_answers"):
        combined_input += f"\n\n--- Stakeholder Clarifications ---\n{state['clarification_answers']}"
    reqs = extractor.extract_requirements(combined_input)
    return {**state, "requirements": reqs}


def quality_node(state: PipelineState) -> PipelineState:
    """
    Node 2: Check extracted requirements for ambiguity, incompleteness, or conflicts.
    Sets 'needs_clarification' flag to True if issues are found.
    """
    quality = quality_checker.analyze_quality(state["requirements"])
    needs = quality.get("ambiguity_detected", False)
    return {**state, "quality": quality, "needs_clarification": needs}


def compliance_node(state: PipelineState) -> PipelineState:
    """Node 3: Check requirements against financial regulations."""
    report = compliance_checker.check_compliance(state["requirements"])
    return {**state, "compliance": report}


def documentation_node(state: PipelineState) -> PipelineState:
    """Node 4: Generate Agile User Stories from the requirements."""
    artifacts = documenter.generate_artifacts(state["requirements"])
    return {**state, "artifacts": artifacts}


def sdlc_node(state: PipelineState) -> PipelineState:
    """Node 5: Recommend SDLC model and generate the detailed development plan."""
    rec = sdlc_recommender.recommend_sdlc(state["requirements"])
    return {**state, "sdlc": rec}


# ── Conditional edge (the clarification loop) ─────────────────────────────────

def should_clarify(state: PipelineState) -> str:
    """
    Router: After Quality check, decide what to do next.
    - If ambiguity is found AND no clarification answers exist yet → pause (WAIT_FOR_HUMAN).
    - Otherwise → continue the pipeline to Compliance.
    """
    if state["needs_clarification"] and not state.get("clarification_answers"):
        return "WAIT_FOR_HUMAN"
    return "CONTINUE"


# ── Build the LangGraph ───────────────────────────────────────────────────────

def build_graph():
    graph = StateGraph(PipelineState)

    # Register all nodes
    graph.add_node("extract",      extraction_node)
    graph.add_node("quality",      quality_node)
    graph.add_node("compliance",   compliance_node)
    graph.add_node("documentation", documentation_node)
    graph.add_node("sdlc",         sdlc_node)

    # Define the flow: start → extract → quality
    graph.set_entry_point("extract")
    graph.add_edge("extract", "quality")

    # Conditional fork after quality check
    graph.add_conditional_edges(
        "quality",
        should_clarify,
        {
            "WAIT_FOR_HUMAN": END,      # Stop here, show questions to user
            "CONTINUE":       "compliance"  # Proceed with pipeline
        }
    )

    # Linear path after compliance check
    graph.add_edge("compliance",   "documentation")
    graph.add_edge("documentation", "sdlc")
    graph.add_edge("sdlc",         END)

    return graph.compile()

# Single compiled graph instance
pipeline = build_graph()
