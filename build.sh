#!/usr/bin/env bash
set -o errexit

echo "========== Python Deployment Build =========="
echo "Python version:"
python --version
echo ""

echo "========== Upgrading pip =========="
pip install --upgrade pip setuptools wheel

echo "========== Installing dependencies =========="
cd backend
pip install -r requirements.txt

echo "========== Collecting static files =========="
python manage.py collectstatic --noinput --clear

echo "========== Running migrations =========="
python manage.py migrate

echo "========== Setting up social apps =========="
python manage.py setup_social_apps

echo "========== Build Complete =========="
echo "App is ready to start!"
