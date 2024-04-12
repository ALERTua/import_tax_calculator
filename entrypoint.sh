#!/bin/bash
echo "entrypoint"

export PYTHONIOENCODING=utf-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

cd $BASE_DIR || (echo "Cannot CD to $BASE_DIR. Exiting" & exit)

port=${PORT:-8000}

echo "$port @ $(pwd)"

ls -lA
python -V
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

gunicorn config.wsgi:application --bind 0.0.0.0:"$port" --workers 3 --log-level=info

echo "entrypoint done"
