from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _ok(msg: str) -> None:
    print(f"[OK] {msg}")


def _fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    raise SystemExit(1)


def main() -> None:
    required_files = [
        "inference.py",
        "openenv.yaml",
        "Dockerfile",
        "uv.lock",
        "server/app.py",
    ]
    for rel in required_files:
        if not (ROOT / rel).exists():
            _fail(f"Missing required file: {rel}")
    _ok("Required files present")

    yaml_text = (ROOT / "openenv.yaml").read_text(encoding="utf-8")
    if "spec_version: 1" not in yaml_text:
        _fail("openenv.yaml must use Meta manifest spec_version: 1 (see OpenEnv docs)")
    if "server.app:app" not in yaml_text:
        _fail("openenv.yaml must set app: server.app:app")
    for task_id in ("easy-001", "medium-001", "hard-001"):
        if task_id not in yaml_text:
            _fail(f"Task missing from openenv.yaml: {task_id}")
    for grader in ("grade_easy", "grade_medium", "grade_hard"):
        if grader not in yaml_text:
            _fail(f"Grader missing in openenv.yaml: {grader}")
    _ok("openenv.yaml contains 3 tasks and 3 graders")

    pyproject_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    if "openenv-core[core]>=0.2.2" not in pyproject_text:
        _fail("pyproject.toml must include openenv-core[core]>=0.2.2")
    _ok("pyproject.toml contains required OpenEnv core dependency")

    server_text = (ROOT / "openenv_email_triage" / "server.py").read_text(encoding="utf-8")
    for endpoint in ('@app.get("/tasks")', '@app.get("/grader")'):
        if endpoint not in server_text:
            _fail(f"Missing server endpoint: {endpoint}")
    _ok("Server exposes tasks and grader endpoints")

    env = os.environ.copy()
    env.setdefault("API_BASE_URL", "https://openrouter.ai/api/v1")
    env.setdefault("MODEL_NAME", "openai/gpt-4o-mini")
    run = subprocess.run(
        [sys.executable, str(ROOT / "inference.py")],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    if run.returncode != 0:
        print(run.stdout)
        print(run.stderr)
        _fail("inference.py exits non-zero")

    lines = [ln.strip() for ln in run.stdout.splitlines() if ln.strip()]
    if not any(ln.startswith("[START]") for ln in lines):
        _fail("Missing [START] log")
    if not any(ln.startswith("[STEP]") for ln in lines):
        _fail("Missing [STEP] log")
    if not any(ln.startswith("[END] overall_score=") for ln in lines):
        _fail("Missing [END] overall log")

    score_line = next(ln for ln in lines if ln.startswith("[END] overall_score="))
    # Parse the trailing scores JSON safely.
    scores_part = score_line.split("scores=", 1)[1]
    scores = json.loads(scores_part)
    if len(scores) < 3:
        _fail("Less than 3 task scores found")
    for task_id, score in scores.items():
        if not (0.0 < float(score) < 1.0):
            _fail(f"Score out of strict range for {task_id}: {score}")
    _ok("Inference logs and scores validated")
    _ok("Preflight passed")


if __name__ == "__main__":
    main()

