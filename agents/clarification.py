from __future__ import annotations

import re
from typing import Any

from agents.common import as_state, audit
from schemas.models import ProjectState, RequirementItem

VAGUE_TERMS = ("fast", "user-friendly", "secure", "minimal friction", "high-value",
               "standard encryption", "quick", "seamless", "reasonable")


def clarify_requirements(requirements: list[RequirementItem]) -> tuple[list[RequirementItem], list[str]]:
    questions: list[str] = []
    for item in requirements:
        text = f"{item.statement} {item.source_quote}".lower()
        flags = [term for term in VAGUE_TERMS if term in text]
        missing_threshold = bool(re.search(r"\b(fast|quick|high[- ]value|standard|seamless)\b", text))
        if flags or (not item.acceptance_criteria) or missing_threshold:
            item.needs_clarification = True
            item.clarification_questions = [
                f"Please define a measurable threshold and test condition for '{flag}' in requirement {item.req_id}."
                for flag in flags
            ] or [f"What measurable acceptance threshold should apply to {item.req_id}?"]
            questions.extend(item.clarification_questions)
    return requirements, questions


def clarification(state: ProjectState | dict[str, Any]) -> dict[str, Any]:
    current = as_state(state)
    items = [RequirementItem.model_validate(item) for item in current.requirements]
    items, questions = clarify_requirements(items)
    audit(current, "clarification", f"Flagged {len(questions)} clarification question(s)",
          evidence="; ".join(questions[:4]))
    return {
        "requirements": [item.model_dump(mode="json") for item in items],
        "has_ambiguities": bool(questions), "follow_up_questions": questions,
        "clarification_round": current.clarification_round + (
            1 if current.interactive_mode and questions and
            current.clarification_round < current.max_clarification_rounds else 0
        ),
    }
