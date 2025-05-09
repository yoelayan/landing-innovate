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

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False
ENV ALLOWED_HOSTS=localhost,127.0.0.1,.railway.app

# Default superuser credentials - override these in production
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com
ENV DJANGO_SUPERUSER_PASSWORD=admin_password

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Create a script to run migrations and start the server
RUN echo '#!/bin/bash\nset -e\n\necho "Checking for conflicting migrations and resolving if needed..."\npython manage.py resolve_migrations --no-input\n\necho "Creating superuser if needed..."\npython manage.py createsuperuser_env\n\necho "Starting web server..."\nexec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT' > /app/start.sh
RUN chmod +x /app/start.sh

# Run the script
CMD ["/app/start.sh"]
