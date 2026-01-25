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
# pip install depcon[dev] | depcon[all]
```

## From source

```bash
git clone https://github.com/lancereinsmith/depcon.git && cd depcon
uv pip install -e ".[dev]"
# or: pip install -e ".[dev]"
```

## Optional dependency groups

- **dev**: ruff, ty, pytest, pre-commit
- **test**: pytest-cov, pytest-mock
- **docs**: mkdocs, mkdocs-material, mkdocstrings
- **all**: all of the above

Example: `uv tool install depcon[dev,docs]`.

## Requirements

Python ≥3.12. `uv`, `pip`, or `pipx` for installation.
