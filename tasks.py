"""Root-level task exports for validator compatibility."""

from grader import grade_easy, grade_hard, grade_medium


TASKS = [
    {
        "id": "easy-001",
        "task_id": "easy-001",
        "name": "easy-001",
        "difficulty": "easy",
        "description": (
            "Classify a duplicate-charge support email and provide a refund-oriented reply."
        ),
        "grader": grade_easy,
        "grader_path": "grader.grade_easy",
    },
    {
        "id": "medium-001",
        "task_id": "medium-001",
        "name": "medium-001",
        "difficulty": "medium",
        "description": (
            "Handle an urgent account lockout caused by missing 2FA codes."
        ),
        "grader": grade_medium,
        "grader_path": "grader.grade_medium",
    },
    {
        "id": "hard-001",
        "task_id": "hard-001",
        "name": "hard-001",
        "difficulty": "hard",
        "description": (
            "Handle an API outage report that also mentions invoice discrepancies."
        ),
        "grader": grade_hard,
        "grader_path": "grader.grade_hard",
    },
]


def get_tasks():
    """Return tasks in a validator-friendly format."""
    return TASKS


__all__ = ["TASKS", "get_tasks"]
