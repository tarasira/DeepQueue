#!/bin/sh

# to build
# nvidia-docker build -t tfworker .

#to run
cat test.py | nvidia-docker run -i tfworker

#cat main.py | nvidia-docker run -i tfworker
#cat perceptron.py | nvidia-docker run -i tfworker