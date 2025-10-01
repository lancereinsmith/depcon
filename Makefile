.PHONY: help install install-dev test test-cov lint format type-check docs clean build release

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install package in production mode
	uv pip install -e .

install-dev: ## Install package in development mode with all dependencies
	uv pip install -e ".[dev,test,docs]"
	pre-commit install

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=depcon --cov-report=html --cov-report=term-missing

test-fast: ## Run tests without coverage (faster)
	pytest --no-cov

lint: ## Run linting
	ruff check src/ tests/
	black --check src/ tests/

format: ## Format code
	black src/ tests/
	ruff check src/ tests/ --fix

type-check: ## Run type checking
	mypy src/

check: lint type-check test ## Run all checks

docs: ## Build documentation
	cd docs && uv run sphinx-build -b html . _build/html

docs-serve: ## Serve documentation locally
	cd docs && python -m http.server 8000 --directory _build/html

docs-clean: ## Clean documentation build
	cd docs && rm -rf _build/

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: ## Build package
	uv build

build-check: ## Check built package
	uv build
	uv pip install dist/*.whl
	depcon --version

release: ## Release package (requires proper version bumping)
	@echo "Make sure you have:"
	@echo "1. Updated version in pyproject.toml"
	@echo "2. Updated __version__ in __init__.py"
	@echo "3. Updated changelog"
	@echo "4. Committed all changes"
	@echo "5. Created and pushed tag"
	@echo "Then run: uv publish"

dev-setup: install-dev ## Set up development environment
	@echo "Development environment set up!"
	@echo "Run 'make check' to verify everything is working"

ci: ## Run CI checks locally
	pre-commit run --all-files
	pytest --cov=depcon --cov-report=xml

security: ## Run security checks
	safety check
	bandit -r src/

benchmark: ## Run performance benchmarks
	pytest --benchmark-only

profile: ## Profile the code
	python -m cProfile -o profile.stats -m depcon.cli --help
	python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(20)"

update-deps: ## Update dependencies
	uv pip install --upgrade -e ".[dev,test,docs]"

check-deps: ## Check for outdated dependencies
	uv pip list --outdated

install-hooks: ## Install pre-commit hooks
	pre-commit install

update-hooks: ## Update pre-commit hooks
	pre-commit autoupdate

run-hooks: ## Run pre-commit hooks on all files
	pre-commit run --all-files

demo: ## Run demo script
	python examples/demo.py

validate: ## Validate pyproject.toml
	depcon validate

show: ## Show dependencies
	depcon show

convert-example: ## Convert example requirements
	depcon convert -r examples/requirements.txt --verbose

# Development shortcuts
dev: install-dev ## Alias for install-dev
check-all: check ## Alias for check
test-all: test-cov ## Alias for test-cov
format-all: format ## Alias for format
