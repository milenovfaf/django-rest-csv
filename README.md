

docker-compose up
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

http://127.0.0.1:8000/api/deals/




