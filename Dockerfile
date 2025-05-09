FROM python:3.10-slim

WORKDIR /app

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
RUN echo '#!/bin/bash\npython manage.py migrate\npython manage.py createsuperuser_env\ngunicorn config.wsgi:application --bind 0.0.0.0:$PORT' > /app/start.sh
RUN chmod +x /app/start.sh

# Run the script
CMD ["/app/start.sh"]
