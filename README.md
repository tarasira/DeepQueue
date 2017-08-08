# DeepQueue

# Docker CE setup
[ref](https://docs.docker.com/engine/reference/commandline/run/#capture-container-id-cidfile)
$ curl -fsSL get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
$ sudo usermod -aG docker your-user

# Docker compose
[ref](https://docs.docker.com/compose/django/#create-a-django-project)

# Run start project
docker-compose run web django-admin.py startproject Deepqueue ./web

# note
143  docker-compose run web django-admin.py startproject Deepqueue ./web
 144  docker-compose run web rm -rf composeexample .
 145  docker-compose run web python3