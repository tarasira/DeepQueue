#!/bin/sh

# to build
# docker build -t tfworker .

#to run
cat test.py | docker run -i tfworker

#cat main.py | docker run -i tfworker
#cat perceptron.py | docker run -i tfworker