#!/bin/bash
echo "entrypoint"

port=${PORT:-8000}
echo "$port @ $(pwd)"

whoami
echo "test" >> /etc/passwd

ls -lA
python -V
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

gunicorn config.wsgi:application --bind 0.0.0.0:"$port" --workers 3 --log-level=info

echo "entrypoint done"
