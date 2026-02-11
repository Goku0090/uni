#!/bin/bash
set -e

# Get port from environment or default to 8000
PORT=${PORT:-8000}
echo "Using PORT: $PORT"

cd auth_project

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || true

echo "Starting gunicorn on port $PORT..."
exec gunicorn auth_project.wsgi:application \
    --workers 3 \
    --worker-class sync \
    --bind 0.0.0.0:$PORT \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
