from pydantic import BaseModel, Field
from typing import List, Optional

class Requirement(BaseModel):
    req_id: str = Field(description="Unique ID, e.g., FR-001")
    statement: str = Field(description="The requirement description")
    category: str = Field(description="Category (e.g., Security, Functional, Compliance)")
    risk_level: str = Field(description="High, Medium, or Low")
    priority: str = Field(description="High, Medium, or Low")
    confidence_score: str = Field(description="Confidence percentage (e.g., 95%)")
    acceptance_criteria: List[str] = Field(description="List of conditions to accept this requirement")

class RequirementList(BaseModel):
    requirements: List[Requirement]

class QualityReport(BaseModel):
    ambiguity_detected: bool = Field(description="True if any requirements are vague or conflicting")
    missing_information: List[str] = Field(description="List of things the stakeholder forgot to mention")
    clarification_questions: List[str] = Field(description="Questions to ask the stakeholder to clarify requirements")

class UserStory(BaseModel):
    story_id: str = Field(description="Unique ID, e.g., US-001")
    as_a: str = Field(description="User role")
    i_want_to: str = Field(description="Goal or action")
    so_that: str = Field(description="Reason or benefit")

class DocumentationArtifacts(BaseModel):
    user_stories: List[UserStory]

class SDLCRecommendation(BaseModel):
    model_name: str = Field(description="Recommended SDLC model (e.g., Agile, V-Model)")
    confidence: str = Field(description="Confidence percentage")
    justification: str = Field(description="Why this model was chosen")
    development_plan: str = Field(description="A highly detailed, comprehensive step-by-step SDLC workflow plan tailored to this project. For each phase (e.g., Requirements, Design, Implementation, Testing, Deployment), specify the exact activities, responsible roles, deliverables, security controls, and compliance validation gates.")
