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
    # Expose grader metadata directly so validators can confirm task wiring.
    return [
        {
            "id": task["task_id"],
            "task_id": task["task_id"],
            "difficulty": task["difficulty"],
            "grader": task["grader_fn"],
            "grader_id": task["grader_id"],
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


@app.get("/grader")
def grader() -> dict:
    current_state = env.state()
    task_id = current_state.get("task_id")
    grader_name = None
    for task in TASKS:
        if task["task_id"] == task_id:
            grader_name = task["grader_id"]
            break
    return {
        "task_id": task_id,
        "grader": grader_name,
        "score": env.grade_current(),
    }
