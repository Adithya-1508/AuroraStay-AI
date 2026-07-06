.PHONY: setup lint format test typecheck docker run clean docs coverage

setup:
	uv pip install -e .[dev,test,ml]
	pre-commit install

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy shared tests

test:
	pytest

coverage:
	pytest --cov=shared --cov-report=html

docker:
	docker compose build

run:
	docker compose up -d

clean:
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov mlruns
	find . -type d -name "__pycache__" -exec rm -rf {} +

docs:
	@echo "Generating documentation..."
