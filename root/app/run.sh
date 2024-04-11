#!/bin/bash
export PYTHONIOENCODING=utf-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

cd /app/ || (echo "Cannot CD to /app/. Exiting" & exit)
port=${PORT:-8000}
echo "start $APP_NAME at $port @ $(pwd)"

/usr/local/bin/python -V
/usr/local/bin/python manage.py makemigrations --noinput
/usr/local/bin/python manage.py migrate --noinput
/usr/local/bin/python manage.py collectstatic --noinput

gunicorn "$APP_NAME".wsgi:application --bind 0.0.0.0:"$port" --workers 3 --log-level=info

echo "done $APP_NAME"
