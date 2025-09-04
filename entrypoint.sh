#!/bin/bash
echo "entrypoint"

port=${PORT:-8000}
echo "$port @ $(pwd)"

whoami
echo "test" >> /etc/passwd

ls -lA
uv run python -V
uv run python manage.py makemigrations --noinput
uv run python manage.py migrate --noinput
uv run python manage.py collectstatic --noinput

uv run gunicorn config.wsgi:application --bind 0.0.0.0:"$port" --workers 3 --log-level=info

echo "entrypoint done"
