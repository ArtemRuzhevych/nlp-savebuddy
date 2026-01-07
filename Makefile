.PHONY: build up down logs shell test

build:
	docker-compose up --build

down:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec nlp-api /bin/bash

test:
	docker-compose exec nlp-api pytest tests/
