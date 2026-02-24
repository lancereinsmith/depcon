.PHONY: help install install-dev test test-cov test-fast lint format type-check check docs docs-serve docs-clean clean build build-check release dev-setup ci demo validate show

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install package in production mode
	uv sync --no-dev

install-dev: ## Install package in development mode with all dependencies
	uv sync
	pre-commit install

test: ## Run tests
	uv run pytest

test-cov: ## Run tests with coverage
	uv run pytest --cov=depcon --cov-report=html --cov-report=term-missing

test-fast: ## Run tests without coverage (faster)
	uv run pytest --no-cov

lint: ## Check code style
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/

format: ## Format code
	uv run ruff format src/ tests/
	uv run ruff check --fix src/ tests/

type-check: ## Run type checking
	uv run ty check

check: lint type-check test ## Run all checks

docs: ## Build documentation
	uv run mkdocs build

docs-serve: ## Serve documentation locally
	uv run mkdocs serve

docs-clean: ## Clean documentation build
	rm -rf site/

clean: ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/ .mypy_cache/ .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: ## Build package
	uv build

build-check: ## Build and verify package
	uv build
	uv pip install dist/*.whl
	depcon --version

release: ## Show release instructions
	@echo "Release steps:"
	@echo "1. Update version in pyproject.toml"
	@echo "2. Update changelog"
	@echo "3. Commit all changes"
	@echo "4. Create and push tag: git tag v<version> && git push --tags"
	@echo "5. GitHub Actions will publish to PyPI"

dev-setup: install-dev ## Set up development environment
	@echo "Development environment ready! Run 'make check' to verify."

ci: ## Run CI checks locally
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/
	uv run ty check
	uv run pytest --cov=depcon --cov-report=xml

demo: ## Run demo script
	uv run python examples/demo.py

validate: ## Validate pyproject.toml
	uv run depcon validate

show: ## Show dependencies
	uv run depcon show
