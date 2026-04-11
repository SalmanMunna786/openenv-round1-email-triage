"""Root-level grader module - validators typically look for this file."""


def _clamp_score(score):
    """Ensure score is strictly between 0 and 1 (exclusive)."""
    return max(0.01, min(0.99, float(score)))


def grade_easy(state_or_env):
    """Grade the easy task.
    
    Args:
        state_or_env: Either a dict (state) or env object with state() method
        
    Returns:
        float: Score strictly between 0 and 1
    """
    # Handle both state dict and env object
    if isinstance(state_or_env, dict):
        state = state_or_env
    else:
        state = state_or_env.state() if hasattr(state_or_env, 'state') else {}
    
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
    if isinstance(state_or_env, dict):
        state = state_or_env
    else:
        state = state_or_env.state() if hasattr(state_or_env, 'state') else {}
    
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
    if isinstance(state_or_env, dict):
        state = state_or_env
    else:
        state = state_or_env.state() if hasattr(state_or_env, 'state') else {}
    
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


__all__ = ["grade_easy", "grade_medium", "grade_hard", "grade"]

