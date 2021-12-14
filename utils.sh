#!/bin/bash


if [ "$1" == "backend" ]; then
	docker exec -it $(docker ps --quiet --filter=name=docker-backend-1) bash
elif [ "$1" == "frontend" ]; then
	docker exec -it $(docker ps --quiet --filter=name=docker-frontend-1) bash
elif [ "$1" == "database" ]; then
	mysql -ufortune_db_user -p -P33060 --protocol=tcp fortune_db
elif [ "$1" == "docker" ]; then
	docker-compose -f .docker/docker-compose.yml up
else
	echo backend, database, docker
fi