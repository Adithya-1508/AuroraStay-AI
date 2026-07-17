# Stage 1: Build virtual environment and dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir --user .

# Stage 2: Runtime image
FROM python:3.12-slim AS runtime

WORKDIR /app

RUN groupadd -r hospitality && useradd -r -g hospitality hospitality

COPY --from=builder /root/.local /home/hospitality/.local
COPY . .

RUN chown -R hospitality:hospitality /app

ENV PATH=/home/hospitality/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

USER hospitality

EXPOSE 3000

CMD ["python", "-m", "streamlit", "run", "dashboard/app.py", "--server.port=3000", "--server.address=0.0.0.0"]
