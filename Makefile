.PHONY: up stop shell clean-docker

up:
	docker-compose up -d && docker-compose logs -f app

stop:
	docker-compose stop

shell:
	docker exec -ti app1 bash

clean-docker:
	docker system prune --all --volumes