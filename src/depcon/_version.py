"""Version from pyproject.toml (single source of truth)."""

from pathlib import Path


def _get_version() -> str:
    """Read version from installed package metadata or pyproject.toml."""
    try:
        from importlib.metadata import version

        return version("depcon")
    except Exception:
        pass
    # Fallback when not installed: read from pyproject.toml
    import tomllib

    root = Path(__file__).resolve().parent.parent.parent
    with open(root / "pyproject.toml", "rb") as f:
        return tomllib.load(f)["project"]["version"]


__version__ = _get_version()
