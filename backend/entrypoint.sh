#!/bin/sh
# Apply any pending database migrations, then start the API server.
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Starting API server..."
# Bind to $PORT when the platform provides one (e.g. Railway); default to 8000 locally.
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
