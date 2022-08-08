#!/bin/bash

LOCAL_DIR=$(PWD)
ROOT_DIR=${LOCAL_DIR}/../..



#source ${LOCAL_DIR}/dev.env

#python3 ${ROOT_DIR}/django/manage.py runserver

#docker-compose up -d --build

#docker-compose logs -f


#docker-compose exec django python django/manage.py migrate --noinput


#docker-compose exec django python django/manage.py migrate --noinput

docker-compose exec  web django-admin startproject api


