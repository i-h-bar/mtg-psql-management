.PHONY: run pull

setup_local:
	@pre-commit install
	@pre-commit install --hook-type pre-commit --hook-type pre-push

start_docker:
	@sudo systemctl start docker

test:
	@uv run coverage run
	@uv run coverage report

lint:
	@uv run ruff check --fix
	@uv run ty check src

run:
	@uv sync && cd src && uv run main.py

pull:
	@git pull

cron: pull run
