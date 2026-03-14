FROM python:3.11

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml .

RUN pip install ".[backend]"

COPY backend/alembic ./alembic
COPY backend/alembic.ini .
COPY backend/app/ ./app/
COPY backend/scripts/ ./scripts/
COPY backend/entrypoint.sh .

RUN chmod +x entrypoint.sh

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

ENTRYPOINT ["./entrypoint.sh"]
