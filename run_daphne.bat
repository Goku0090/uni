@echo off
REM WebSocket Development Server (Windows)
REM Run this instead of: python manage.py runserver

cd /d "%~dp0auth_project"

REM Set Django settings module
set DJANGO_SETTINGS_MODULE=auth_project.settings
set PYTHONUNBUFFERED=1

echo ========================================
echo Starting Daphne ASGI Server
echo ========================================
echo.
echo Server will be available at:
echo   HTTP:      http://localhost:8000
echo   WebSocket: ws://localhost:8000
echo.
echo Features enabled:
echo   ✅ HTTP (Django views)
echo   ✅ WebSocket (real-time updates)
echo.
echo Press Ctrl+C to stop
echo ========================================
echo.

python -m daphne -b 127.0.0.1 -p 8000 auth_project.asgi:application
