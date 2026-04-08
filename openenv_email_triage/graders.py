from __future__ import annotations

from typing import Any, Dict


def strict_score(value: float) -> float:
    """Map [0,1] linearly into (0.01, 0.99) — Phase 2 rejects exact 0.0 and 1.0."""
    x = min(1.0, max(0.0, float(value)))
    return round(0.01 + x * 0.98, 4)


def _to_state(source: Any) -> Dict[str, Any]:
    """Accept either a state dict or env object (with .state())."""
    if isinstance(source, dict):
        return source
    state_fn = getattr(source, "state", None)
    if callable(state_fn):
        try:
            out = state_fn()
            if isinstance(out, dict):
                return out
        except Exception:
            pass
    return {"status": {}}


def _weighted_status(
    source: Any, w_cat: float, w_pri: float, w_rep: float
) -> float:
    state = _to_state(source)
    status = state.get("status", {})
    raw = (
        w_cat * float(bool(status.get("category_done")))
        + w_pri * float(bool(status.get("priority_done")))
        + w_rep * float(bool(status.get("reply_done")))
    )
    return strict_score(raw)


def grade_easy(source: Any) -> float:
    # Slightly more weight on correct category (easy task).
    return _weighted_status(source, 0.45, 0.30, 0.25)


def grade_medium(source: Any) -> float:
    return _weighted_status(source, 0.40, 0.35, 0.25)


def grade_hard(source: Any) -> float:
    # Hard task: more weight on reply quality proxy (completion flag).
    return _weighted_status(source, 0.35, 0.33, 0.32)


def grade(source: Any) -> float:
    """
    Generic grader fallback for validators that only call `grade(env)`.
    Uses medium rubric by default and keeps strict (0,1) output.
    """
    return grade_medium(source)


GRADERS = {
    "grader_easy": grade_easy,
    "grader_medium": grade_medium,
    "grader_hard": grade_hard,
}
