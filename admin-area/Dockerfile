FROM python:3.6-alpine3.7

ENV LANG en_US.UTF-8
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# install system packages
RUN apk add --no-cache jpeg mailcap postgresql-libs zlib && \
    apk add --no-cache --virtual .build-deps \
        gcc jpeg-dev libc-dev linux-headers postgresql-dev zlib-dev

# install requirements
COPY requirements.txt /usr/src/app/
RUN pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

# install django app
COPY . /usr/src/app
RUN SECRET_KEY=build ./manage.py collectstatic && \
    apk del .build-deps

CMD uwsgi /usr/src/app/uwsgi.ini
