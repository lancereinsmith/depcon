# Development Guide

## Setup

- Python ≥3.12, Git, uv or pip
- Fork and clone, then:

```bash
uv pip install -e ".[dev]"
pre-commit install
depcon --version && pytest
```

## Tools

- **ruff** — Lint and format
- **ty** — Type checking
- **pre-commit** — Hooks

Run: `pre-commit run --all-files` or individually: `ruff check src/ tests/`, `ruff format src/ tests/`, `ty check`.

## IDE

**VS Code / Cursor:** [Ruff extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff), format on save, `ty check` in terminal. Example `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": { "source.fixAll": "explicit", "source.organizeImports": "explicit" }
  },
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests/"]
}
```

**PyCharm:** Project venv, Ruff as formatter and inspector.

## Code style

PEP 8, type hints, docstrings on public API, small focused functions.

## Testing

```bash
pytest
pytest --cov=depcon
pytest tests/test_models.py
pytest tests/test_models.py::TestDependencySpec::test_basic_dependency
pytest -n auto   # if pytest-xdist
```

Use fixtures for shared data; test success and failure. Coverage: `pytest --cov=depcon --cov-report=html` then `open htmlcov/index.html`.

## Documentation

```bash
uv sync --group docs
uv run mkdocs build
uv run mkdocs serve
```

Write in Markdown with examples; follow the existing structure.

## Git

Branch from main, commit with [conventional commits](https://www.conventionalcommits.org/) (`feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `ci`, `chore`), push and open a PR.

## Release

1. Bump version in `pyproject.toml`
2. Update [changelog](changelog.md)
3. Tag and push
4. Publish to PyPI

Checklist: tests pass, docs/changelog updated, lint and type-check clean.

## Debugging

- **Import errors:** `uv pip install -e ".[dev]"`; inspect `sys.path` if needed
- **Test failures:** `pytest -v -s` or run a single test
- **Lint:** `ruff check src/ --fix` and `ruff format src/`

Use `pdb` or your IDE’s debugger.

## Performance

- **Profiling:** e.g. `line_profiler`, `memory_profiler`
- **Benchmarks:** `pytest-benchmark`, run with `pytest --benchmark-only`

## Resources

- [Python Packaging](https://packaging.python.org/)
- [Pytest](https://docs.pytest.org/)
- [MkDocs](https://www.mkdocs.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Pre-commit](https://pre-commit.com/)
- [Ruff](https://docs.astral.sh/ruff/)

---

[Contributing](contributing.md)
