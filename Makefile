PYTHON ?= python

.PHONY: install lint test typecheck format check run

install:
	poetry install

lint:
	poetry run ruff check .

test:
	poetry run pytest

typecheck:
	poetry run mypy src tests

format:
	poetry run ruff format .

check: lint test typecheck

run:
	poetry run uvicorn graphops_ai.api:app --reload