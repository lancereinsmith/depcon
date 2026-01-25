# User Guide

Reference for depcon commands and options.

## Commands

depcon provides several commands:

- [convert](#convert-command) — Convert requirements files to pyproject.toml
- [show](#show-command) — Display dependencies from pyproject.toml
- [validate](#validate-command) — Validate pyproject.toml dependencies
- [list](#list-command) — List all dependency groups
- [check](#check-command) — Check for common issues
- **export** — Export dependencies to requirements.txt
- **diff** — Show differences between files
- **sync** — Sync dependencies to requirements files

## Convert {#convert-command}

Converts requirements files to pyproject.toml.

```bash
depcon convert -r requirements.txt
```

### Options

#### Requirements Files

- `-r, --requirements PATH`: Main requirements files (requirements.txt, requirements.in)
- `-d, --dev-requirements PATH`: Development requirements files
- `-t, --test-requirements PATH`: Test requirements files
- `--docs-requirements PATH`: Documentation requirements files

#### Output Options

- `-o, --output PATH`: Output pyproject.toml file path (default: pyproject.toml)
- `--append / --no-append`: Append to existing dependencies instead of replacing
- `--backup / --no-backup`: Create backup of existing pyproject.toml

#### Processing Options

- `--resolve / --no-resolve`: Resolve and pin dependency versions
- `--sort / --no-sort`: Sort dependencies alphabetically

#### Build Backend Options

- `--build-backend [hatchling|setuptools|poetry]`: Build backend to use

#### Group Configuration

- `--dev-group TEXT`: Name for development dependencies group (default: dev)
- `--test-group TEXT`: Name for test dependencies group (default: test)
- `--docs-group TEXT`: Name for documentation dependencies group (default: docs)

#### Project Metadata

- `--project-name TEXT`: Project name (if creating new pyproject.toml)
- `--project-version TEXT`: Project version (if creating new pyproject.toml)
- `--project-description TEXT`: Project description (if creating new pyproject.toml)
- `--python-version TEXT`: Python version requirement (default: >=3.11)
- `--use-optional-deps / --use-dependency-groups`: Use optional-dependencies (PEP 621 extras) instead of dependency-groups (PEP 735)
- `--remove-duplicates / --keep-duplicates`: Remove duplicate dependencies across groups (default: remove)
- `--strict / --no-strict`: Strict mode: fail on parsing errors instead of warning

#### General Options

- `-v, --verbose`: Enable verbose output
- `--help`: Show help message

```bash
depcon convert -r requirements.txt
depcon convert -r requirements.txt -d requirements-dev.txt -t requirements-test.txt
depcon convert -r requirements.txt --project-name "x" --project-description "..." --append
```

## Show {#show-command}

`-f, --file PATH` (default: pyproject.toml); `--format [table|json|yaml]`; `--group TEXT`.

```bash
depcon show
depcon show --format json
depcon show -f my-project.toml
```

## Validate {#validate-command}

`-f, --file`; `--group TEXT`; `--check-pypi / --no-check-pypi`.

```bash
depcon validate
depcon validate --group dev
```

## List {#list-command}

`-f, --file`. Lists dependency groups.

```bash
depcon list
```

## Check {#check-command}

`-f, --file`; `--check-duplicates`; `--check-missing`. Finds duplicates and other issues.

```bash
depcon check
```

## Dependency grouping

- **Main:** Runtime deps (frameworks, data libs, HTTP, DB drivers, etc.)
- **Dev:** Formatters, linters, type checkers, pytest, pre-commit, build tools
- **Test:** pytest, coverage, mocks, benchmarks
- **Docs:** mkdocs, sphinx, themes

## File formats

Any filename. Supported: `requirements.txt`, `requirements.in`, `requirements-*.txt`.

Requirement specs: version (`>=2.25.0,<3.0.0`), extras (`requests[security]`), URLs (`git+https://...`), local paths, `-e` editable, environment markers.

## Build backends

`--build-backend [hatchling|setuptools|poetry]`. Default: hatchling.

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Setuptools: `requires = ["setuptools>=61.0", "wheel"]`, `build-backend = "setuptools.build_meta"`. Poetry: `poetry-core`, `poetry.core.masonry.api`.

## Tool integration

Output uses `[dependency-groups]` for uv. For hatch: `[tool.hatch.build.targets.wheel]` with `packages = ["src"]`.

## Troubleshooting

- **Invalid version specifiers:** `depcon convert -r requirements.txt --verbose` to locate; fix the line and re-run.
- **Resolution failures:** `--no-resolve`, or install first then convert with `--resolve`.
- **File not found:** Use correct path; `ls requirements*.txt` to confirm.

`depcon --help`, `depcon convert --help`, etc.
