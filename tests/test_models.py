"""Tests for data models."""

from pathlib import Path

import pytest

from depcon.models import (
    ConversionOptions,
    DependencyGroup,
    DependencySpec,
    ProjectConfig,
)


class TestDependencySpec:
    """Test DependencySpec model."""

    def test_basic_dependency(self):
        """Test basic dependency creation."""
        dep = DependencySpec(name="requests", version_specs=[">=2.25.0"])

        assert dep.name == "requests"
        assert dep.version_specs == [">=2.25.0"]
        assert dep.extras == []
        assert dep.url is None
        assert dep.path is None
        assert dep.editable is False
        assert dep.markers is None

    def test_dependency_with_extras(self):
        """Test dependency with extras."""
        dep = DependencySpec(
            name="requests", version_specs=[">=2.25.0"], extras=["security", "socks"]
        )

        assert dep.name == "requests"
        assert dep.extras == ["security", "socks"]

    def test_dependency_with_url(self):
        """Test dependency with URL."""
        dep = DependencySpec(
            name="requests", url="https://github.com/psf/requests/archive/main.zip"
        )

        assert dep.name == "requests"
        assert dep.url == "https://github.com/psf/requests/archive/main.zip"
        assert dep.version_specs == []

    def test_dependency_with_path(self):
        """Test dependency with local path."""
        dep = DependencySpec(
            name="local-package", path="./local-package", editable=True
        )

        assert dep.name == "local-package"
        assert dep.path == "./local-package"
        assert dep.editable is True

    def test_dependency_with_markers(self):
        """Test dependency with environment markers."""
        dep = DependencySpec(
            name="requests",
            version_specs=[">=2.25.0"],
            markers="python_version >= '3.8'",
        )

        assert dep.name == "requests"
        assert dep.markers == "python_version >= '3.8'"

    def test_to_string_basic(self):
        """Test basic string conversion."""
        dep = DependencySpec(name="requests", version_specs=[">=2.25.0"])

        assert dep.to_string() == "requests>=2.25.0"

    def test_to_string_with_extras(self):
        """Test string conversion with extras."""
        dep = DependencySpec(
            name="requests", version_specs=[">=2.25.0"], extras=["security"]
        )

        assert dep.to_string() == "requests[security]>=2.25.0"

    def test_to_string_with_url(self):
        """Test string conversion with URL."""
        dep = DependencySpec(
            name="requests", url="https://github.com/psf/requests/archive/main.zip"
        )

        assert (
            dep.to_string()
            == "requests @ https://github.com/psf/requests/archive/main.zip"
        )

    def test_to_string_with_path(self):
        """Test string conversion with path."""
        dep = DependencySpec(
            name="local-package", path="./local-package", editable=True
        )

        assert dep.to_string() == "-e ./local-package"

    def test_to_string_with_markers(self):
        """Test string conversion with markers."""
        dep = DependencySpec(
            name="requests",
            version_specs=[">=2.25.0"],
            markers="python_version >= '3.8'",
        )

        assert dep.to_string() == "requests>=2.25.0; python_version >= '3.8'"

    def test_validation_empty_name(self):
        """Test validation with empty name."""
        with pytest.raises(ValueError, match="Package name cannot be empty"):
            DependencySpec(name="")

    def test_validation_invalid_version_spec(self):
        """Test validation with invalid version spec."""
        with pytest.raises(ValueError, match="Invalid version spec"):
            DependencySpec(name="requests", version_specs=["invalid"])


class TestDependencyGroup:
    """Test DependencyGroup model."""

    def test_create_group(self):
        """Test creating a dependency group."""
        group = DependencyGroup(name="dev")

        assert group.name == "dev"
        assert group.dependencies == []
        assert group.description is None

    def test_add_dependency(self):
        """Test adding a dependency to a group."""
        group = DependencyGroup(name="dev")
        dep = DependencySpec(name="pytest", version_specs=[">=7.0.0"])

        group.add_dependency(dep)

        assert len(group.dependencies) == 1
        assert group.dependencies[0] == dep

    def test_add_duplicate_dependency(self):
        """Test adding duplicate dependency updates existing."""
        group = DependencyGroup(name="dev")
        dep1 = DependencySpec(name="pytest", version_specs=[">=7.0.0"])
        dep2 = DependencySpec(name="pytest", version_specs=[">=8.0.0"])

        group.add_dependency(dep1)
        group.add_dependency(dep2)

        assert len(group.dependencies) == 1
        assert group.dependencies[0].version_specs == [">=8.0.0"]

    def test_remove_dependency(self):
        """Test removing a dependency from a group."""
        group = DependencyGroup(name="dev")
        dep = DependencySpec(name="pytest", version_specs=[">=7.0.0"])

        group.add_dependency(dep)
        assert len(group.dependencies) == 1

        removed = group.remove_dependency("pytest")
        assert removed is True
        assert len(group.dependencies) == 0

    def test_remove_nonexistent_dependency(self):
        """Test removing nonexistent dependency."""
        group = DependencyGroup(name="dev")

        removed = group.remove_dependency("nonexistent")
        assert removed is False


class TestProjectConfig:
    """Test ProjectConfig model."""

    def test_create_basic_config(self):
        """Test creating basic project config."""
        config = ProjectConfig(name="test-project")

        assert config.name == "test-project"
        assert config.version == "0.1.0"
        assert config.description == ""
        assert config.requires_python == ">=3.8"
        assert config.dependencies == []
        assert config.optional_dependencies == {}
        assert config.dependency_groups == {}

    def test_add_main_dependency(self):
        """Test adding main dependency."""
        config = ProjectConfig(name="test-project")
        dep = DependencySpec(name="requests", version_specs=[">=2.25.0"])

        config.add_dependency(dep)

        assert len(config.dependencies) == 1
        assert config.dependencies[0] == dep

    def test_add_optional_dependency(self):
        """Test adding optional dependency."""
        config = ProjectConfig(name="test-project")
        dep = DependencySpec(name="pytest", version_specs=[">=7.0.0"])

        config.add_dependency(dep, group="dev", use_dependency_groups=True)

        assert "dev" in config.dependency_groups
        assert len(config.dependency_groups["dev"].dependencies) == 1
        assert config.dependency_groups["dev"].dependencies[0] == dep

    def test_add_optional_dependency_pep621(self):
        """Test adding optional dependency as PEP 621 extra."""
        config = ProjectConfig(name="test-project")
        dep = DependencySpec(name="requests", version_specs=[">=2.25.0"], extras=["security"])

        config.add_dependency(dep, group="security", use_dependency_groups=False)

        assert "security" in config.optional_dependencies
        assert len(config.optional_dependencies["security"].dependencies) == 1
        assert config.optional_dependencies["security"].dependencies[0] == dep

    def test_get_dependency_group(self):
        """Test getting dependency group."""
        config = ProjectConfig(name="test-project")
        dep = DependencySpec(name="pytest", version_specs=[">=7.0.0"])

        config.add_dependency(dep, group="dev", use_dependency_groups=True)

        group = config.get_dependency_group("dev", use_dependency_groups=True)
        assert group is not None
        assert group.name == "dev"
        assert len(group.dependencies) == 1

    def test_get_nonexistent_dependency_group(self):
        """Test getting nonexistent dependency group."""
        config = ProjectConfig(name="test-project")

        group = config.get_dependency_group("nonexistent")
        assert group is None

    def test_create_dependency_group(self):
        """Test creating new dependency group."""
        config = ProjectConfig(name="test-project")

        group = config.create_dependency_group("test", "Test dependencies", use_dependency_groups=True)

        assert group.name == "test"
        assert group.description == "Test dependencies"
        assert "test" in config.dependency_groups
        assert config.dependency_groups["test"] == group

    def test_dependency_groups_vs_optional_dependencies(self):
        """Test that dependency-groups and optional-dependencies are separate."""
        config = ProjectConfig(name="test-project")
        dep1 = DependencySpec(name="pytest", version_specs=[">=7.0.0"])
        dep2 = DependencySpec(name="requests", version_specs=[">=2.25.0"])

        # Add to dependency-groups
        config.add_dependency(dep1, group="dev", use_dependency_groups=True)
        # Add to optional-dependencies
        config.add_dependency(dep2, group="dev", use_dependency_groups=False)

        assert "dev" in config.dependency_groups
        assert "dev" in config.optional_dependencies
        assert len(config.dependency_groups["dev"].dependencies) == 1
        assert len(config.optional_dependencies["dev"].dependencies) == 1
        assert config.dependency_groups["dev"].dependencies[0].name == "pytest"
        assert config.optional_dependencies["dev"].dependencies[0].name == "requests"


class TestConversionOptions:
    """Test ConversionOptions model."""

    def test_create_default_options(self):
        """Test creating default conversion options."""
        options = ConversionOptions()

        assert options.output_file == Path("pyproject.toml")
        assert options.backup is True
        assert options.append is False
        assert options.dev_group_name == "dev"
        assert options.test_group_name == "test"
        assert options.docs_group_name == "docs"
        assert options.build_backend == "hatchling"
        assert options.enable_uv is True
        assert options.enable_hatch is True

    def test_validation_nonexistent_file(self, tmp_path):
        """Test validation with nonexistent file."""
        nonexistent_file = tmp_path / "nonexistent.txt"

        with pytest.raises(ValueError, match="File does not exist"):
            ConversionOptions(requirements_files=[nonexistent_file])
