FROM python:3.9-alpine
LABEL org.opencontainers.image.authors="Above Average Design Ltd"

ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

COPY app/requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN apk del build-deps

RUN adduser -D user
USER user