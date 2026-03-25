.PHONY: test lint clean install dev

install:
	pip install .

dev:
	pip install -e ".[dev]"

test:
	PYTHONPATH=src python3 -m pytest tests/ -v --tb=short

coverage:
	PYTHONPATH=src python3 -m pytest tests/ -v --cov=loki --cov-report=term-missing

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache build dist
