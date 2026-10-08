#!/usr/bin/env bash
set -e
echo "Installing Python dependencies..."
python -m pip install -r requirements.txt
echo "Running tests..."
python -m pytest
echo "Starting production server..."
gunicorn app:app
