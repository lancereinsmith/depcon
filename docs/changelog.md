# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.6.0] - 2026-02-24

### Added

- `parse_dep_string()` public helper in `generators` module for parsing PEP 621 dependency strings into `DependencySpec` objects.
- `DependencyGroup.include_groups` field for PEP 735 `include-group` support. Dependency groups can now reference other groups (e.g., dev includes test).
- Full PEP 735 `include-group` round-trip: loading, generating, and writing `{include-group = "..."}` entries in `[dependency-groups]`.
- `test_generators.py` with 23 tests covering TOML generation, PEP 639 license handling, PEP 735 include-group support, file I/O, backup creation, config loading, and round-trip integrity.

### Changed

- **PEP 639 license format**: License is now emitted as a simple SPDX string (`license = "MIT"`) instead of the legacy table format (`[project.license] text = "MIT"`). Old-format files are normalized on load.
- **Default Python version**: Changed from `>=3.8` / `>=3.11` to `>=3.12` across models, CLI, and generated output. Python 3.11 and earlier are EOL.
- **Removed `tomli` dependency**: Since Python >=3.12 is required, the stdlib `tomllib` is always available for TOML reading. Only `tomli-w` is needed for writing.
- **Classifiers updated**: Removed Python 3.11 classifier (not supported), added Python 3.14.
- **`_load_existing_config()` renamed to `load_config()`**: Now a public method on `PyProjectUpdater` instead of a private one.
- **`to_pep621_string()` now differs from `to_string()`**: PEP 621 output omits editable flags (`-e`) and local paths which are not valid in pyproject.toml dependency specifiers.
- **Logging replaces `print()`**: Parsers and generators now use `logging` module instead of bare `print()` calls.
- **Makefile modernized**: `lint` uses `ruff check` + `ruff format --check` (was black). `format` uses `ruff format` (was black). `type-check` uses `ty check` (was mypy). All commands use `uv run` and `uv sync`.
- **Pre-commit config rewritten**: Removed black, isort, mypy, flake8, django-upgrade, pyupgrade, yesqa, prettier, commitizen, bandit, safety, and broken local hooks. Now uses only pre-commit-hooks v5, ruff v0.14, and codespell v2.4.
- **Authors format**: Changed from `[[project.authors]]` table to inline `authors = [{...}]` syntax.

### Removed

- Dead TOML library fallback chains in generators (tried `tomli_w` -> `toml` -> manual writer, and `tomllib` -> `tomli` -> `toml`). Since Python >=3.12, `tomllib` is always available.
- `_write_toml_manually()` method (~85 lines of dead code) from `PyProjectGenerator`.
- Automatic empty `[tool.uv]` table generation (uv reads `[dependency-groups]` natively).
- Automatic `[tool.hatch.build]` with hardcoded `packages = ["src"]` (wrong for non-src layouts).

## [0.5.0] - 2026-01-24

### Added

- MkDocs-based documentation (mkdocs, mkdocs-material, mkdocstrings). API reference via mkdocstrings.
- Doc pages: code_of_conduct, contributors, development, workflows (reference for `.github/workflows/`). Content from root `CODE_OF_CONDUCT.md`, `CONTRIBUTORS.md`, and `DEVELOPMENT.md` merged into docs; those files removed.
- `[tool.uv]` `default-groups = ["dev", "test", "docs"]` in `pyproject.toml`.

### Changed

- **Version: single source of truth in pyproject.toml** — Version is read only from `pyproject.toml`. `_version.py` uses `importlib.metadata` when installed, or reads `pyproject.toml` from source. Removed hardcoded `__version__` from `__init__.py`. CLI and `depcon.__version__` both derive from this.
- **Documentation: Sphinx -> MkDocs** — All docs converted from RST to Markdown. `docs` dependency group: Sphinx deps replaced with mkdocs, mkdocs-material, mkdocstrings, pymdown-extensions. `[tool.rumdl]` flavor set to `mkdocs`. Makefile: `docs` / `docs-serve` / `docs-clean` use mkdocs and `site/`. GitHub docs workflow: `mkdocs build`, publish `site/` to GitHub Pages.
- Docs trimmed: redundancy, novice-oriented content, and marketing removed; Code of Conduct shortened. Release/contributing docs: version only in `pyproject.toml`.

### Fixed

- Ruff lint: B007, N806, SIM102, W293, N805 (Pydantic `@field_validator` `cls`), B904 (`raise ... from` in parsers).

## [0.4.1] - 2025-12-08

### Fixed

- Fixed broken LICENSE link in documentation
- Fixed GitHub Actions workflows to use dependency-groups correctly
- Improved dependency group nesting using PEP 735 `include-group` syntax

## [0.4.0] - 2025-12-08

### Added

- New `list` command to list all dependency groups in pyproject.toml
- New `check` command to check for common issues (duplicates, missing dependencies)
- Enhanced `convert` command with `--use-optional-deps` flag to choose between dependency-groups (PEP 735) and optional-dependencies (PEP 621 extras)
- Enhanced `convert` command with `--remove-duplicates` flag to automatically remove duplicate dependencies
- Enhanced `convert` command with `--strict` flag for strict error handling
- Enhanced `show` command with `--group` option to filter by specific dependency group
- Enhanced `validate` command with `--check-pypi` flag to verify packages exist on PyPI
- Improved duplicate dependency detection and removal
- Better error messages and validation output
- Default Python version requirement updated to >=3.11

### Changed

- Default Python version requirement changed from >=3.8 to >=3.11 to align with modern standards
- Improved handling of dependency-groups vs optional-dependencies
- Enhanced CLI help text and error messages
- Better integration with uv and modern Python packaging tools

### Fixed

- Fixed duplicate dependency handling across groups
- Improved error handling in various commands
- Better validation of dependency specifications

## [0.3.0] - 2025-12-08

### Added

- Full PEP 735 support for dependency-groups
- New `export` command to export dependencies to requirements.txt format
- New `diff` command to compare dependencies between pyproject.toml and requirements files
- New `sync` command to sync dependencies from pyproject.toml to requirements files
- Enhanced `show` command to display both dependency-groups and optional-dependencies
- Support for distinguishing between dependency-groups (PEP 735) and optional-dependencies (PEP 621 extras)
- Improved validation for both dependency types
- Comprehensive tests for new CLI features

### Changed

- Properly distinguish between dependency-groups (PEP 735) and optional-dependencies (PEP 621)
- Development dependencies now use dependency-groups by default for better uv compatibility
- Updated documentation to reflect latest PEP standards
- Improved error messages and validation output
- Enhanced CLI help text and examples

### Fixed

- Fixed handling of dependency-groups vs optional-dependencies in pyproject.toml
- Improved parsing of both dependency types from existing pyproject.toml files

## [0.2.1] - 2025-10-15

### Added

- Initial release of depcon
- Full PEP 621 support
- Intelligent dependency grouping
- Rich CLI interface
- Multiple build backend support
- Tool integration (uv, hatch, poetry)
- Advanced validation
- Comprehensive test suite

## [0.2.0] - 2025-10-15

### Added

- Complete rewrite with modern architecture
- Full PEP 621 support
- Intelligent dependency grouping
- Rich CLI interface
- Advanced validation
- Multiple build backend support
- Tool integration (uv, hatch, poetry)

### Changed

- Modernized codebase
- Improved error handling
- Enhanced user experience

## [0.1.x] - 2024-12-12

### Added

- Basic requirements.txt to pyproject.toml conversion
- Limited feature set

### Changed

- Initial implementation
