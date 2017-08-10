#FROM tutum/nginx
#RUN rm /etc/nginx/sites-enabled/default
#ADD sites-enabled/ /etc/nginx/sites-enabled

FROM nginx
MAINTAINER Wasit Limprasert
#RUN rm /etc/nginx/nginx.conf
COPY ./django_nginx.conf /etc/nginx/conf.d/default.conf