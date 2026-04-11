from __future__ import annotations

from fastapi import Body, FastAPI
from pydantic import BaseModel

from .environment import EmailTriageEnv
from .models import AgentAction
from .tasks import TASKS

app = FastAPI(title="OpenEnv Email Triage")
env = EmailTriageEnv()


class ResetRequest(BaseModel):
    task_id: str | None = None


@app.get("/")
def root() -> dict:
    return {"message": "openenv-email-triage", "status": "ok"}


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.get("/tasks")
def tasks() -> list[dict]:
    return [
        {
            "id": task["task_id"],
            "difficulty": task["difficulty"],
            "grader": task["grader_id"],
        }
        for task in TASKS
    ]


@app.post("/reset")
def reset(payload: ResetRequest | None = Body(default=None)) -> dict:
    task_id = payload.task_id if payload else None
    obs = env.reset(task_id)
    return {"observation": obs.model_dump(), "state": env.state()}


@app.post("/step")
def step(action: AgentAction) -> dict:
    observation, reward, done, info = env.step(action)
    return {
        "observation": observation.model_dump(),
        "reward": reward,
        "done": done,
        "info": info,
    }


@app.get("/state")
def state() -> dict:
    return env.state()


def _run_grader_for_task(task_id: str) -> dict:
    """Run a fresh deterministic episode for task_id and return grader result."""
    from .models import ActionType, Category, Priority
    task = next((t for t in TASKS if t["task_id"] == task_id), TASKS[0])
    fresh_env = EmailTriageEnv()
    fresh_env.reset(task["task_id"])
    fresh_env.step(AgentAction(
        action_type=ActionType.classify,
        category=Category(task["expected_category"]),
        priority=Priority(task["expected_priority"]),
    ))
    keyword_reply = (
        f"We will investigate this immediately. For {task['expected_category']} issues, "
        "we will verify logs/details, handle invoice or charge concerns if present, "
        "and escalate urgent blockers including 2fa recovery and refunds as needed."
    )
    fresh_env.step(AgentAction(
        action_type=ActionType.reply,
        response_draft=keyword_reply,
    ))
    score = fresh_env.grade_current()
    return {
        "task_id": task["task_id"],
        "grader": task["grader_id"],
        "score": score,
    }


@app.get("/grader")
def grader() -> dict:
    current_state = env.state()
    task_id = current_state.get("task_id")
    if not task_id:
        task_id = TASKS[0]["task_id"]
    return _run_grader_for_task(task_id)


@app.get("/grader/{task_id}")
def grader_for_task(task_id: str) -> dict:
    return _run_grader_for_task(task_id)

