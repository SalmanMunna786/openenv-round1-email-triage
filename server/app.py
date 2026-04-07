import os

import uvicorn

from openenv_email_triage.server import app as fastapi_app

app = fastapi_app


def main() -> None:
    port = int(os.getenv("PORT", "7860"))
    uvicorn.run("server.app:app", host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()

