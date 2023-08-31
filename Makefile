build-project:
	docker compose build

run-project:
	docker compose up -d

stop-project:
	docker compose down -v