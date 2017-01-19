docker-compose build
docker-compose up -d
docker-compose stop
docker-compose start
docker rm $(docker ps -a -q)
docker rmi $(docker images | grep "^<none>" | awk "{print $3}")