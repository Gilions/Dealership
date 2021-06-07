#!/bin/sh
sleep 3
python manage.py migrate
python manage.py createcachetable
python manage.py collectstatic  --noinput
gunicorn dealership.wsgi:application --bind 0.0.0.0:8000
exec "$@"