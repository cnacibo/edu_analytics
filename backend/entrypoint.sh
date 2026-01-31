#!/usr/bin/env sh
set -e

echo "Waiting for database..."
until pg_isready -h postgres -p 5432 -U "$POSTGRES_USER"; do
  sleep 1
done

echo "Running migrations..."
alembic upgrade head

echo "Starting backend..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
