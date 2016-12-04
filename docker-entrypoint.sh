#!/usr/bin/env bash

git clone https://github.com/jpoirier55/docker_p2p

python /docker_p2p/manage.py makemigrations
python /docker_p2p/manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'pw')" | python /docker_p2p/manage.py shell

echo "This is the first test file" > /files/testfile.txt

ip=$(ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/')

python /docker_p2p/scripts/server.py --serverip $ip --serverport $TCP_PORT_NUM &
python /docker_p2p/scripts/server2.py --serverip $ip --serverport $TCP_PORT_NUM2 &

python /docker_p2p/manage.py runserver 0.0.0.0:$PORT_NUM