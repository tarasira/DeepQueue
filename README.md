# DeepQueue

# Docker CE setup
[ref](https://docs.docker.com/engine/reference/commandline/run/#capture-container-id-cidfile)
* replace 'your-user' with the system user account
```sh
  curl -fsSL get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  sudo usermod -aG docker your-user
```
or
```sh
curl -sSL https://get.docker.com | sh
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
* Todelete docker image 
```sh
#!/bin/bash
# Delete all containers
docker rm $(docker ps -a -q)
# Delete all images
docker rmi $(docker images -q)
```

# Nvidia Docker
[ref](https://github.com/NVIDIA/nvidia-docker)
```sh
  wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker_1.0.1-1_amd64.deb
  sudo dpkg -i /tmp/nvidia-docker*.deb && rm /tmp/nvidia-docker*.deb
  nvidia-docker run --rm nvidia/cuda nvidia-smi
```
* print tensorflow verions
```sh
nvidia-docker run --rm tensorflow/tensorflow:nightly-devel-gpu python -c 'import tensorflow as tf ; print tf.__version__'
````

or

```sh
nvidia-docker run --rm gcr.io/tensorflow/tensorflow:latest-gpu python -c 'import tensorflow as tf ; print tf.__version__'
```

* excecute addition
````sh
nvidia-docker run --rm tensorflow/tensorflow:nightly-devel-gpu python -c '
import tensorflow as tf;
a=tf.constant(2);
b=tf.constant(3);
c=tf.add(a,b);
with tf.Session() as session:
    result=session.run(c);
    print(result)'
```

# Create container
[ref](https://docs.docker.com/get-started/part2/)
```sh
nvidia-docker build -t tfworker .
nvidia-docker images
nvidia-docker run --rm tfworker
```

#publish
```sh
nvidia-docker login
nvidia-docker tag tfworker wasit7/tfworker:gpu
nvidia-docker images
nvidia-docker push wasit7/tfworker:gpu
```