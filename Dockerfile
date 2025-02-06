FROM python:3.9-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml \
    uv.lock ./


FROM builder AS dev

ENV UV_PROJECT_ENVIRONMENT=/opt/.venv/
ENV PATH="/opt/.venv/bin:$PATH"

RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv sync --frozen --extra dev

COPY src/ /app

CMD ["python", "main.py"]
