#!/bin/bash

if [ "$DATABASE" = "Imodels" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

sleep 2

echo "Apply database migrations"
python3 manage.py makemigrations
python3 manage.py migrate account

# python3 manage.py runserver --insecure 0.0.0.0:8000

exec "$@"