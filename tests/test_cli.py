"""Tests for CLI commands."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from depcon.cli import main


class TestConvertCommand:
    """Test convert command."""

    def test_convert_basic(self, tmp_path):
        """Test basic conversion."""
        runner = CliRunner()
        req_file = tmp_path / "requirements.txt"
        req_file.write_text("requests>=2.25.0\nnumpy>=1.20.0")
        output_file = tmp_path / "pyproject.toml"

        result = runner.invoke(
            main,
            ["convert", "-r", str(req_file), "-o", str(output_file), "--no-backup"],
        )

        assert result.exit_code == 0
        assert output_file.exists()

    def test_convert_with_optional_deps(self, tmp_path):
        """Test convert with --use-optional-deps flag."""
        runner = CliRunner()
        req_file = tmp_path / "requirements.txt"
        req_file.write_text("requests>=2.25.0")
        dev_file = tmp_path / "requirements-dev.txt"
        dev_file.write_text("pytest>=7.0.0")
        output_file = tmp_path / "pyproject.toml"

        result = runner.invoke(
            main,
            [
                "convert",
                "-r",
                str(req_file),
                "-d",
                str(dev_file),
                "-o",
                str(output_file),
                "--use-optional-deps",
                "--no-backup",
            ],
        )

        assert result.exit_code == 0
        assert output_file.exists()
        content = output_file.read_text()
        assert "optional-dependencies" in content

    def test_convert_remove_duplicates(self, tmp_path):
        """Test convert with --remove-duplicates flag."""
        runner = CliRunner()
        req_file = tmp_path / "requirements.txt"
        req_file.write_text("requests>=2.25.0\npytest>=7.0.0")
        dev_file = tmp_path / "requirements-dev.txt"
        dev_file.write_text("pytest>=7.0.0")
        output_file = tmp_path / "pyproject.toml"

        result = runner.invoke(
            main,
            [
                "convert",
                "-r",
                str(req_file),
                "-d",
                str(dev_file),
                "-o",
                str(output_file),
                "--remove-duplicates",
                "--no-backup",
            ],
        )

        assert result.exit_code == 0
        assert output_file.exists()


class TestShowCommand:
    """Test show command."""

    def test_show_basic(self, tmp_path):
        """Test basic show command."""
        runner = CliRunner()
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(
            """[project]
name = "test-project"
version = "0.1.0"
dependencies = ["requests>=2.25.0"]
"""
        )

        result = runner.invoke(main, ["show", "-f", str(pyproject_file)])

        assert result.exit_code == 0
        assert "requests" in result.output

    def test_show_with_group(self, tmp_path):
        """Test show with --group option."""
        runner = CliRunner()
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(
            """[project]
name = "test-project"
version = "0.1.0"
dependencies = ["requests>=2.25.0"]

[dependency-groups]
dev = ["pytest>=7.0.0"]
"""
        )

        result = runner.invoke(
            main, ["show", "-f", str(pyproject_file), "--group", "dev"]
        )

        assert result.exit_code == 0
        assert "pytest" in result.output

    def test_show_json_format(self, tmp_path):
        """Test show with JSON format."""
        runner = CliRunner()
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(
            """[project]
name = "test-project"
version = "0.1.0"
dependencies = ["requests>=2.25.0"]
"""
        )

        result = runner.invoke(
            main, ["show", "-f", str(pyproject_file), "--format", "json"]
        )

        assert result.exit_code == 0
        assert "requests" in result.output


class TestValidateCommand:
    """Test validate command."""

    def test_validate_basic(self, tmp_path):
        """Test basic validate command."""
        runner = CliRunner()
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(
            """[project]
name = "test-project"
version = "0.1.0"
dependencies = ["requests>=2.25.0"]
"""
        )

        result = runner.invoke(main, ["validate", "-f", str(pyproject_file)])

        assert result.exit_code == 0
        assert "valid" in result.output.lower()

    def test_validate_with_group(self, tmp_path):
        """Test validate with --group option."""
        runner = CliRunner()
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(
            """[project]
name = "test-project"
version = "0.1.0"
dependencies = ["requests>=2.25.0"]

[dependency-groups]
dev = ["pytest>=7.0.0"]
"""
        )

        result = runner.invoke(
            main, ["validate", "-f", str(pyproject_file), "--group", "dev"]
        )

        assert result.exit_code == 0


class TestListCommand:
    """Test list command."""

    def test_list_groups(self, tmp_path):
        """Test list command."""
        runner = CliRunner()
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(
            """[project]
name = "test-project"
version = "0.1.0"
dependencies = ["requests>=2.25.0"]

[dependency-groups]
dev = ["pytest>=7.0.0"]
test = ["pytest-cov>=4.0.0"]
"""
        )

        result = runner.invoke(main, ["list", "-f", str(pyproject_file)])

        assert result.exit_code == 0
        assert "dev" in result.output
        assert "test" in result.output


class TestCheckCommand:
    """Test check command."""

    def test_check_basic(self, tmp_path):
        """Test basic check command."""
        runner = CliRunner()
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(
            """[project]
name = "test-project"
version = "0.1.0"
dependencies = ["requests>=2.25.0"]
"""
        )

        result = runner.invoke(main, ["check", "-f", str(pyproject_file)])

        assert result.exit_code == 0

    def test_check_duplicates(self, tmp_path):
        """Test check with duplicate detection."""
        runner = CliRunner()
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(
            """[project]
name = "test-project"
version = "0.1.0"
dependencies = ["pytest>=7.0.0"]

[dependency-groups]
dev = ["pytest>=7.0.0"]
"""
        )

        result = runner.invoke(
            main, ["check", "-f", str(pyproject_file), "--check-duplicates"]
        )

        # Should find duplicate
        assert (
            "duplicate" in result.output.lower() or "warning" in result.output.lower()
        )


class TestExportCommand:
    """Test export command."""

    def test_export_basic(self, tmp_path):
        """Test basic export command."""
        runner = CliRunner()
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(
            """[project]
name = "test-project"
version = "0.1.0"
dependencies = ["requests>=2.25.0"]
"""
        )
        output_file = tmp_path / "requirements.txt"

        result = runner.invoke(
            main, ["export", "-f", str(pyproject_file), "-o", str(output_file)]
        )

        assert result.exit_code == 0
        assert output_file.exists()
        assert "requests" in output_file.read_text()


class TestDiffCommand:
    """Test diff command."""

    def test_diff_basic(self, tmp_path):
        """Test basic diff command."""
        runner = CliRunner()
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(
            """[project]
name = "test-project"
version = "0.1.0"
dependencies = ["requests>=2.25.0"]
"""
        )
        req_file = tmp_path / "requirements.txt"
        req_file.write_text("requests>=2.25.0\nnumpy>=1.20.0")

        result = runner.invoke(
            main, ["diff", "-f", str(pyproject_file), "-r", str(req_file)]
        )

        assert result.exit_code == 0


class TestSyncCommand:
    """Test sync command."""

    def test_sync_dry_run(self, tmp_path):
        """Test sync with dry-run."""
        runner = CliRunner()
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(
            """[project]
name = "test-project"
version = "0.1.0"
dependencies = ["requests>=2.25.0"]

[dependency-groups]
dev = ["pytest>=7.0.0"]
"""
        )

        result = runner.invoke(main, ["sync", "-f", str(pyproject_file), "--dry-run"])

        assert result.exit_code == 0
        assert "Would sync" in result.output or "requests" in result.output
