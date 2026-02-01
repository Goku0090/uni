web: gunicorn auth_project.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --worker-class sync --worker-connections 1000 --timeout 60
