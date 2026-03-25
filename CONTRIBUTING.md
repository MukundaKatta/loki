# Contributing to Loki

Thanks for your interest in contributing!

## Development Setup

```bash
git clone https://github.com/MukundaKatta/loki.git
cd loki
pip install -e ".[dev]"
```

## Running Tests

```bash
make test
# or
PYTHONPATH=src python3 -m pytest tests/ -v
```

## Code Style

- Follow PEP 8
- Use type hints for public APIs
- Keep functions focused and under 30 lines where practical

## Pull Requests

1. Fork the repo and create your branch from `main`
2. Add tests for any new functionality
3. Ensure all tests pass before submitting
4. Write a clear PR description

## Adding New Command Patterns

To add support for a new natural language pattern:

1. Add a regex pattern to `_PATTERNS` in `src/loki/parser.py`
2. Add a corresponding `ActionType` variant if needed in `src/loki/core.py`
3. Add a handler method in `ActionExecutor`
4. Write tests in `tests/test_parser.py` and `tests/test_core.py`
