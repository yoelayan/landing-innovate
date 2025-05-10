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
COPY compose/entrypoint.sh /entrypoint.sh
COPY compose/start.sh /start.sh

# Make scripts executable
RUN chmod +x /entrypoint.sh
RUN chmod +x /start.sh

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False
ENV ALLOWED_HOSTS=localhost,127.0.0.1,.railway.app

# Default database configuration (override these in production)
ENV DATABASE_HOST=postgres.railway.internal
ENV DATABASE_PORT=5432
ENV DATABASE_NAME=railway
ENV DATABASE_USER=postgres
ENV DATABASE_PASSWORD=password

# Default superuser credentials - override these in production
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com
ENV DJANGO_SUPERUSER_PASSWORD=admin_password

# Install wait-for-it script for database connection checking
RUN apt-get update && apt-get install -y wait-for-it && rm -rf /var/lib/apt/lists/*

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/start.sh"]
