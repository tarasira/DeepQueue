FROM gcr.io/tensorflow/tensorflow:latest
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
ADD *.py /code/
WORKDIR /code
RUN ls -la
ENTRYPOINT ["python", "-", "2>&1"]
