"""Grader functions for email triage environment."""


def strict_score(x):
    """Ensure score is strictly between 0 and 1."""
    return max(0.01, min(0.99, float(x)))


def grade_easy(source):
    """Grade easy task based on state."""
    if hasattr(source, 'state'):
        state = source.state()
    else:
        state = source if isinstance(source, dict) else {}
    
    score = 0.0
    if state.get('category_done', False):
        score += 0.5
    if state.get('reply_done', False):
        score += 0.5
    
    return strict_score(score)


def grade_medium(source):
    """Grade medium task based on state."""
    if hasattr(source, 'state'):
        state = source.state()
    else:
        state = source if isinstance(source, dict) else {}
    
    score = 0.0
    if state.get('category_done', False):
        score += 0.3
    if state.get('priority_done', False):
        score += 0.3
    if state.get('reply_done', False):
        score += 0.4
    
    return strict_score(score)


def grade_hard(source):
    """Grade hard task based on state."""
    if hasattr(source, 'state'):
        state = source.state()
    else:
        state = source if isinstance(source, dict) else {}
    
    score = 0.0
    if state.get('category_done', False):
        score += 0.2
    if state.get('priority_done', False):
        score += 0.3
    if state.get('reply_done', False):
        score += 0.5
    
    return strict_score(score)


def grade(source):
    """Generic grade function."""
    return 0.5


GRADERS = {
    "grader_easy": grade_easy,
    "grader_medium": grade_medium,
    "grader_hard": grade_hard,
}

