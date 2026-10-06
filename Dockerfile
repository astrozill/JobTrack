FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home appuser && chown appuser:appuser /app

COPY --chown=appuser:appuser . .

USER appuser

# Collect assets without runtime secrets or a database connection.
# These temporary values apply only to this build command.
RUN DJANGO_SECRET_KEY=build-only-secret-for-collectstatic \
    DB_NAME=collectstatic DB_USER=collectstatic DB_PASSWORD=unused \
    DB_HOST=localhost DB_PORT=5432 \
    python manage.py collectstatic --noinput

EXPOSE 8000

# Local development; supply Django and database environment variables at runtime.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
