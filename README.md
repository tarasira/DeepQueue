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

# Run start project
```sh
#docker-compose run [service_name] [command with args] [current_directory]
docker-compose run web django-admin.py startproject Deepqueue ./web
```

# note
* To start the Django project```docker-compose run web django-admin.py startproject Deepqueue ./web```
* To remove some directory ```docker-compose run web rm -rf some_dir .```
* To execute Python kernel ```docker-compose run web python3```
