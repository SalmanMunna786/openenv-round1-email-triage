from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple

from .graders import GRADERS, strict_score
from .models import ActionType, AgentAction, Observation
from .tasks import TASKS


def _reply_score(response: str, keywords: list[str]) -> float:
    if not response:
        return 0.0
    lowered = response.lower()
    matched = sum(1 for k in keywords if k in lowered)
    return matched / len(keywords)


@dataclass
class EpisodeState:
    task: Dict[str, Any]
    step_count: int = 0
    max_steps: int = 5
    category_done: bool = False
    priority_done: bool = False
    reply_done: bool = False
    history: list[str] = field(default_factory=list)


class EmailTriageEnv:
    def __init__(self) -> None:
        self.tasks_by_id = {t["task_id"]: t for t in TASKS}
        self.current: EpisodeState | None = None

    def reset(self, task_id: str | None = None) -> Observation:
        if task_id and task_id in self.tasks_by_id:
            task = self.tasks_by_id[task_id]
        else:
            task = TASKS[0]
        self.current = EpisodeState(task=task)
        return self._observation()

    def state(self) -> Dict[str, Any]:
        if self.current is None:
            return {"ready": False}
        return {
            "ready": True,
            "task_id": self.current.task["task_id"],
            "step_count": self.current.step_count,
            "category_done": self.current.category_done,
            "priority_done": self.current.priority_done,
            "reply_done": self.current.reply_done,
            "status": {
                "category_done": self.current.category_done,
                "priority_done": self.current.priority_done,
                "reply_done": self.current.reply_done,
            },
        }

    def step(self, action: AgentAction) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        if self.current is None:
            # Defensive default for validators calling step() first.
            self.reset()

        s = self.current
        s.step_count += 1
        reward = 0.0
        reason = "no_progress"

        if action.action_type == ActionType.classify:
            reward, reason = self._apply_classification(action)
        elif action.action_type == ActionType.reply:
            reward, reason = self._apply_reply(action)
        elif action.action_type == ActionType.finish:
            reason = "agent_finished"
            reward = 0.0
        else:
            reward, reason = -0.1, "invalid_action"

        s.history.append(f"{action.action_type.value}:{reason}")

        done = self._all_done() or action.action_type == ActionType.finish or s.step_count >= s.max_steps
        if s.step_count >= s.max_steps and not self._all_done():
            reward -= 0.2
            reason = "max_steps_penalty"

        info = {"reason": reason, "task_id": s.task["task_id"], "score": self.grade_current()}
        return self._observation(), round(reward, 4), done, info

    def grade_current(self) -> float:
        if self.current is None:
            return 0.01
        grader_id = self.current.task.get("grader_id", "")
        grader = GRADERS.get(grader_id)
        if grader is None:
            # Safe fallback: still keep strict score bounds for validator.
            score = 0.0
            score += 0.4 if self.current.category_done else 0.0
            score += 0.3 if self.current.priority_done else 0.0
            score += 0.3 if self.current.reply_done else 0.0
            return strict_score(score)
        return grader(self.state())

    def _all_done(self) -> bool:
        assert self.current is not None
        return self.current.category_done and self.current.priority_done and self.current.reply_done

    def _apply_classification(self, action: AgentAction) -> tuple[float, str]:
        assert self.current is not None
        reward = 0.0
        reason = []
        if action.category and action.category.value == self.current.task["expected_category"]:
            if not self.current.category_done:
                self.current.category_done = True
                reward += 0.4
            reason.append("category_ok")
        else:
            reward -= 0.05
            reason.append("category_wrong")

        if action.priority and action.priority.value == self.current.task["expected_priority"]:
            if not self.current.priority_done:
                self.current.priority_done = True
                reward += 0.3
            reason.append("priority_ok")
        else:
            reward -= 0.05
            reason.append("priority_wrong")
        return round(reward, 4), ",".join(reason)

    def _apply_reply(self, action: AgentAction) -> tuple[float, str]:
        assert self.current is not None
        score = _reply_score(action.response_draft or "", self.current.task["reply_keywords"])
        if score >= 0.5:
            self.current.reply_done = True
            return round(0.3 * score, 4), "reply_good"
        return -0.05, "reply_weak"

    def _observation(self) -> Observation:
        assert self.current is not None
        return Observation(
            task_id=self.current.task["task_id"],
            step_count=self.current.step_count,
            email_text=self.current.task["email_text"],
            status={
                "category_done": self.current.category_done,
                "priority_done": self.current.priority_done,
                "reply_done": self.current.reply_done,
            },
            history=self.current.history,
        )
