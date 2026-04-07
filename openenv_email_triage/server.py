from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from .environment import EmailTriageEnv
from .models import AgentAction

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


@app.post("/reset")
def reset(payload: ResetRequest) -> dict:
    obs = env.reset(payload.task_id)
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

