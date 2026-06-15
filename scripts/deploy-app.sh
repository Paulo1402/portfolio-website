#!/usr/bin/env bash

set -euo pipefail

docker compose --env-file .env.cicd pull
docker compose --env-file .env.cicd up -d

docker compose --env-file .env.cicd exec -T django python manage.py migrate --noinput
docker compose --env-file .env.cicd exec -T django python manage.py compilemessages
docker compose --env-file .env.cicd exec -T django python manage.py collectstatic --noinput
