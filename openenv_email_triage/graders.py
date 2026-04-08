def grade_easy(source):
    return 0.5

def grade_medium(source):
    return 0.6

def grade_hard(source):
    return 0.7

def grade(source):
    return 0.5

GRADERS = {
    "grader_easy": grade_easy,
    "grader_medium": grade_medium,
    "grader_hard": grade_hard,
}
