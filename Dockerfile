FROM ubuntu:16.04

RUN apt-get update \
	&& apt-get install -y --no-install-recommends python2.7 python-pip python2.7-setuptools python2.7-dev gcc gettext mysql-client libmysqlclient-dev postgresql-client libpq-dev sqlite3 \
	&& rm -rf /var/lib/apt/lists/*

ENV DJANGO_VERSION 1.10

RUN pip install wheel \
	&& pip install mysqlclient psycopg2 django=="$DJANGO_VERSION"

RUN echo 'deb http://ppa.launchpad.net/ansible/ansible/ubuntu xenial main' > /etc/apt/sources.list.d/ansible.list \
	&& apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7BB9C367 \
	&& apt-get update \
	&& apt-get install -y ansible \
	&& mkdir /root/.ssh \
	&& chmod 700 /root/.ssh \
	&& rm -rf /var/lib/apt/lists/*

ARG ANSIBLE_SSH_KEY=${HOME}/.ssh/id_rsa
ARG HOSTS_FILE=hosts_sample
ENV DEST=/usr/src/catstricity-deploy

COPY ${ANSIBLE_SSH_KEY} /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/*
COPY app/ ${DEST}/app/
COPY ansible/ ${DEST}/ansible/
COPY $HOSTS_FILE ${DEST}/hosts_sample
WORKDIR /usr/src/catstricity-deploy/app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

