FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

# Collect static files
RUN python manage.py collectstatic --noinput

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# Expose the port the app runs on
EXPOSE 8000

# Run gunicorn
CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
