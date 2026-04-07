TASKS = [
    {
        "task_id": "easy-001",
        "difficulty": "easy",
        "email_text": (
            "Subject: Duplicate charge\n"
            "Hello support, I was charged twice for my March subscription. "
            "Can you refund one of the charges?"
        ),
        "expected_category": "billing",
        "expected_priority": "medium",
        "reply_keywords": ["refund", "charge", "investigate"],
    },
    {
        "task_id": "medium-001",
        "difficulty": "medium",
        "email_text": (
            "Subject: Locked out of account\n"
            "I enabled 2FA yesterday and now the OTP code never arrives. "
            "I cannot log in and have an urgent client demo in 2 hours."
        ),
        "expected_category": "account",
        "expected_priority": "high",
        "reply_keywords": ["verify", "2fa", "recovery", "urgent"],
    },
    {
        "task_id": "hard-001",
        "difficulty": "hard",
        "email_text": (
            "Subject: API failures and invoice mismatch\n"
            "Our integration is returning 500 errors after the latest release, "
            "and finance also reports invoice totals that do not match usage."
        ),
        "expected_category": "technical",
        "expected_priority": "high",
        "reply_keywords": ["logs", "incident", "billing", "escalate"],
    },
]

