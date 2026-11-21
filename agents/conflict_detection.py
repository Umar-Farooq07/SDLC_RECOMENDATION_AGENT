from __future__ import annotations

import re
from typing import Any

from agents.common import as_state, audit
from config import DATABASE_PATH
from database.sqlite_manager import SQLiteManager
from schemas.models import ConflictItem, ProjectState, RequirementItem


def detect_conflicts(requirements: list[RequirementItem]) -> list[ConflictItem]:
    found: list[ConflictItem] = []
    reported_issues: set[tuple[str, ...]] = set()
    for index, first in enumerate(requirements):
        for second in requirements[index + 1:]:
            if first.source_stakeholder == second.source_stakeholder:
                continue
            a, b = first.source_quote.lower(), second.source_quote.lower()
            kind, severity, description, resolution = "", "High", "", ""
            activation_with_no_wait = any(
                ("activation" in text or "activate" in text)
                and any(word in text for word in ("immediate", "instant", "without"))
                for text in (a, b)
            )
            audit_before_activation = any(
                "audit" in text and ("before" in text or "prior" in text)
                for text in (a, b)
            )
            indefinite_vs_retention = (
                ("indefinite" in a or "forever" in a)
                and ("retention" in b or "erase" in b)
                and any(term in b for term in ("video", "personal data", "data"))
            ) or (
                ("indefinite" in b or "forever" in b)
                and ("retention" in a or "erase" in a)
                and any(term in a for term in ("video", "personal data", "data"))
            )
            kfs_a = "kfs" in a or "key fact statement" in a
            kfs_b = "kfs" in b or "key fact statement" in b
            if activation_with_no_wait and audit_before_activation and a != b:
                kind, description = "Policy conflict", "Immediate activation conflicts with the required pre-activation audit."
                resolution = "Block activation until required verification and concurrent audit evidence are complete."
            elif (kfs_a and kfs_b and "disburs" in a and "disburs" in b
                  and "before" in a and "before" in b):
                kind = "Policy conflict"
                description = "Disbursal before KFS acknowledgment conflicts with the required pre-contract disclosure."
                resolution = "Require durable borrower KFS acknowledgment before contract execution and disbursal."
            elif indefinite_vs_retention:
                kind, description = "Contradiction", "Indefinite behavioral-data retention conflicts with purpose limitation and retention controls."
                resolution = "Define purpose-specific retention periods and statutory exceptions; require privacy/legal approval."
            else:
                nums_a = [int(value.replace(",", "")) for value in
                          re.findall(r"\b(\d{1,3}(?:,\d{3})*|\d{2,5})\s*ms\b", a)]
                nums_b = [int(value.replace(",", "")) for value in
                          re.findall(r"\b(\d{1,3}(?:,\d{3})*|\d{2,5})\s*ms\b", b)]
                if nums_a and nums_b and abs(nums_a[0] - nums_b[0]) >= 500:
                    kind, description = "SLA mismatch", f"Stakeholder latency targets differ ({nums_a[0]}ms vs {nums_b[0]}ms)."
                    resolution = "Agree end-to-end budget and distinguish application processing time from dependency latency."
                    severity = "Medium"
                elif ("zero document" in a or "without document" in a) and ("ovd" in b or "document" in b):
                    kind, description = "Contradiction", "Zero-document onboarding conflicts with mandatory identity-document verification."
                    resolution = "Define allowed digital document verification methods and mandatory evidence before activation."
                else:
                    normalize = lambda value: set(re.findall(r"[a-z0-9]+", value)) - {
                        "the", "system", "shall", "must", "and", "for", "with", "before", "after",
                        "when", "that", "this", "from", "into", "customer",
                    }
                    terms_a, terms_b = normalize(a), normalize(b)
                    overlap = len(terms_a & terms_b) / max(len(terms_a | terms_b), 1)
                    if overlap >= 0.82:
                        kind, severity = "Duplicate", "Low"
                        description = "Different stakeholders supplied substantially equivalent requirement statements."
                        resolution = "Consolidate into one traceable requirement while retaining both stakeholder evidence sources."
            if kind:
                if kind == "Policy conflict":
                    key = ("activation", first.req_id if "activate" in a or "activation" in a else second.req_id)
                elif kind == "Contradiction":
                    key = ("retention", first.req_id if "indefinite" in a or "forever" in a else second.req_id)
                else:
                    key = (kind, *sorted((first.req_id, second.req_id)))
                if key in reported_issues:
                    continue
                reported_issues.add(key)
                found.append(ConflictItem(
                    conflict_id=f"CON-{len(found) + 1:03d}", req_id_a=first.req_id, req_id_b=second.req_id,
                    conflict_type=kind, description=description, severity=severity,
                    suggested_resolution=resolution,
                ))
    return found


def conflict_detection(state: ProjectState | dict[str, Any]) -> dict[str, Any]:
    current = as_state(state)
    conflicts = detect_conflicts([RequirementItem.model_validate(item) for item in current.requirements])
    audit(current, "conflict_detection", f"Detected {len(conflicts)} cross-stakeholder conflicts",
          evidence="; ".join(conflict.description for conflict in conflicts[:3]))
    SQLiteManager(DATABASE_PATH).save_conflicts(current.project_id, conflicts)
    return {"conflicts": [item.model_dump(mode="json") for item in conflicts]}
