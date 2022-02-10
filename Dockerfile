ARG PROJECT_NAME
FROM alpine:3.14
ARG PROJECT_NAME
MAINTAINER Glenn Lusk

ENV PYTHONUNBUFFERED 1

# ensure local python is preferred over distribution python
# ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
# ENV LANG C.UTF-8

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache python3-dev py3-pip python2 py-pip curl
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /$PROJECT_NAME
WORKDIR /$PROJECT_NAME
COPY ./$PROJECT_NAME /$PROJECT_NAME

RUN mkdir -p /volume/web/media
RUN mkdir -p /volume/web/static
RUN adduser -D user
RUN chown -R user:user /volume/
RUN chmod -R 755 /volume/web
USER user
