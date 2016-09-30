#!/usr/bin/env bash

# Activate virtual env
. /opt/python/venv/google-portal/bin/activate

# Run Django server
python manage.py runserver 0.0.0.0:8000
