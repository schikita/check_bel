.PHONY: dev prod down superuser

DEV_ENV = -f docker-compose.yml -f docker-compose.dev.yml
PROD_ENV = -f docker-compose.yml

prod:
	docker compose $(PROD_ENV) up -d --build

dev:
	docker compose $(DEV_ENV) up -d --build

down:
	docker compose $(DEV_ENV) down