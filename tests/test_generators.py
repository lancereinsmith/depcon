"""Tests for the generators module."""

from __future__ import annotations

import tomllib

from depcon.generators import PyProjectGenerator, PyProjectUpdater, parse_dep_string
from depcon.models import (
    ConversionOptions,
    DependencyGroup,
    DependencySpec,
    ProjectConfig,
)


class TestParseDepString:
    """Tests for the parse_dep_string helper."""

    def test_simple_package(self):
        dep = parse_dep_string("requests")
        assert dep is not None
        assert dep.name == "requests"
        assert dep.version_specs == []

    def test_package_with_version(self):
        dep = parse_dep_string("requests>=2.28.0")
        assert dep is not None
        assert dep.name == "requests"
        assert ">=2.28.0" in dep.version_specs

    def test_package_with_extras(self):
        dep = parse_dep_string("uvicorn[standard]>=0.20.0")
        assert dep is not None
        assert dep.name == "uvicorn"
        assert "standard" in dep.extras

    def test_package_with_markers(self):
        dep = parse_dep_string('pywin32; sys_platform == "win32"')
        assert dep is not None
        assert dep.name == "pywin32"
        assert dep.markers is not None
        assert "win32" in dep.markers

    def test_invalid_string_returns_none(self):
        dep = parse_dep_string("not a valid!!!! spec @@@")
        assert dep is None

    def test_url_dependency(self):
        dep = parse_dep_string("mypackage @ https://example.com/pkg.tar.gz")
        assert dep is not None
        assert dep.name == "mypackage"


class TestPyProjectGenerator:
    """Tests for PyProjectGenerator."""

    def test_basic_generation(self):
        config = ProjectConfig(
            name="test-project",
            version="1.0.0",
            description="A test project",
        )
        generator = PyProjectGenerator(config)
        content = generator.generate_toml_content()

        assert content["build-system"]["requires"] == ["hatchling"]
        assert content["project"]["name"] == "test-project"
        assert content["project"]["version"] == "1.0.0"

    def test_pep639_license_from_string(self):
        config = ProjectConfig(name="test", license="MIT")
        generator = PyProjectGenerator(config)
        content = generator.generate_toml_content()

        assert content["project"]["license"] == "MIT"

    def test_pep639_license_from_dict(self):
        config = ProjectConfig(name="test", license={"text": "Apache-2.0"})
        generator = PyProjectGenerator(config)
        content = generator.generate_toml_content()

        # Should normalize dict to string
        assert content["project"]["license"] == "Apache-2.0"

    def test_dependency_groups_with_include(self):
        dev_group = DependencyGroup(
            name="dev",
            include_groups=["test"],
            dependencies=[DependencySpec(name="ruff", version_specs=[">=0.14.0"])],
        )
        config = ProjectConfig(
            name="test",
            dependency_groups={"dev": dev_group},
        )
        generator = PyProjectGenerator(config)
        content = generator.generate_toml_content()

        dev_items = content["dependency-groups"]["dev"]
        assert {"include-group": "test"} in dev_items
        assert "ruff>=0.14.0" in dev_items
        # include-group should come before deps
        assert dev_items[0] == {"include-group": "test"}

    def test_dependencies_in_output(self):
        config = ProjectConfig(
            name="test",
            dependencies=[
                DependencySpec(name="click", version_specs=[">=8.0"]),
                DependencySpec(name="rich", version_specs=[">=13.0"]),
            ],
        )
        generator = PyProjectGenerator(config)
        content = generator.generate_toml_content()

        deps = content["project"]["dependencies"]
        assert "click>=8.0" in deps
        assert "rich>=13.0" in deps

    def test_optional_dependencies(self):
        test_group = DependencyGroup(
            name="test",
            dependencies=[DependencySpec(name="pytest", version_specs=[">=8.0"])],
        )
        config = ProjectConfig(
            name="test",
            optional_dependencies={"test": test_group},
        )
        generator = PyProjectGenerator(config)
        content = generator.generate_toml_content()

        assert "pytest>=8.0" in content["project"]["optional-dependencies"]["test"]

    def test_removes_deprecated_uv_dev_dependencies(self):
        config = ProjectConfig(
            name="test",
            tool_configs={"uv": {"dev-dependencies": ["pytest"], "other": "value"}},
        )
        generator = PyProjectGenerator(config)
        content = generator.generate_toml_content()

        assert "dev-dependencies" not in content["tool"]["uv"]
        assert content["tool"]["uv"]["other"] == "value"

    def test_removes_empty_uv_config(self):
        config = ProjectConfig(
            name="test",
            tool_configs={"uv": {"dev-dependencies": ["pytest"]}},
        )
        generator = PyProjectGenerator(config)
        content = generator.generate_toml_content()

        assert "uv" not in content.get("tool", {})

    def test_write_to_file(self, tmp_path):
        config = ProjectConfig(
            name="test-project",
            version="1.0.0",
            description="Test",
            license="MIT",
        )
        generator = PyProjectGenerator(config)
        output = tmp_path / "pyproject.toml"
        generator.write_to_file(output, backup=False)

        with open(output, "rb") as f:
            data = tomllib.load(f)

        assert data["project"]["name"] == "test-project"
        assert data["project"]["license"] == "MIT"

    def test_write_creates_backup(self, tmp_path):
        output = tmp_path / "pyproject.toml"
        output.write_text("[project]\nname = 'old'\n")

        config = ProjectConfig(name="new")
        generator = PyProjectGenerator(config)
        generator.write_to_file(output, backup=True)

        backup = tmp_path / "pyproject.toml.backup"
        assert backup.exists()


class TestPyProjectUpdater:
    """Tests for PyProjectUpdater."""

    def test_load_config_nonexistent_file(self, tmp_path):
        updater = PyProjectUpdater(tmp_path / "nonexistent.toml", ConversionOptions())
        config = updater.load_config()

        assert config.name == "project-name"

    def test_load_config_basic(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[project]\nname = "myproject"\nversion = "2.0.0"\n'
            'requires-python = ">=3.12"\nlicense = "MIT"\n'
        )

        updater = PyProjectUpdater(pyproject, ConversionOptions())
        config = updater.load_config()

        assert config.name == "myproject"
        assert config.version == "2.0.0"
        assert config.requires_python == ">=3.12"
        assert config.license == "MIT"

    def test_load_config_pep639_license_normalization(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[project]\nname = "test"\n\n[project.license]\ntext = "BSD-3-Clause"\n'
        )

        updater = PyProjectUpdater(pyproject, ConversionOptions())
        config = updater.load_config()

        assert config.license == "BSD-3-Clause"

    def test_load_config_dependency_groups_with_include(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[project]\nname = "test"\n\n'
            "[dependency-groups]\n"
            'dev = [{include-group = "test"}, "ruff>=0.14.0"]\n'
            'test = ["pytest>=8.0"]\n'
        )

        updater = PyProjectUpdater(pyproject, ConversionOptions())
        config = updater.load_config()

        assert "dev" in config.dependency_groups
        assert "test" in config.dependency_groups
        dev = config.dependency_groups["dev"]
        assert "test" in dev.include_groups
        assert any(d.name == "ruff" for d in dev.dependencies)

    def test_load_config_with_dependencies(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[project]\nname = "test"\ndependencies = ["click>=8.0", "rich>=13.0"]\n'
        )

        updater = PyProjectUpdater(pyproject, ConversionOptions())
        config = updater.load_config()

        assert len(config.dependencies) == 2
        names = [d.name for d in config.dependencies]
        assert "click" in names
        assert "rich" in names

    def test_load_config_with_tool_configs(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[project]\nname = "test"\n\n[tool.ruff]\nline-length = 88\n'
        )

        updater = PyProjectUpdater(pyproject, ConversionOptions())
        config = updater.load_config()

        assert "ruff" in config.tool_configs
        assert config.tool_configs["ruff"]["line-length"] == 88

    def test_round_trip(self, tmp_path):
        """Load a pyproject.toml, generate content, write it, and load again."""
        original = tmp_path / "pyproject.toml"
        original.write_text(
            '[build-system]\nrequires = ["hatchling"]\n'
            'build-backend = "hatchling.build"\n\n'
            '[project]\nname = "roundtrip"\nversion = "1.0.0"\n'
            'description = "Test round trip"\n'
            'requires-python = ">=3.12"\n'
            'license = "MIT"\n'
            'dependencies = ["click>=8.0", "rich>=13.0"]\n\n'
            "[dependency-groups]\n"
            'dev = [{include-group = "test"}, "ruff>=0.14.0"]\n'
            'test = ["pytest>=8.0"]\n'
        )

        updater = PyProjectUpdater(original, ConversionOptions())
        config = updater.load_config()

        generator = PyProjectGenerator(config)
        output = tmp_path / "output.toml"
        generator.write_to_file(output, backup=False)

        updater2 = PyProjectUpdater(output, ConversionOptions())
        config2 = updater2.load_config()

        assert config2.name == "roundtrip"
        assert config2.version == "1.0.0"
        assert config2.license == "MIT"
        assert len(config2.dependencies) == 2
        assert "test" in config2.dependency_groups["dev"].include_groups
