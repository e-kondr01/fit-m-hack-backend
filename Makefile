.PHONY: up
up:
	docker compose up --build

.PHONY: run
run: up

.PHONY: local
local:
	docker compose -f local-docker-compose.yml up -d --build
	cd app; alembic upgrade head; \
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --proxy-headers

.PHONY: migrations
migrations:
	cd app; alembic revision --autogenerate; \
	alembic upgrade head

.PHONY: migrate
migrate:
	cd app; alembic upgrade head

.DEFAULT_GOAL := up
