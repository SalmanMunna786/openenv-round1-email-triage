from __future__ import annotations

from typing import Any, Dict


def strict_score(value: float) -> float:
    # Phase-2 validator requires strict bounds: 0 < score < 1.
    return round(min(0.99, max(0.01, value)), 4)


def grade_email_triage(state: Dict[str, Any]) -> float:
    status = state.get("status", {})
    score = 0.0
    score += 0.4 if status.get("category_done") else 0.0
    score += 0.3 if status.get("priority_done") else 0.0
    score += 0.3 if status.get("reply_done") else 0.0
    return strict_score(score)


def grade_easy(state: Dict[str, Any]) -> float:
    return grade_email_triage(state)


def grade_medium(state: Dict[str, Any]) -> float:
    return grade_email_triage(state)


def grade_hard(state: Dict[str, Any]) -> float:
    return grade_email_triage(state)


GRADERS = {
    "grader_easy": grade_easy,
    "grader_medium": grade_medium,
    "grader_hard": grade_hard,
}

