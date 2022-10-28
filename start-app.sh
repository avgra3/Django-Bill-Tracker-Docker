#!/bin/bash

# Uncomment if encountering errors
# docker-compose up --force-recreate --remove-orphans --abort-on-container-exit --always-recreate-deps

# Runs commands in the background
docker-compose build --no-cache
#docker-compose up -d --force-recreate
docker-compose up --force-recreate  --always-recreate-deps