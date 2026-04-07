from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Category(str, Enum):
    billing = "billing"
    technical = "technical"
    account = "account"
    sales = "sales"


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ActionType(str, Enum):
    classify = "classify"
    reply = "reply"
    finish = "finish"


class Observation(BaseModel):
    task_id: str
    step_count: int
    email_text: str
    status: Dict[str, bool]
    history: List[str]
    allowed_actions: List[ActionType] = Field(
        default_factory=lambda: [ActionType.classify, ActionType.reply, ActionType.finish]
    )


class AgentAction(BaseModel):
    action_type: ActionType
    category: Optional[Category] = None
    priority: Optional[Priority] = None
    response_draft: Optional[str] = None


class RewardModel(BaseModel):
    value: float
    reason: str

