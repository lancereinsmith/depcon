"""Convert Python requirements files to pyproject.toml format.

This module provides functionality to convert traditional requirements.txt and
requirements-dev.txt files into the newer pyproject.toml format. It supports
both regular dependencies and development dependencies, preserving version
specifications.

Features:
    - Parse requirements.txt files and convert to pyproject.toml format
    - Handle both regular and development dependencies
    - Preserve existing pyproject.toml content when updating
    - Create new pyproject.toml file if none exists
    - Support for version specifications in requirements

Usage:
    depconvert -r requirements.txt -d requirements-dev.txt -p pyproject.toml
"""

import argparse
from pathlib import Path
from typing import Optional

import requirements
import toml


def get_version():
    """Read version from pyproject.toml."""
    try:
        data = toml.load(Path("pyproject.toml"))
        return data["project"]["version"]
    except (FileNotFoundError, KeyError):
        return "0.1.0"  # fallback version


__version__ = get_version()


def parse_requirements(file_path: Path) -> list[str]:
    """Parse a requirements file and return a list of dependencies."""
    if not file_path.exists():
        return []

    dependencies = []
    for requirement in requirements.parse(file_path.read_text()):
        name = requirement.name
        if len(requirement.specs) > 0:
            specs = [
                f"{conditional}{version}" for conditional, version in requirement.specs
            ]
            dependencies.append(f"{name}{','.join(specs)}")
        else:
            dependencies.append(name)
    return dependencies


def update_pyproject_toml(
    requirements_path: Optional[Path] = None,
    requirements_dev_path: Optional[Path] = None,
    pyproject_path: Path = Path("pyproject.toml"),
) -> None:
    """Update pyproject.toml with dependencies from requirements files."""

    # Read existing pyproject.toml or create default structure
    if pyproject_path.exists():
        data = toml.load(pyproject_path)
    else:
        data = {
            "project": {
                "name": "project-name",
                "version": "0.1.0",
                "description": "project description",
                "readme": "README.md",
                "requires-python": ">=3.11",
                "dependencies": [],
            },
            "tool": {"uv": {"dev-dependencies": []}},
        }

    # Ensure required sections exist
    if "project" not in data:
        data["project"] = {
            "name": "project-name",
            "version": "0.1.0",
            "description": "project description",
            "readme": "README.md",
            "requires-python": ">=3.11",
            "dependencies": [],
        }
    if "tool" not in data:
        data["tool"] = {"uv": {"dev-dependencies": []}}
    if "uv" not in data["tool"]:
        data["tool"]["uv"] = {"dev-dependencies": []}

    # Update dependencies if requirements file is provided
    if requirements_path:
        dependencies = parse_requirements(requirements_path)
        data["project"]["dependencies"] = dependencies

    # Update dev dependencies if requirements-dev file is provided
    if requirements_dev_path:
        dev_dependencies = parse_requirements(requirements_dev_path)
        data["tool"]["uv"]["dev-dependencies"] = dev_dependencies

    # Write updated content back to pyproject.toml
    toml.dump(data, open(pyproject_path, "w"))


def main():
    parser = argparse.ArgumentParser(
        description="Convert requirements files to pyproject.toml format"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show program's version number and exit",
    )
    parser.add_argument(
        "-r",
        "--requirements",
        type=Path,
        help="Path to requirements.txt or requirements.in",
    )
    parser.add_argument(
        "-d",
        "--requirements-dev",
        type=Path,
        help="Path to requirements-dev.txt or dev-requirements.in",
    )
    parser.add_argument(
        "-p",
        "--pyproject",
        type=Path,
        default=Path("pyproject.toml"),
        help="Path to pyproject.toml. Defaults to pyproject.toml and creates it if it doesn't exist.",
    )

    args = parser.parse_args()

    # Show help if no requirements files are specified
    if not args.requirements and not args.requirements_dev:
        parser.print_help()
        return

    update_pyproject_toml(
        requirements_path=args.requirements,
        requirements_dev_path=args.requirements_dev,
        pyproject_path=args.pyproject,
    )

    print(f"\nSuccessfully updated {args.pyproject}")


if __name__ == "__main__":
    main()
