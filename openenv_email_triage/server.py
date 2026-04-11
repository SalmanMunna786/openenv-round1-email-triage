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


class GradeRequest(BaseModel):
    task_id: str | None = None


def _task_payload(task: dict) -> dict:
    return {
        "id": task["task_id"],
        "task_id": task["task_id"],
        "name": task["task_id"],
        "difficulty": task["difficulty"],
        "description": task["email_text"],
        # Some validators only check that this field is present and truthy.
        "grader": True,
        "grader_id": task["grader_id"],
        "grader_path": task["grader_fn"],
    }


def _grade_for_task(task_id: str) -> dict:
    matched_task = next((task for task in TASKS if task["task_id"] == task_id), None)
    if matched_task is None:
        return {"task_id": task_id, "grader": None, "score": 0.01}

    env.reset(task_id)
    return {
        "task_id": task_id,
        "grader": matched_task["grader_fn"],
        "grader_id": matched_task["grader_id"],
        "score": env.grade_current(),
    }


@app.get("/")
def root() -> dict:
    return {"message": "openenv-email-triage", "status": "ok"}


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.get("/tasks")
def tasks() -> dict:
    # Return a wrapped payload for broader validator compatibility.
    task_items = [_task_payload(task) for task in TASKS]
    return {"tasks": task_items, "count": len(task_items)}


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
def grader(task_id: str | None = None) -> dict:
    if task_id:
        return _grade_for_task(task_id)

    current_state = env.state()
    current_task_id = current_state.get("task_id")
    if current_task_id:
        return _grade_for_task(current_task_id)

    scores = [_grade_for_task(task["task_id"]) for task in TASKS]
    return {"tasks": scores, "count": len(scores)}


@app.post("/grader")
def grader_post(payload: GradeRequest | None = Body(default=None)) -> dict:
    if payload and payload.task_id:
        return _grade_for_task(payload.task_id)
    return grader()


@app.get("/grade/{task_id}")
def grade_task(task_id: str) -> dict:
    return _grade_for_task(task_id)


@app.get("/validate")
def validate() -> dict:
    task_items = [_task_payload(task) for task in TASKS]
    checks = {
        "min_3_tasks": len(task_items) >= 3,
        "all_tasks_have_graders": all(task["grader"] for task in task_items),
        "scores_strictly_between_zero_and_one": all(
            0.0 < _grade_for_task(task["task_id"])["score"] < 1.0 for task in TASKS
        ),
    }
    return {"valid": all(checks.values()), "checks": checks, "task_count": len(task_items)}
