#!/bin/sh

python manage.py collectstatic --no-input
gunicorn --workers=2 --bind=:8000 backend_tax_calculator.wsgi:application