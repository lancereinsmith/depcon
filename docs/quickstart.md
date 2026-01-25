# Quick Start

## Basic conversion

```bash
depcon convert -r requirements.txt
```

Creates or updates `pyproject.toml` with dependency groups and backs up an existing file.

## Multiple files

```bash
depcon convert \
  -r requirements.txt \
  -d requirements-dev.txt \
  -t requirements-test.txt \
  --docs-requirements requirements-docs.txt \
  --project-name "my-project" \
  --project-description "Short description"
```

## View and validate

```bash
depcon show                 # table (default); --format json|yaml
depcon show --group dev
depcon validate
depcon validate --group dev
```

## Typical workflow

```bash
depcon convert -r requirements.txt -d requirements-dev.txt -t requirements-test.txt --project-name my-project --verbose
# review pyproject.toml, then:
depcon validate && uv sync && uv build
```

See [User Guide](user_guide.md) and [Examples](examples.md) for more.
