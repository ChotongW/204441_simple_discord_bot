#!/bin/sh


docker compose build --build-arg IMAGE_TAG=chotongw/204441-discord-bot
docker compose -f docker-compose.yml --compatibility up -d