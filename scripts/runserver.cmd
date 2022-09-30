docker-compose build
docker-compose up -d db
docker-compose run --rm app sh -c "ping -w60 db"
docker-compose up