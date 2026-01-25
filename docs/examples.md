# Examples

## Basic

### Single file

```bash
# requirements.txt: requests>=2.25.0, numpy>=1.20.0, pandas>=1.3.0
depcon convert -r requirements.txt
```

Produces `pyproject.toml` with `[build-system]` (hatchling) and `[project]` `dependencies = [..]`.

### Multiple files

```bash
# requirements.txt, requirements-dev.txt, requirements-test.txt
depcon convert -r requirements.txt -d requirements-dev.txt -t requirements-test.txt
```

Main deps in `[project]` `dependencies`; dev/test in `[project.optional-dependencies]` or `[dependency-groups]` depending on `--use-optional-deps`.

## More convert options

```bash
# Full metadata
depcon convert -r req.txt -d req-dev.txt -t req-test.txt --docs-requirements req-docs.txt \
  --project-name "x" --project-description "..." --project-version "1.0.0" --python-version ">=3.12"

# Custom group names
depcon convert -r req.txt -d req-dev.txt --dev-group "development" --test-group "testing"

# Other backends
depcon convert -r requirements.txt --build-backend setuptools
depcon convert -r requirements.txt --build-backend poetry

# Append, resolve
depcon convert -r new-req.txt --append
depcon convert -r requirements.in --resolve
```

## Project types

**Django:** `-r requirements.txt -d requirements-dev.txt --project-name "my-django-app"` (typical reqs: Django, psycopg2, redis, celery; dev: pytest, pytest-django, ruff).

**Data science:** add `--docs-requirements requirements-docs.txt` when you have sphinx/mkdocs deps.

**FastAPI:** same pattern; dev often includes pytest-asyncio, httpx.

## CI/CD

### GitHub Actions

```yaml
- uses: actions/checkout@v4
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
- run: pip install uv
- run: uvx depcon convert -r requirements.txt
- run: uv sync
- run: uv run pytest
```

### Docker

```dockerfile
FROM python:3.12-slim
RUN pip install uv
COPY requirements.txt .
RUN uvx depcon convert -r requirements.txt
RUN uv sync
COPY src/ /app/src/
COPY pyproject.toml /app/
WORKDIR /app
CMD ["uv", "run", "python", "-m", "src.main"]
```

## Project layout

```text
my-project/
├── requirements.txt
├── requirements-dev.txt
├── requirements-test.txt
├── requirements-docs.txt
├── pyproject.toml    # generated
└── src/
    └── my_project/
```

Prefer `>=` for minimum versions; avoid `==` unless required.
