"""Tests for dependency parsers."""

from depcon.models import DependencySpec
from depcon.parsers import group_dependencies_by_type, parse_requirements_file


class TestRequirementsParser:
    """Test requirements file parsing."""

    def test_parse_simple_requirements(self, tmp_path):
        """Test parsing simple requirements.txt."""
        req_file = tmp_path / "requirements.txt"
        req_file.write_text(
            """
requests>=2.25.0
numpy>=1.20.0,<2.0.0
pandas>=1.3.0
"""
        )

        deps = parse_requirements_file(req_file)

        assert len(deps) == 3
        assert deps[0].name == "requests"
        assert deps[0].version_specs == [">=2.25.0"]
        assert deps[1].name == "numpy"
        assert set(deps[1].version_specs) == {">=1.20.0", "<2.0.0"}
        assert deps[2].name == "pandas"
        assert deps[2].version_specs == [">=1.3.0"]

    def test_parse_with_extras(self, tmp_path):
        """Test parsing requirements with extras."""
        req_file = tmp_path / "requirements.txt"
        req_file.write_text("requests[security]>=2.25.0")

        deps = parse_requirements_file(req_file)

        assert len(deps) == 1
        assert deps[0].name == "requests"
        assert deps[0].extras == ["security"]
        assert deps[0].version_specs == [">=2.25.0"]

    def test_parse_with_markers(self, tmp_path):
        """Test parsing requirements with environment markers."""
        req_file = tmp_path / "requirements.txt"
        req_file.write_text("requests>=2.25.0; python_version >= '3.8'")

        deps = parse_requirements_file(req_file)

        assert len(deps) == 1
        assert deps[0].name == "requests"
        assert deps[0].version_specs == [">=2.25.0"]
        assert deps[0].markers == 'python_version >= "3.8"'

    def test_parse_editable_install(self, tmp_path):
        """Test parsing editable installs."""
        req_file = tmp_path / "requirements.txt"
        req_file.write_text("-e ./local-package")

        deps = parse_requirements_file(req_file)

        assert len(deps) == 1
        assert deps[0].name == "local-package"  # Extracted from path
        assert deps[0].path == "./local-package"
        assert deps[0].editable is True

    def test_parse_url_install(self, tmp_path):
        """Test parsing URL installs."""
        req_file = tmp_path / "requirements.txt"
        req_file.write_text(
            "requests @ https://github.com/psf/requests/archive/main.zip"
        )

        deps = parse_requirements_file(req_file)

        assert len(deps) == 1
        assert deps[0].name == "requests"
        assert deps[0].url == "https://github.com/psf/requests/archive/main.zip"

    def test_parse_empty_file(self, tmp_path):
        """Test parsing empty requirements file."""
        req_file = tmp_path / "requirements.txt"
        req_file.write_text("")

        deps = parse_requirements_file(req_file)

        assert len(deps) == 0

    def test_parse_nonexistent_file(self, tmp_path):
        """Test parsing nonexistent file."""
        req_file = tmp_path / "nonexistent.txt"

        deps = parse_requirements_file(req_file)

        assert len(deps) == 0


class TestDependencyGrouping:
    """Test dependency grouping functionality."""

    def test_group_main_dependencies(self):
        """Test grouping main dependencies."""
        deps = [
            DependencySpec(name="requests", version_specs=[">=2.25.0"]),
            DependencySpec(name="numpy", version_specs=[">=1.20.0"]),
            DependencySpec(name="pandas", version_specs=[">=1.3.0"]),
        ]

        grouped = group_dependencies_by_type(deps)

        assert "main" in grouped
        assert len(grouped["main"]) == 3
        assert "dev" in grouped
        assert len(grouped["dev"]) == 0

    def test_group_dev_dependencies(self):
        """Test grouping development dependencies."""
        deps = [
            DependencySpec(name="pytest", version_specs=[">=7.0.0"]),
            DependencySpec(name="black", version_specs=[">=23.0.0"]),
            DependencySpec(name="ruff", version_specs=[">=0.1.0"]),
        ]

        grouped = group_dependencies_by_type(deps)

        assert "dev" in grouped
        assert len(grouped["dev"]) == 3
        assert "main" in grouped
        assert len(grouped["main"]) == 0

    def test_group_test_dependencies(self):
        """Test grouping test dependencies."""
        deps = [
            DependencySpec(name="pytest", version_specs=[">=7.0.0"]),
            DependencySpec(name="pytest-cov", version_specs=[">=4.0.0"]),
            DependencySpec(name="factory-boy", version_specs=[">=3.2.0"]),
        ]

        grouped = group_dependencies_by_type(deps)

        assert "test" in grouped
        assert len(grouped["test"]) == 2  # pytest-cov and factory-boy
        assert "dev" in grouped
        assert len(grouped["dev"]) == 1  # pytest

    def test_group_docs_dependencies(self):
        """Test grouping documentation dependencies."""
        deps = [
            DependencySpec(name="sphinx", version_specs=[">=5.0.0"]),
            DependencySpec(name="sphinx-rtd-theme", version_specs=[">=1.0.0"]),
            DependencySpec(name="myst-parser", version_specs=[">=1.0.0"]),
        ]

        grouped = group_dependencies_by_type(deps)

        assert "docs" in grouped
        assert len(grouped["docs"]) == 3
        assert "main" in grouped
        assert len(grouped["main"]) == 0

    def test_group_mixed_dependencies(self):
        """Test grouping mixed dependencies."""
        deps = [
            DependencySpec(name="requests", version_specs=[">=2.25.0"]),
            DependencySpec(name="pytest", version_specs=[">=7.0.0"]),
            DependencySpec(name="sphinx", version_specs=[">=5.0.0"]),
            DependencySpec(name="factory-boy", version_specs=[">=3.2.0"]),
        ]

        grouped = group_dependencies_by_type(deps)

        assert len(grouped["main"]) == 1  # requests
        assert len(grouped["dev"]) == 1  # pytest
        assert len(grouped["docs"]) == 1  # sphinx
        assert len(grouped["test"]) == 1  # factory-boy
