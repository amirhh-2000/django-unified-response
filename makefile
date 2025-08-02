.PHONY: help install install-dev test lint format security clean

help:
    @echo "Available commands:"
    @echo "  install     Install the package"
    @echo "  install-dev Install development dependencies"
    @echo "  test        Run tests"
    @echo "  lint        Run linting checks"
    @echo "  format      Format code"
    @echo "  security    Run security checks"
    @echo "  clean       Clean build artifacts"

install:
    uv pip install .

install-dev:
    uv sync --dev

test:
    uv run pytest --cov=django_unified_response --cov-report=term-missing

lint:
    uv run ruff check .

format:
    uv run ruff format .

security:
    uv run bandit -r django_unified_response
    uv run safety check

clean:
    rm -rf build/
    rm -rf dist/
    rm -rf *.egg-info/
    rm -rf .pytest_cache/
    rm -rf .coverage
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
