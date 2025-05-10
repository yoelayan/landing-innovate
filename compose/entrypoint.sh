#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Check if required environment variables are set
if [ -z "${DATABASE_HOST:-}" ]; then
    echo "ERROR: DATABASE_HOST environment variable is not set."
    exit 1
fi

if [ -z "${DATABASE_PORT:-}" ]; then
    echo "ERROR: DATABASE_PORT environment variable is not set."
    export DATABASE_PORT="5432"
    echo "Using default DATABASE_PORT: ${DATABASE_PORT}"
fi

if [ -z "${DATABASE_NAME:-}" ]; then
    echo "ERROR: DATABASE_NAME environment variable is not set."
    exit 1
fi

if [ -z "${DATABASE_USER:-}" ]; then
    base_postgres_image_default_user='postgres'
    export DATABASE_USER="${base_postgres_image_default_user}"
    echo "Using default DATABASE_USER: ${DATABASE_USER}"
fi

if [ -z "${DATABASE_PASSWORD:-}" ]; then
    echo "ERROR: DATABASE_PASSWORD environment variable is not set."
    exit 1
fi

# Export the DATABASE_URL
export DATABASE_URL="postgres://${DATABASE_USER}:${DATABASE_PASSWORD}@${DATABASE_HOST}:${DATABASE_PORT}/${DATABASE_NAME}"
echo "Database URL: ${DATABASE_URL}"

# Wait for the database to be available
echo "Waiting for database at ${DATABASE_HOST}:${DATABASE_PORT}..."
wait-for-it ${DATABASE_HOST}:${DATABASE_PORT} -t 30

echo "PostgreSQL is available"

# Execute the command passed to the script
exec "$@"
