#!/bin/bash

git clone https://github.com/jpoirier55/docker_p2p

cd docker_p2p

python manage.py makemigrations
python manage.py migrate
echo "Creating database user, requires input:"
python manage.py createsuperuser
