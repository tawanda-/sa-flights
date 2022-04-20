#!/bin/sh
rm db.sqlite3
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
./manage.py makemigrations
./manage.py migrate
./manage.py loaddata airports.json
./manage.py loaddata aircrafts.json
./manage.py createsuperuser
./manage.py runserver