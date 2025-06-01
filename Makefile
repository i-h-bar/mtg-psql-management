setup_local:
	@pre-commit install
	@pre-commit install --hook-type pre-commit --hook-type pre-push


start_docker:
	@sudo systemctl start docker

test:
	@uv run coverage run
	@uv run coverage report

lint:
	@uv run ruff check
	@uv run ty check app
