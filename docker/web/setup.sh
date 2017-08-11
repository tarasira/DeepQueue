#!/bin/bash

#echo "yes" | python manage.py reset_db
python manage.py makemigrations
python manage.py migrate
python manage.py shell < init_db.py
