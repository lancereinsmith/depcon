# Examples

## Basic

### Single file

Create a `requirements.txt` with your dependencies, then:

```bash
depcon convert -r requirements.txt
```

You get a `pyproject.toml` with `[build-system]` (hatchling) and `[project]` `dependencies`.

### Multiple files

```bash
depcon convert \
  -r requirements.txt \
  -d requirements-dev.txt \
  -t requirements-test.txt
```

Main deps go in `[project]` `dependencies`; dev and test go in `[project.optional-dependencies]` or `[dependency-groups]` depending on `--use-optional-deps`.

---

## Convert options

### Full metadata

```bash
depcon convert \
  -r requirements.txt \
  -d requirements-dev.txt \
  -t requirements-test.txt \
  --docs-requirements requirements-docs.txt \
  --project-name "my-project" \
  --project-description "Short description" \
  --project-version "1.0.0" \
  --python-version ">=3.12"
```

### Custom group names

```bash
depcon convert -r requirements.txt -d requirements-dev.txt \
  --dev-group "development" --test-group "testing"
```

### Other build backends

```bash
depcon convert -r requirements.txt --build-backend setuptools
depcon convert -r requirements.txt --build-backend poetry
```

### Append and resolve

```bash
depcon convert -r new-requirements.txt --append
depcon convert -r requirements.in --resolve
```

---

## Project types

### Django

Typical: Django, psycopg2, redis, celery in `requirements.txt`; pytest, pytest-django, ruff in `requirements-dev.txt`.

```bash
depcon convert -r requirements.txt -d requirements-dev.txt \
  --project-name "my-django-app" --project-description "A Django app"
```

### Data science

Add `--docs-requirements` when you have sphinx/mkdocs in a separate file:

```bash
depcon convert -r requirements.txt -d requirements-dev.txt \
  --docs-requirements requirements-docs.txt \
  --project-name "data-tool"
```

### FastAPI

Same pattern; dev often includes pytest-asyncio and httpx.

```bash
depcon convert -r requirements.txt -d requirements-dev.txt \
  --project-name "my-api" --project-description "A FastAPI service"
```

---

## CI/CD

### GitHub Actions

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
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

---

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

Use `>=` for minimum versions; avoid `==` unless needed.
