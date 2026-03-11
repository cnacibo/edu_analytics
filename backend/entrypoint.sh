#!/usr/bin/env sh
set -e

echo "Waiting for database..."
until pg_isready -h postgres -p 5432 -U "$POSTGRES_USER"; do
  sleep 1
done

echo "Running migrations..."
alembic upgrade head

if [ -n "$(ls -A /app/storage/files)" ] || [ "$FORCE_LOAD_DATA" = "true" ]; then
    echo "Loading initial data..."
    python -u scripts/load_data.py 2>&1 | tee /tmp/load.log
    cat /tmp/load.log
    echo "Exit code: $?"
else
    echo "No data files found, skipping data loading"
fi

echo "Starting backend..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
