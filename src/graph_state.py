from typing import TypedDict, Optional, List

class PipelineState(TypedDict):
    """
    The shared state object that flows through every node in the LangGraph.
    Each agent reads from and writes to this single state dict.
    """
    # Input
    raw_input: str                      # The original stakeholder text
    clarification_answers: Optional[str] # User answers to clarification questions

    # Agent Outputs
    requirements: Optional[dict]        # From ExtractionAgent
    quality: Optional[dict]             # From QualityAgent
    compliance: Optional[str]           # From ComplianceAgent
    artifacts: Optional[dict]           # From DocumentationAgent
    sdlc: Optional[dict]                # From SDLCAgent

    # Control flags
    needs_clarification: bool           # True if QualityAgent found ambiguity
