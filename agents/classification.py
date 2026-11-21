from __future__ import annotations

import re
from typing import Any

from agents.common import as_state, audit
from config import DATABASE_PATH
from database.sqlite_manager import SQLiteManager
from schemas.models import ProjectState, RequirementItem

TAXONOMY = {
    "Business": ("business", "objective", "activation", "onboarding", "borrower"),
    "Stakeholder": ("stakeholder", "customer", "officer", "reviewer"),
    "Functional": ("system shall", "capture", "verify", "provide", "support", "activate", "disburse"),
    "Security": ("security", "encrypt", "mfa", "authentication", "rbac", "session", "threat"),
    "Privacy": ("privacy", "consent", "purpose", "data minimization", "erasure", "personal data"),
    "Regulatory": ("regulation", "compliance", "kyc", "v-cip", "retention", "pan", "ovd"),
    "Performance": ("ms", "latency", "sla", "response", "throughput", "fast"),
    "Availability & Reliability": ("availability", "recovery", "failure", "reconciliation", "resilience"),
    "Usability": ("user-friendly", "journey", "friction", "accessible"),
    "Data Management": ("data", "retain", "storage", "record", "video"),
    "Integration": ("api", "legacy", "core banking", "cbs", "nsdl", "uti"),
    "Audit & Reporting": ("audit", "log", "report", "siem", "evidence"),
    "Operational & Maintenance": ("operations", "monitor", "support", "incident", "deployment"),
}


def classify_requirements(requirements: list[RequirementItem]) -> list[RequirementItem]:
    for item in requirements:
        source = f"{item.statement} {item.source_quote}".lower()
        item.categories = [category for category, terms in TAXONOMY.items()
                           if any(term in source for term in terms)]
        if not item.categories:
            item.categories = ["Functional"]
        item.classification_rationale = "Labels selected from requirement evidence: " + ", ".join(item.categories)
        item.confidence_score = min(0.99, round(0.68 + 0.08 * len(item.categories), 2))
    return requirements


def classification(state: ProjectState | dict[str, Any]) -> dict[str, Any]:
    current = as_state(state)
    requirements = classify_requirements([RequirementItem.model_validate(item) for item in current.requirements])
    audit(current, "classification", "Applied 13-dimension multi-label taxonomy",
          evidence=f"{len(requirements)} requirements classified")
    SQLiteManager(DATABASE_PATH).save_requirements(current.project_id, requirements)
    return {"requirements": [item.model_dump(mode="json") for item in requirements]}
