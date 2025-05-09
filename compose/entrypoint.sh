#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

if [ -z "${DATABASE_USER}" ]; then
    base_postgres_image_default_user='postgres'
    export POSTGRES_USER="${base_postgres_image_default_user}"
fi
export DATABASE_URL="postgres://${DATABASE_USER}:${DATABASE_PASSWORD}@${DATABASE_HOST}:${DATABASE_PORT}/${DATABASE_NAME}"

wait-for-it ${DATABASE_HOST}:${DATABASE_PORT} -t 30

>&2 echo 'PostgreSQL is available'

exec "$@"
