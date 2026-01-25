# depcon

[![PyPI version](https://img.shields.io/pypi/v/depcon.svg)](https://pypi.org/project/depcon/)
[![Python versions](https://img.shields.io/pypi/pyversions/depcon.svg)](https://pypi.org/project/depcon/)
[![License](https://img.shields.io/github/license/lancereinsmith/depcon.svg)](https://github.com/lancereinsmith/depcon/blob/master/LICENSE)
[![CI Status](https://img.shields.io/github/actions/workflow/status/lancereinsmith/depcon/ci.yml)](https://github.com/lancereinsmith/depcon/actions)

Converts `requirements.txt` to `pyproject.toml` (PEP 621). Groups dependencies into main, dev, test, and docs; supports hatchling, setuptools, and poetry; integrates with uv and hatch.

## Quick Start

```bash
uv tool install depcon
depcon convert -r requirements.txt
```

For multiple files: `depcon convert -r requirements.txt -d requirements-dev.txt -t requirements-test.txt`. See [Installation](installation.md) and [Quick Start](quickstart.md).
