FROM python:3.8-alpine

LABEL Description="SORTDRU"
MAINTAINER noors <jackmovies01@gmail.com>

ARG BACKEND_WEB_PORT

WORKDIR /opt/app
COPY . .

RUN apk update && \
    apk add --no-cache \
    build-base \
    postgresql-dev musl-dev \
    postgresql-client \
    py3-pillow libxslt-dev \
    postgresql-libs libffi-dev \
    zlib-dev jpeg-dev gettext \
    libffi-dev openssl-dev gcc \
    libc-dev make py3-pip python3-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod +x /opt/app/entrypoint.sh

EXPOSE $BACKEND_WEB_PORT

ENTRYPOINT ["/opt/app/entrypoint.sh"]
