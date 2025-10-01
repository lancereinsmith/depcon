"""Dependency parsing modules for various file formats."""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional, Tuple

from packaging.requirements import Requirement

from .models import DependencySpec


class RequirementsParser:
    """Parser for requirements.txt and requirements.in files."""

    def __init__(self, file_path: Path):
        """Initialize parser with file path."""
        self.file_path = file_path
        self.content = file_path.read_text(encoding="utf-8")

    def parse(self) -> List[DependencySpec]:
        """Parse requirements file and return list of dependencies."""
        dependencies = []

        for line_num, line in enumerate(self.content.splitlines(), 1):
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            # Skip -r and -c directives (we'll handle them separately)
            if line.startswith(("-r ", "-c ")):
                continue

            try:
                dep = self._parse_line(line, line_num)
                if dep:
                    dependencies.append(dep)
            except Exception as e:
                print(
                    f"Warning: Failed to parse line {line_num} in {self.file_path}: {line}"
                )
                print(f"Error: {e}")
                continue

        return dependencies

    def _parse_line(self, line: str, line_num: int) -> Optional[DependencySpec]:
        """Parse a single line of requirements."""
        # Handle editable installs
        if line.startswith("-e ") or line.startswith("--editable "):
            return self._parse_editable(line)

        # Handle direct URLs
        if "@" in line and not line.startswith("#"):
            return self._parse_url(line)

        # Handle local paths
        if line.startswith("./") or line.startswith("../") or line.startswith("/"):
            return self._parse_path(line)

        # Handle regular package specifications
        return self._parse_package(line)

    def _parse_editable(self, line: str) -> DependencySpec:
        """Parse editable install specification."""
        # Remove -e or --editable prefix
        line = re.sub(r"^(-e|--editable)\s+", "", line)

        # Check if it's a URL or path
        if "@" in line:
            return self._parse_url(line, editable=True)
        else:
            return self._parse_path(line, editable=True)

    def _parse_url(self, line: str, editable: bool = False) -> DependencySpec:
        """Parse URL-based dependency."""
        if "@" not in line:
            raise ValueError("Invalid URL format")

        package_part, url_part = line.rsplit("@", 1)
        package_part = package_part.strip()
        url_part = url_part.strip()

        # Extract package name and extras
        name, extras = self._extract_name_and_extras(package_part)

        return DependencySpec(name=name, extras=extras, url=url_part, editable=editable)

    def _parse_path(self, line: str, editable: bool = False) -> DependencySpec:
        """Parse local path dependency."""
        # Extract package name and extras from path
        path = line.strip()

        # Try to extract name from setup.py or pyproject.toml in the path
        name = self._extract_name_from_path(Path(path))

        return DependencySpec(name=name, path=path, editable=editable)

    def _parse_package(self, line: str) -> DependencySpec:
        """Parse regular package specification."""
        try:
            req = Requirement(line)
        except Exception as e:
            raise ValueError(f"Invalid package specification: {e}")

        # Extract version specs
        version_specs = []
        if req.specifier:
            for spec in req.specifier:
                version_specs.append(str(spec))

        # Extract markers
        markers = str(req.marker) if req.marker else None

        return DependencySpec(
            name=req.name,
            version_specs=version_specs,
            extras=list(req.extras),
            markers=markers,
        )

    def _extract_name_and_extras(self, package_part: str) -> Tuple[str, List[str]]:
        """Extract package name and extras from package specification."""
        if "[" in package_part and "]" in package_part:
            name_part, extras_part = package_part.split("[", 1)
            name = name_part.strip()
            extras = [e.strip() for e in extras_part.rstrip("]").split(",")]
            return name, extras
        else:
            return package_part.strip(), []

    def _extract_name_from_path(self, path: Path) -> str:
        """Extract package name from local path."""
        # Try to read from pyproject.toml first
        pyproject_path = path / "pyproject.toml"
        if pyproject_path.exists():
            try:
                import tomli

                with open(pyproject_path, "rb") as f:
                    data = tomli.load(f)
                    if "project" in data and "name" in data["project"]:
                        return data["project"]["name"]
            except Exception:
                pass

        # Try to read from setup.py
        setup_path = path / "setup.py"
        if setup_path.exists():
            try:
                content = setup_path.read_text()
                # Simple regex to extract name from setup.py
                match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    return match.group(1)
            except Exception:
                pass

        # Fallback to directory name
        return path.name


class PipToolsParser(RequirementsParser):
    """Parser for pip-tools generated requirements.txt files."""

    def parse(self) -> List[DependencySpec]:
        """Parse pip-tools requirements file."""
        dependencies = []
        current_dep = None

        for line_num, line in enumerate(self.content.splitlines(), 1):
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            # Check if this is a continuation line (starts with spaces)
            if line.startswith(" ") and current_dep:
                # This is a continuation of the previous dependency
                current_dep.version_specs.append(line.strip())
                continue

            # Parse the main dependency line
            try:
                dep = self._parse_line(line, line_num)
                if dep:
                    dependencies.append(dep)
                    current_dep = dep
                else:
                    current_dep = None
            except Exception as e:
                print(
                    f"Warning: Failed to parse line {line_num} in {self.file_path}: {line}"
                )
                print(f"Error: {e}")
                current_dep = None
                continue

        return dependencies


class DependencyResolver:
    """Resolve and pin dependency versions."""

    def __init__(self, requirements_files: List[Path]):
        """Initialize resolver with requirements files."""
        self.requirements_files = requirements_files

    def resolve(self, dependencies: List[DependencySpec]) -> List[DependencySpec]:
        """Resolve and pin dependency versions."""
        # This is a simplified resolver - in a real implementation,
        # you would use pip-tools or similar to resolve dependencies
        resolved = []

        for dep in dependencies:
            if dep.url or dep.path:
                # Don't resolve URLs or local paths
                resolved.append(dep)
            else:
                # For now, just return the original dependency
                # In a real implementation, you would resolve versions here
                resolved.append(dep)

        return resolved

    def get_latest_versions(self, package_names: List[str]) -> dict[str, str]:
        """Get latest versions for package names."""
        # This would typically use PyPI API or similar
        # For now, return empty dict
        return {}


def parse_requirements_file(file_path: Path) -> List[DependencySpec]:
    """Parse a requirements file and return dependencies."""
    if not file_path.exists():
        return []

    # Determine parser type based on file name
    if file_path.name.endswith(".in"):
        parser = RequirementsParser(file_path)
    else:
        # Check if it's a pip-tools generated file
        content = file_path.read_text()
        if "via -r" in content or "via " in content:
            parser = PipToolsParser(file_path)
        else:
            parser = RequirementsParser(file_path)

    return parser.parse()


def group_dependencies_by_type(
    dependencies: List[DependencySpec],
) -> dict[str, List[DependencySpec]]:
    """Group dependencies by type (dev, test, docs, etc.)."""
    groups = {"main": [], "dev": [], "test": [], "docs": []}

    # Common development packages
    dev_packages = {
        "pytest",
        "black",
        "isort",
        "flake8",
        "mypy",
        "ruff",
        "pre-commit",
        "coverage",
        "tox",
        "nox",
        "jupyter",
        "ipython",
        "notebook",
        "jupyterlab",
    }

    test_packages = {
        "pytest-cov",
        "pytest-mock",
        "pytest-xdist",
        "pytest-asyncio",
        "coverage",
        "factory-boy",
        "faker",
        "responses",
        "httpx",
        "aioresponses",
    }

    docs_packages = {
        "sphinx",
        "mkdocs",
        "sphinx-rtd-theme",
        "myst-parser",
        "sphinx-autodoc-typehints",
    }

    for dep in dependencies:
        name = dep.name.lower()
        categorized = False

        # Check test packages first (more specific)
        if name in test_packages:
            groups["test"].append(dep)
            categorized = True

        # Check dev packages (broader category) - pytest is in both
        if name in dev_packages:
            groups["dev"].append(dep)
            categorized = True

        # Check docs packages
        if name in docs_packages:
            groups["docs"].append(dep)
            categorized = True

        # If not categorized, add to main
        if not categorized:
            groups["main"].append(dep)

    # Always return all groups, even if empty
    return groups
