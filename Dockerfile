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

# Install wait-for-it script for database connection checking
RUN apt-get update && apt-get install -y wait-for-it && rm -rf /var/lib/apt/lists/*

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

CMD ["/entrypoint.sh", "/start.sh"]
