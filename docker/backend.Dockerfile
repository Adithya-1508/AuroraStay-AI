# Stage 1: Build virtualenv
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml .
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
RUN uv pip install --no-cache-dir .

# Stage 2: Final minimal runner
FROM python:3.12-slim AS runner

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

# Expose standard API Gateway port
EXPOSE 8000

CMD ["python", "-m", "shared.logging"]
