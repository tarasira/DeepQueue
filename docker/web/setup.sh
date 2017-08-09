#!/bin/bash

#echo "yes" | python manage.py reset_db
python manage.py makemigrations
python manage.py migrate
python manage.py shell < create_superuser.py