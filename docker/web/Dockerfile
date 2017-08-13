FROM python:3
#ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE DeepQueue.settings.docker
RUN mkdir /code
ADD . /code
WORKDIR /code
#RUN mkdir -p /var/www/static/
#RUN touch /var/www/static/nginx_error.log
#RUN touch /var/www/static/nginx_access.log
#RUN chmod -R 755 /var/www
# RUN ls -la
RUN pip install -r requirements.txt
RUN chmod 755 setup.sh
RUN python manage.py collectstatic --noinput


#ENV DJANGO_DEBUG "True"
