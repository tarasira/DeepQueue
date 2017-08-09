FROM python:3
#ENV PYTHONUNBUFFERED 1
RUN mkdir /code
ADD . /code
WORKDIR /code
RUN mkdir -p /var/www/static/
RUN touch /var/www/DeepQueue.log
RUN chmod -R 755 /var/www
RUN ls -la
RUN pip install -r requirements.txt
RUN chmod 755 setup.sh
RUN python manage.py collectstatic --noinput


#ENV DJANGO_DEBUG "True"