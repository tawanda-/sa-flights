#!/bin/sh
rm db.sqlite3
./manage.py migrate
./manage.py loaddata airports.json
./manage.py loaddata aircrafts.json
./manage.py createsuperuser
celery -A myproject  worker -l INFO
./manage.py runserver