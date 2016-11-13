#!/bin/bash

python manage.py makemigrations
python manage.py migrate
echo "Creating database user, requires input:"
python manage.py createsuperuser
