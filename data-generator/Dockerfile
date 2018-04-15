FROM python:3.6-alpine3.7

ENV LANG en_US.UTF-8
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# install system packages
RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps \
        gcc libc-dev linux-headers postgresql-dev

# install requirements
COPY requirements.txt /usr/src/app/
RUN pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

# install flask app
COPY . /usr/src/app
RUN apk del .build-deps

CMD uwsgi /usr/src/app/uwsgi.ini
