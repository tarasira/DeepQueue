echo yes | ./manage.py reset_db 
./manage.py makemigrations
./manage.py migrate
./manage.py shell < init_db.py
./manage.py runserver 0.0.0.0:8000