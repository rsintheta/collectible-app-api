FROM python:3.7-alpine
MAINTAINER Glenn Lusk

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /collectible-app
WORKDIR /collectible-app
COPY ./collectible-app /collectible-app

RUN mkdir -p /volume/web/media
RUN mkdir -p /volume/web/static
RUN adduser -D user
RUN chown -R user:user /volume/
RUN chmod -R 755 /volume/web
USER user
