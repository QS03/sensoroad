#!/bin/bash

NAME="sensoroad"
DIR=/opt/sensoroad
USER=sensoroad
GROUP=sensoroad
WORKERS=3
BIND=unix:/opt/sensoroad/run/gunicorn.sock
DJANGO_SETTINGS_MODULE=sensoroad.settings.dev
DJANGO_WSGI_MODULE=sensoroad.wsgi
LOG_LEVEL=error

cd $DIR
source ../env/bin/activate

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DIR:$PYTHONPATH

exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $WORKERS \
  --user=$USER \
  --group=$GROUP \
  --bind=$BIND \
  --log-level=$LOG_LEVEL \
  --log-file=-