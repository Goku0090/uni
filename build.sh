#!/usr/bin/env bash
set -o errexit

echo "========== Python Deployment Build =========="
echo "Python version:"
python --version
echo ""

echo "========== Upgrading pip =========="
pip install --upgrade pip setuptools wheel

echo "========== Installing dependencies =========="
cd auth_project
pip install -r requirements.txt

echo "========== Collecting static files =========="
python manage.py collectstatic --noinput --clear

echo "========== Running migrations =========="
python manage.py migrate

echo "========== Build Complete =========="
echo "App is ready to start!"
