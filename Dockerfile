FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Non-secret defaults for validators / minimal env (HF_TOKEN must still be supplied as a secret).
ENV API_BASE_URL=https://openrouter.ai/api/v1
ENV MODEL_NAME=openai/gpt-4o-mini

EXPOSE 7860
CMD ["uvicorn", "openenv_email_triage.server:app", "--host", "0.0.0.0", "--port", "7860"]

