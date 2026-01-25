# Contributing

[Code of Conduct](code_of_conduct.md) applies. For setup, testing, and tooling, see the [Development Guide](development.md).

## Setup

Fork, clone, then: `uv pip install -e ".[dev]"` and `pre-commit install`. Run `pytest` and `pre-commit run --all-files` before pushing.

## Pull requests

1. Branch from main, make changes, add tests.
2. Ensure tests pass, lint is clean, docs updated.
3. Push, open a PR, link related issues.

**PR template:** Description; type (bug fix / feature / docs / …); confirm tests pass and docs/changelog updated if needed.

## Issues

**Bugs:** Python and depcon versions, OS, steps to reproduce, expected vs actual, logs.

**Features:** Use case, proposed approach, alternatives.

## Project layout

- **models** — Data structures and validation
- **parsers** — Requirements file parsing
- **generators** — pyproject.toml generation
- **cli** — Commands

## Adding features

Design, update models if needed, implement parsing/generation, add CLI, add tests, update docs.

## Backward compatibility

Prefer backward compatibility; use deprecation warnings and documented migration for breaking changes.

## Release

Maintainers: version in `pyproject.toml`, changelog, tag, publish. See [Development Guide](development.md#release-process).

---

[Development](development.md) · [Contributors](contributors.md) · [Code of Conduct](code_of_conduct.md)
