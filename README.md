# DeepQueue

# Docker CE setup
[ref](https://docs.docker.com/engine/reference/commandline/run/#capture-container-id-cidfile)
* replace 'your-user' with the system user account
```sh
  curl -fsSL get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  sudo usermod -aG docker your-user
```
# Docker compose
[ref](https://docs.docker.com/compose/django/#create-a-django-project)
* The demo in ref is used in this script
* ```Dockerfile```
```sh
  FROM python:3
  ENV PYTHONUNBUFFERED 1
  RUN mkdir /code
  WORKDIR /code
  ADD requirements.txt /code/
  RUN pip install -r requirements.txt
  ADD . /code/
```
* ```requirements.txt```
```sh
  Django>=1.8,<2.0
  psycopg2
```
* ```docker-compose.yml```
```sh
version: '3'

services:
  db:
    image: postgres
  web:
    build: .
    command: python3 manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    depends_on:
      - db
```


# Run start project
```sh
#docker-compose run [service_name] [command with args] [current_directory]
docker-compose run web django-admin.py startproject Deepqueue ./web
```
```sh
.
├── docker-compose.yml
└── web
    ├── Deepqueue
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── Dockerfile
    ├── manage.py
    └── requirements.txt

```

# Connect DB
* in setting.py
```python
ALLOWED_HOSTS = ['*']
...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
```
# note
* To change owner of the current directory ```sudo chown -R $USER:$USER .```
* To execute Python kernel ```docker-compose run web python3```
* To start the Django project```docker-compose run web django-admin.py startproject Deepqueue ./web```
* To start bash```docker-compose run web bash```
* To reset db ```python manage.py reset_db``` 