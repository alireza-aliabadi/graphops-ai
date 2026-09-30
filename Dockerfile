FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

COPY pyproject.toml poetry.lock README.md ./
COPY src ./src

RUN pip install --no-cache-dir "poetry>=2.0,<3.0" \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

EXPOSE 8000

CMD ["uvicorn", "graphops_ai.api:app", "--host", "0.0.0.0", "--port", "8000"]
