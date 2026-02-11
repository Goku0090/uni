web: cd auth_project && python manage.py migrate && gunicorn auth_project.wsgi:application --workers 3 --bind 0.0.0.0:8000
