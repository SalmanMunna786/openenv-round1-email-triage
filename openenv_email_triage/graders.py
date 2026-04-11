def strict_score(x):
    return max(0.01, min(0.99, x))

def grade_easy(source):
    if hasattr(source, 'state'):
        state = source.state()
    else:
        state = source
    score = 0.0
    if state.get('category_done', False):
        score += 0.5
    if state.get('reply_done', False):
        score += 0.5
    return strict_score(score)

def grade_medium(source):
    if hasattr(source, 'state'):
        state = source.state()
    else:
        state = source
    score = 0.0
    if state.get('category_done', False):
        score += 0.3
    if state.get('priority_done', False):
        score += 0.3
    if state.get('reply_done', False):
        score += 0.4
    return strict_score(score)

def grade_hard(source):
    if hasattr(source, 'state'):
        state = source.state()
    else:
        state = source
    score = 0.0
    if state.get('category_done', False):
        score += 0.2
    if state.get('priority_done', False):
        score += 0.3
    if state.get('reply_done', False):
        score += 0.5
    return strict_score(score)

def grade(source):
    return 0.5

GRADERS = {
    "grader_easy": grade_easy,
    "grader_medium": grade_medium,
    "grader_hard": grade_hard,
}
