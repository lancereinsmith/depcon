# Contributing

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

## Code of Conduct

### Pledge

We pledge to make participation in this project harassment-free for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Standards

**Expected:** Welcoming and inclusive language; respect for differing views; accepting constructive criticism; empathy.

**Unacceptable:** Sexualized language or imagery; trolling, insults, or personal/political attacks; harassment; publishing others’ private information without permission; other conduct inappropriate in a professional setting.

### Reporting

Report concerns to [info@k2rad.com](mailto:info@k2rad.com) or by [opening an issue](https://github.com/lancereinsmith/depcon/issues). Complaints will be reviewed promptly. Reporter privacy will be respected.

### Attribution

Adapted from the [Contributor Covenant](https://www.contributor-covenant.org/version/2/0/code_of_conduct.html), v2.0.

---

[Development](development.md)
