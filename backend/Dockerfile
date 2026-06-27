# syntax=docker/dockerfile:1

# ---------- Base ----------
FROM python:3.13-slim AS base

# Keep Python lean and predictable in containers.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# ---------- Dependencies ----------
# Copy requirements first so this layer is cached unless deps change.
COPY requirements.txt .
RUN pip install -r requirements.txt

# ---------- Application ----------
COPY app ./app

# Run as a non-root user.
RUN useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
