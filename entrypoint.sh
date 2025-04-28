#!/bin/sh
# entrypoint.sh
set -e

# Variables de entorno esperadas:
# DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

echo "⏳ Waiting for database at $DB_HOST..."
until mysqladmin ping -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASSWORD" --silent; do
  sleep 2
done

echo "✅ Database is up – running migrations"
python manage.py migrate --noinput

echo "✅ Collecting static files"
python manage.py collectstatic --noinput

# Finalmente ejecutar el CMD de la imagen
exec "$@"
