#!/bin/bash
set -e

cd auth_project

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || true

echo "Starting gunicorn on port 8000..."
exec gunicorn auth_project.wsgi:application \
    --workers 3 \
    --worker-class sync \
    --bind 0.0.0.0:8000 \
    --timeout 120
