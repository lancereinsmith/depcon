# Installation

## uv (recommended)

```bash
uv tool install depcon
# or: uvx depcon | uv add depcon
```

## pipx

```bash
pipx install depcon
# pipx upgrade depcon | pipx run depcon
```

## pip

```bash
pip install depcon
```

## From source

```bash
git clone https://github.com/lancereinsmith/depcon.git && cd depcon
uv sync
# or: pip install -e .
```

## Dependency groups

depcon uses PEP 735 dependency groups for development:

- **dev**: ruff, ty, rumdl (includes test group)
- **test**: pytest, pytest-cov, pytest-mock
- **docs**: mkdocs, mkdocs-material, mkdocstrings

Install all dev dependencies: `uv sync` (installs all default groups).

## Requirements

Python >=3.12. `uv`, `pip`, or `pipx` for installation.
