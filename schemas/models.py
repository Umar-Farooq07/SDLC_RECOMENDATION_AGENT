"""Typed data contracts shared by agents, storage, and the UI."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from config import LLM_MODEL, LLM_PROVIDER


class Citation(BaseModel):
    document_title: str
    section: str = "Unspecified"
    jurisdiction: str = "India"
    version: str = "2025"
    effective_date: str = "2025-01-01"
    supporting_evidence: str
    source_id: str = ""


class RequirementItem(BaseModel):
    req_id: str
    statement: str
    source_stakeholder: str = "Unknown"
    source_quote: str = ""
    business_justification: str = ""
    priority: Literal["High", "Medium", "Low"] = "Medium"
    dependencies: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)
    needs_clarification: bool = False
    clarification_questions: list[str] = Field(default_factory=list)
    categories: list[str] = Field(default_factory=list)
    classification_rationale: str = ""
    confidence_score: float = Field(default=0.75, ge=0, le=1)
    applicable_regulations: list[Citation] = Field(default_factory=list)
    compliance_gaps: list[str] = Field(default_factory=list)
    retention_or_reporting_obligation: str = ""
    requires_legal_signoff: bool = False
    security_controls: list[str] = Field(default_factory=list)
    likelihood: int = Field(default=3, ge=1, le=5)
    impact: int = Field(default=3, ge=1, le=5)
    risk_level: Literal["Critical", "High", "Medium", "Low"] = "Medium"
    failure_consequences: list[str] = Field(default_factory=list)
    mitigations: list[str] = Field(default_factory=list)
    test_case_ids: list[str] = Field(default_factory=list)


class ConflictItem(BaseModel):
    conflict_id: str
    req_id_a: str
    req_id_b: str
    conflict_type: Literal["Contradiction", "SLA mismatch", "Duplicate", "Policy conflict"] = "Contradiction"
    description: str
    severity: Literal["Critical", "High", "Medium", "Low"] = "High"
    suggested_resolution: str = ""
    requires_human_resolution: bool = True
    reviewer_decision: str = ""


class ApprovalItem(BaseModel):
    approval_type: str
    target_id: str
    status: Literal["Pending", "Approved", "Edited", "Rejected", "Regeneration Requested"] = "Pending"
    reviewer: str = ""
    comments: str = ""
    decision_at: str = ""


class SDLCRecommendation(BaseModel):
    factors: dict[str, int] = Field(default_factory=dict)
    rankings: list[dict[str, Any]] = Field(default_factory=list)
    selected_model: str = ""
    workflow: list[dict[str, Any]] = Field(default_factory=list)
    rationale: str = ""


class ValidationReport(BaseModel):
    passed: bool = False
    checks: dict[str, bool] = Field(default_factory=dict)
    quality_score: float = Field(default=0, ge=0, le=1)
    issues: list[str] = Field(default_factory=list)


class ProjectState(BaseModel):
    project_id: str = "kyc-onboarding"
    project_name: str = "Digital Customer Onboarding & Video KYC"
    domain: str = "Financial Services"
    scenario: str = "onboarding"
    active_stakeholder_role: str = "Product Owner"
    llm_provider: str = LLM_PROVIDER
    llm_model: str = LLM_MODEL
    interactive_mode: bool = False
    raw_inputs: list[str] = Field(default_factory=list)
    conversation_turns: list[dict[str, str]] = Field(default_factory=list)
    requirements: list[RequirementItem] = Field(default_factory=list)
    compliance_results: list[dict[str, Any]] = Field(default_factory=list)
    security_results: list[dict[str, Any]] = Field(default_factory=list)
    risk_results: list[dict[str, Any]] = Field(default_factory=list)
    conflicts: list[ConflictItem] = Field(default_factory=list)
    clarification_round: int = 0
    max_clarification_rounds: int = 2
    has_ambiguities: bool = False
    follow_up_questions: list[str] = Field(default_factory=list)
    sdlc_recommendation: SDLCRecommendation = Field(default_factory=SDLCRecommendation)
    validation_report: ValidationReport = Field(default_factory=ValidationReport)
    artifacts: dict[str, str] = Field(default_factory=dict)
    artifact_files: list[str] = Field(default_factory=list)
    audit_events: list[dict[str, Any]] = Field(default_factory=list)
    approvals: list[ApprovalItem] = Field(default_factory=list)
    approval_decisions: dict[str, dict[str, str]] = Field(default_factory=dict)
    reviewer_identity: str = ""
    human_decision: str = ""
    human_comments: str = ""
    pipeline_status: str = "new"
