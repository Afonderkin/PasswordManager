#!/bin/bash

case "$1" in
  up)
    docker-compose -f docker-composes/db.yaml -f docker-composes/app.yaml up --build
    ;;
  down)
    docker-compose -f docker-composes/db.yaml -f docker-composes/app.yaml down
    ;;
  stop)
    docker-compose -f docker-composes/db.yaml -f docker-composes/app.yaml stop
    ;;
  start)
    docker-compose -f docker-composes/db.yaml -f docker-composes/app.yaml start
    ;;
  logs)
    docker-compose -f docker-composes/db.yaml -f docker-composes/app.yaml logs -f
    ;;
  migrate)
    docker exec -it django_app python manage.py migrate
    ;;
  createsuperuser)
    docker exec -it django_app python manage.py createsuperuser
    ;;
  shell)
    docker exec -it django_app /bin/sh
    ;;
  *)
    echo "Использование: $0 {up|down|stop|start|logs|migrate|createsuperuser|shell}"
    exit 1
    ;;
esac