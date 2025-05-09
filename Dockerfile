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

# Copiar el código de la aplicación
COPY app/ .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False
ENV ALLOWED_HOSTS=localhost,127.0.0.1,.railway.app

# Establecer la ruta del archivo .env
ENV ENV_PATH=/app/.env

# Default superuser credentials - override these in production
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com
ENV DJANGO_SUPERUSER_PASSWORD=admin_password

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

# Create a script that genera un .env file from environment variables and starts the server
RUN echo '#!/bin/bash\nset -e\n\necho "Generating .env file from environment variables..."\ntouch $ENV_PATH\n\n# Add variables to .env\n[[ -n "$SECRET_KEY" ]] && echo "SECRET_KEY=$SECRET_KEY" >> $ENV_PATH\n[[ -n "$DEBUG" ]] && echo "DEBUG=$DEBUG" >> $ENV_PATH\n[[ -n "$ALLOWED_HOSTS" ]] && echo "ALLOWED_HOSTS=$ALLOWED_HOSTS" >> $ENV_PATH\n[[ -n "$DATABASE_URL" ]] && echo "DATABASE_URL=$DATABASE_URL" >> $ENV_PATH\n[[ -n "$DJANGO_SUPERUSER_USERNAME" ]] && echo "DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME" >> $ENV_PATH\n[[ -n "$DJANGO_SUPERUSER_EMAIL" ]] && echo "DJANGO_SUPERUSER_EMAIL=$DJANGO_SUPERUSER_EMAIL" >> $ENV_PATH\n[[ -n "$DJANGO_SUPERUSER_PASSWORD" ]] && echo "DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD" >> $ENV_PATH\n\necho "Starting web server..."\nexec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT' > /app/start.sh

RUN chmod +x /app/start.sh

# Run the script
CMD ["/app/start.sh"]
