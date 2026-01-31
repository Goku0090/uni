#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install --upgrade pip
pip install -r auth_project/requirements.txt

# Collect static files
cd auth_project
python manage.py collectstatic --noinput --clear

# Run database migrations
python manage.py migrate

# Create superuser if needed (optional)
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'adminpass') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# Create logs directory
mkdir -p logs

echo "Build completed successfully!"
