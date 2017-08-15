echo yes | python manage.py reset_db
python manage.py makemigrations
python manage.py makemigrations grader
python manage.py migrate
python manage.py shell < init_db.py
python manage.py runserver 0.0.0.0:8000
