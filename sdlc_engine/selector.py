"""Deterministic SDLC decision rules and weighted MCDA ranking."""
from __future__ import annotations

from typing import Any

from config import MCDA_WEIGHTS
from schemas.models import SDLCRecommendation

FACTORS = [
    "requirement_stability", "regulatory_criticality", "security_risk", "project_complexity",
    "system_size", "legacy_dependence", "change_frequency", "continuous_delivery_need",
    "stakeholder_availability", "testing_rigor", "budget_schedule_constraint",
    "formal_verification_need", "failure_consequence",
]
MODELS = [
    "Agile–DevSecOps Hybrid", "Agile–V-Model Hybrid", "V-Model", "Spiral",
    "Agile Scrum", "Waterfall",
]


def default_factors(requirements: list[Any]) -> dict[str, int]:
    scores = {name: 3 for name in FACTORS}
    if requirements:
        scores.update({
            "regulatory_criticality": 5, "security_risk": 4, "legacy_dependence": 4,
            "testing_rigor": 5, "formal_verification_need": 4, "failure_consequence": 5,
            "change_frequency": 4, "continuous_delivery_need": 4,
            "requirement_stability": 2, "stakeholder_availability": 3,
        })
    return scores


def _model_score(model: str, factors: dict[str, int]) -> float:
    profiles = {
        "Agile–DevSecOps Hybrid": [2, 5, 5, 4, 3, 4, 5, 5, 4, 5, 3, 4, 5],
        "Agile–V-Model Hybrid": [3, 5, 4, 4, 3, 4, 4, 3, 4, 5, 3, 5, 5],
        "V-Model": [5, 5, 5, 3, 3, 4, 2, 2, 3, 5, 3, 5, 5],
        "Spiral": [3, 4, 5, 5, 4, 4, 4, 3, 3, 4, 2, 4, 5],
        "Agile Scrum": [2, 2, 2, 3, 2, 2, 5, 5, 5, 3, 4, 2, 2],
        "Waterfall": [5, 4, 3, 2, 2, 3, 1, 1, 2, 4, 3, 4, 4],
    }
    weight_total = sum(MCDA_WEIGHTS.values())
    score = 0.0
    for factor, target in zip(FACTORS, profiles[model]):
        weight = MCDA_WEIGHTS.get(factor, 0.0)
        fit = 1.0 - abs(factors[factor] - target) / 4.0
        score += weight * fit
    return max(0.0, min(100.0, score / weight_total * 100))


def select_sdlc(factors: dict[str, int] | None = None,
                requirements: list[Any] | None = None) -> SDLCRecommendation:
    factors = default_factors(requirements or []) if factors is None else {
        key: max(1, min(5, int(factors.get(key, 3)))) for key in FACTORS
    }
    raw_scores = {model: _model_score(model, factors) for model in MODELS}
    if factors["regulatory_criticality"] >= 4 and factors["security_risk"] >= 4:
        raw_scores["Agile–DevSecOps Hybrid"] = min(100.0, raw_scores["Agile–DevSecOps Hybrid"] + 5.0)
    elif factors["formal_verification_need"] >= 4 or factors["testing_rigor"] >= 5:
        raw_scores["Agile–V-Model Hybrid"] = min(100.0, raw_scores["Agile–V-Model Hybrid"] + 5.0)
    selected = max(raw_scores, key=raw_scores.get)
    rankings = sorted(
        [{"model": model, "score": round(value, 1)} for model, value in raw_scores.items()],
        key=lambda item: item["score"], reverse=True,
    )
    phases = [
        ("Discovery & Governance", "Baseline scope, identify stakeholders and regulatory obligations", "Product Owner, Compliance"),
        ("Architecture & Threat Modeling", "Define target architecture, threat model, privacy and security controls", "Architect, InfoSec"),
        ("Iterative Delivery", "Deliver prioritized onboarding increments with CI/CD and peer review", "Engineering, Product"),
        ("Verification & Compliance", "Run functional, integration, SAST/DAST, performance and audit evidence checks", "QA, InfoSec, Compliance"),
        ("Controlled Release", "Complete UAT, operational readiness, approval and staged rollout", "Operations, Business Owner"),
        ("Operate & Improve", "Monitor SIEM, SLAs, incidents, regulatory changes and backlog", "Operations, Compliance"),
    ]
    workflow = [
        {"phase": phase, "activities": activities, "responsible_roles": roles,
         "deliverables": "Reviewed evidence, traceable requirements and test results",
         "security_controls": "Threat modeling, MFA/RBAC, SAST/DAST, encrypted audit logs",
         "testing_requirements": "Functional, integration, security, resilience, performance, and regression evidence",
         "compliance_checkpoints": "Trace obligations to evidence; obtain compliance/legal review at required gates",
         "entry_criteria": "Approved prior-phase outputs and open risks reviewed",
         "exit_criteria": "Evidence complete; no unresolved critical defects; human gate approved",
         "human_approval_gate": index in (0, 3, 4)}
        for index, (phase, activities, roles) in enumerate(phases)
    ]
    return SDLCRecommendation(
        factors=factors, rankings=rankings, selected_model=selected, workflow=workflow,
        rationale=f"{selected} is selected because the project combines high regulatory and security "
                   "criticality with legacy integration and a need for iterative delivery.",
    )
