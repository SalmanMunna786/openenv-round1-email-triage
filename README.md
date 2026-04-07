---
title: openenv-email-triage
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_file: inference.py
pinned: false
---

# OpenEnv Round 1 - Email Triage Environment

This project implements a real-world OpenEnv environment for customer support email triage.

## What this environment simulates

An AI agent receives incoming support emails and must:

1. classify the issue category,
2. assign the right priority,
3. draft a useful first response.

This mirrors practical workflows in support teams.

## OpenEnv interface

- `reset(task_id: str | None)` returns initial observation
- `step(action)` returns `(observation, reward, done, info)`
- `state()` returns current environment state

Typed models are implemented with Pydantic in `openenv_email_triage/models.py`.

## Tasks and difficulty

- `easy-001`: duplicate billing charge (easy)
- `medium-001`: account lockout with 2FA issue (medium)
- `hard-001`: technical outage + billing mismatch (hard)

Each task has deterministic grading with score in `[0.0, 1.0]`.

## Reward design

- +0.4 for correct category classification
- +0.3 for correct priority
- +up to 0.3 for high-quality response draft (keyword coverage)
- small penalties for wrong guesses and max-step overflow

This creates partial-progress feedback rather than all-or-nothing rewards.

## Environment variables

Set these before running `inference.py`:

- `API_BASE_URL` (example: `https://openrouter.ai/api/v1`)
- `MODEL_NAME` (example: `openai/gpt-4o-mini`)
- `HF_TOKEN` (API key)

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export API_BASE_URL="https://openrouter.ai/api/v1"
export MODEL_NAME="openai/gpt-4o-mini"
export HF_TOKEN="your_api_key"

python inference.py
```

## Structured logs

`inference.py` prints:

- `[START]` run metadata
- `[STEP]` per action step
- `[END]` per-task and overall scores

## API server (for HF Space)

```bash
uvicorn openenv_email_triage.server:app --host 0.0.0.0 --port 7860
```

Endpoints:

- `GET /health`
- `POST /reset`
- `POST /step`
- `GET /state`

## Docker

```bash
docker build -t openenv-email-triage .
docker run -p 7860:7860 openenv-email-triage
```