 FROM python:3
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code/web
 ADD requirements.txt /code/web
 RUN pip install -r requirements.txt
 ADD . /code/