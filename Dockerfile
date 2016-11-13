FROM python:2.7-slim

RUN apt-get update && apt-get install -y \
                gcc \
                gettext \
                mysql-client libmysqlclient-dev \
                postgresql-client libpq-dev \
                sqlite3 \
        --no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN mkdir /files/

ENV DJANGO_VERSION 1.10.1
ENV P2P_FILE_DIR /files/

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/jpoirier55/docker_p2p

RUN pip install requests mysqlclient psycopg2 django=="$DJANGO_VERSION"

RUN python /docker_p2p/manage.py makemigrations
RUN python /docker_p2p/manage.py migrate

RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('jpoirier', '', 'pw')" | python /docker_p2p/manage.py shell
