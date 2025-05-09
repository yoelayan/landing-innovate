#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

echo "Applying database migrations..."
python /app/manage.py migrate

echo "Creating superuser if needed..."
python /app/manage.py createsuperuser_env

echo "Collecting static files..."
python /app/manage.py collectstatic --noinput

echo "Starting web server..."
exec /usr/local/bin/gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}