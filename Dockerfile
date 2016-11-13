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

RUN apt-get update && apt-get install -y git nano

RUN pip install requests mysqlclient psycopg2 django=="$DJANGO_VERSION"

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]