COMPOSE = docker compose
SERVICE = web


up:
	$(COMPOSE) up

up-watch:
	$(COMPOSE) up --watch

up-build:
	$(COMPOSE) up --build


build:
	$(COMPOSE) build

up-d:
	$(COMPOSE) up -d

enter:
# 	$(COMPOSE) exec $(SERVICE) bash
	docker exec -it flask_events_api bash


down:
	$(COMPOSE) down

down-v:
	${COMPOSE} down -v

upgrade:
	${COMPOSE} exec ${SERVICE} flask db upgrade
