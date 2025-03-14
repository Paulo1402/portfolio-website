docker compose down
docker compose up -d --build

docker compose exec django python manage.py migrate
docker compose exec django python manage.py collectstatic --noinput
