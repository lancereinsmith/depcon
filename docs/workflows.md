# GitHub Workflows

Reference for the workflows in `.github/workflows/`.

---

## CI (`ci.yml`)

**Triggers:** Push and pull requests on `master` and `develop`.

**Jobs:**

| Job | Description |
|-----|-------------|
| **test** | Runs on Python 3.11, 3.12, 3.13. Installs with `uv sync --group dev --group test`. Runs `depcon --version` and `--help`, ruff check, black `--check`, mypy, pytest (no coverage), pytest with coverage (XML + term). Uploads `coverage.xml` to Codecov. Lint, format, and type steps use a trailing `|| echo "…"` so they do not fail the job. |
| **build** | After `test`. `uv build`; uploads `dist/` as an artifact. |
| **security** | After `test`. Installs `safety`, runs `safety check` on dependencies. |
| **integration** | After `test`. `uv sync` (no dev/test). Runs `depcon --help`, `convert --help`, `show --help`, `validate --help`. Creates a temp dir with a small `requirements.txt`, runs `depcon convert`, `show`, `validate` on the output, then removes the dir. |

---

## Dependency Review (`dependency-review.yml`)

**Triggers:** Pull requests targeting `master` and `develop`.

**Jobs:**

| Job | Description |
|-----|-------------|
| **dependency-review** | Runs `actions/dependency-review-action`. Comments on the PR with a diff of dependency changes (including known-vulnerable or license issues). |

---

## Documentation (`docs.yml`)

**Triggers:** Push to `master`, pull requests to `master`, and `workflow_dispatch`.

**Jobs:**

| Job | Description |
|-----|-------------|
| **build-docs** | `uv sync --group docs`, `uv run mkdocs build`. Uploads `site/` as the `documentation` artifact. |
| **deploy-docs** | Runs only on **push** to `master` (not on PRs). Downloads the `documentation` artifact into `site/`, then uses `peaceiris/actions-gh-pages` to publish `site/` to GitHub Pages. |
| **docs-preview** | Runs only on **pull_request**. Builds docs with mkdocs (same as `build-docs`). Posts a PR comment: success if `site/index.html` exists, otherwise failure. Success message still says "run `make html`" (legacy; project uses mkdocs). |

---

## Release (`release.yml`)

**Triggers:**

- **Push** to tags matching `v*` (e.g. `v1.0.0`).
- **workflow_dispatch** with required input `version` (e.g. `v1.0.0`).

**Jobs:**

| Job | Description |
|-----|-------------|
| **release** | Checkout (full history). `uv sync --group dev --group test`, `pytest`, `uv build`, `depcon --version`. Creates a GitHub Release with `softprops/action-gh-release`: tag/name from `github.ref_name` (on tag push) or `inputs.version` (on manual run); `draft: false`, `prerelease: false`; attaches `dist/*`. On **push** (tag) only, runs `pypa/gh-action-pypi-publish` to publish `dist/` to PyPI using `secrets.PYPI_API_TOKEN`. |
| **notify** | Runs after `release` with `if: always()`. Prints a success or failure message to the log depending on `needs.release.result`. |

**Secrets:** `PYPI_API_TOKEN` must be set for PyPI publish on tag push.
