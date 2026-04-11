"""Root-level grader module - validators typically look for this file."""


def _clamp_score(score):
    """Ensure score is strictly between 0 and 1 (exclusive)."""
    return max(0.01, min(0.99, float(score)))


def _extract_state(state_or_env):
    """Support env objects, flat dicts, and dicts with nested status."""
    if isinstance(state_or_env, dict):
        state = state_or_env
    else:
        state = state_or_env.state() if hasattr(state_or_env, 'state') else {}

    status = state.get("status", {}) if isinstance(state, dict) else {}
    return {
        "category_done": bool(
            state.get("category_done", status.get("category_done", False))
        ),
        "priority_done": bool(
            state.get("priority_done", status.get("priority_done", False))
        ),
        "reply_done": bool(state.get("reply_done", status.get("reply_done", False))),
    }


def grade_easy(state_or_env):
    """Grade the easy task.
    
    Args:
        state_or_env: Either a dict (state) or env object with state() method
        
    Returns:
        float: Score strictly between 0 and 1
    """
    state = _extract_state(state_or_env)

    # Compute score based on state
    score = 0.0
    if state.get('category_done', False):
        score += 0.5
    if state.get('reply_done', False):
        score += 0.5
    
    return _clamp_score(score)


def grade_medium(state_or_env):
    """Grade the medium task.
    
    Args:
        state_or_env: Either a dict (state) or env object with state() method
        
    Returns:
        float: Score strictly between 0 and 1
    """
    state = _extract_state(state_or_env)

    score = 0.0
    if state.get('category_done', False):
        score += 0.3
    if state.get('priority_done', False):
        score += 0.3
    if state.get('reply_done', False):
        score += 0.4
    
    return _clamp_score(score)


def grade_hard(state_or_env):
    """Grade the hard task.
    
    Args:
        state_or_env: Either a dict (state) or env object with state() method
        
    Returns:
        float: Score strictly between 0 and 1
    """
    state = _extract_state(state_or_env)

    score = 0.0
    if state.get('category_done', False):
        score += 0.2
    if state.get('priority_done', False):
        score += 0.3
    if state.get('reply_done', False):
        score += 0.5
    
    return _clamp_score(score)


# Also export a generic grader (some validators may call grader.grade)
def grade(state_or_env):
    """Generic grade function (defaults to easy grader)."""
    return grade_easy(state_or_env)


GRADERS = {
    "easy-001": grade_easy,
    "medium-001": grade_medium,
    "hard-001": grade_hard,
    "grader_easy": grade_easy,
    "grader_medium": grade_medium,
    "grader_hard": grade_hard,
}


__all__ = ["grade_easy", "grade_medium", "grade_hard", "grade", "GRADERS"]
