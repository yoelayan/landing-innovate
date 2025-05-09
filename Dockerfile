FROM python:3.10-slim

WORKDIR /app

# Install system dependencies required for psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# update pip
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

# Collect static files
RUN python manage.py collectstatic --noinput

# check migrations
RUN python manage.py resolve_migrations --no-input
# cargar fixtures
RUN python manage.py loaddata apps/pages/fixtures/brand.json
RUN python manage.py loaddata apps/pages/fixtures/site_images.json

# create superuser
RUN python manage.py createsuperuser_env

# Expose the port the app runs on
EXPOSE 8000

# run server
RUN echo '#!/bin/bash\nset -e\n\necho "Starting web server..."\nexec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT' > /app/start.sh

RUN chmod +x /app/start.sh

# Run the script
CMD ["/app/start.sh"]
