FROM python:3.9-alpine

LABEL org.opencontainers.image.authors="Above Average Design Ltd"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

RUN pip install --upgrade pip

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY ./app /app
WORKDIR /app

RUN apk del build-deps

COPY ./entrypoint.sh /

ENTRYPOINT [ "sh", "/entrypoint.sh" ]
