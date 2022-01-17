#!/bin/bash
set -e

python manage.py migrate --noinput &&
python manage.py loaddata reporter_tests/fixtures/auth_user.json &&
python manage.py runserver 0.0.0.0:8000
