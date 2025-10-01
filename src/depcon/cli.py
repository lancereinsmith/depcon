"""Command-line interface for depcon."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console
from rich.table import Table

from .generators import PyProjectUpdater
from .models import ConversionOptions, DependencySpec, ProjectConfig
from .parsers import group_dependencies_by_type, parse_requirements_file

console = Console()


@click.group()
@click.version_option(version="0.2.1")
def main():
    """Convert legacy requirements files to modern pyproject.toml format."""
    pass


@main.command()
@click.option(
    "-r",
    "--requirements",
    "requirements_files",
    multiple=True,
    type=click.Path(exists=True, path_type=Path),
    help="Requirements files to process (requirements.txt, requirements.in)",
)
@click.option(
    "-d",
    "--dev-requirements",
    "dev_requirements_files",
    multiple=True,
    type=click.Path(exists=True, path_type=Path),
    help="Development requirements files to process",
)
@click.option(
    "-t",
    "--test-requirements",
    "test_requirements_files",
    multiple=True,
    type=click.Path(exists=True, path_type=Path),
    help="Test requirements files to process",
)
@click.option(
    "--docs-requirements",
    "docs_requirements_files",
    multiple=True,
    type=click.Path(exists=True, path_type=Path),
    help="Documentation requirements files to process",
)
@click.option(
    "-o",
    "--output",
    "output_file",
    type=click.Path(path_type=Path),
    default=Path("pyproject.toml"),
    help="Output pyproject.toml file path",
)
@click.option(
    "--append/--no-append",
    default=False,
    help="Append to existing dependencies instead of replacing",
)
@click.option(
    "--backup/--no-backup",
    default=True,
    help="Create backup of existing pyproject.toml",
)
@click.option(
    "--resolve/--no-resolve", default=False, help="Resolve and pin dependency versions"
)
@click.option("--sort/--no-sort", default=True, help="Sort dependencies alphabetically")
@click.option(
    "--build-backend",
    type=click.Choice(["hatchling", "setuptools", "poetry"]),
    default="hatchling",
    help="Build backend to use",
)
@click.option(
    "--dev-group", default="dev", help="Name for development dependencies group"
)
@click.option("--test-group", default="test", help="Name for test dependencies group")
@click.option(
    "--docs-group", default="docs", help="Name for documentation dependencies group"
)
@click.option("--project-name", help="Project name (if creating new pyproject.toml)")
@click.option(
    "--project-version",
    default="0.1.0",
    help="Project version (if creating new pyproject.toml)",
)
@click.option(
    "--project-description", help="Project description (if creating new pyproject.toml)"
)
@click.option("--python-version", default=">=3.8", help="Python version requirement")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def convert(
    requirements_files: List[Path],
    dev_requirements_files: List[Path],
    test_requirements_files: List[Path],
    docs_requirements_files: List[Path],
    output_file: Path,
    append: bool,
    backup: bool,
    resolve: bool,
    sort: bool,
    build_backend: str,
    dev_group: str,
    test_group: str,
    docs_group: str,
    project_name: Optional[str],
    project_version: str,
    project_description: Optional[str],
    python_version: str,
    verbose: bool,
):
    """Convert requirements files to pyproject.toml format."""

    # Create conversion options
    options = ConversionOptions(
        requirements_files=list(requirements_files),
        output_file=output_file,
        append=append,
        backup=backup,
        resolve_dependencies=resolve,
        sort_dependencies=sort,
        build_backend=build_backend,
        dev_group_name=dev_group,
        test_group_name=test_group,
        docs_group_name=docs_group,
    )

    # Set build requirements based on backend
    if build_backend == "hatchling":
        options.build_requires = ["hatchling"]
    elif build_backend == "setuptools":
        options.build_requires = ["setuptools", "wheel"]
    elif build_backend == "poetry":
        options.build_requires = ["poetry-core"]

    try:
        # Parse all requirements files
        all_dependencies = []

        for req_file in requirements_files:
            if verbose:
                console.print(f"Parsing {req_file}...")
            deps = parse_requirements_file(req_file)
            all_dependencies.extend(deps)

        for req_file in dev_requirements_files:
            if verbose:
                console.print(f"Parsing dev requirements {req_file}...")
            deps = parse_requirements_file(req_file)
            all_dependencies.extend(deps)

        for req_file in test_requirements_files:
            if verbose:
                console.print(f"Parsing test requirements {req_file}...")
            deps = parse_requirements_file(req_file)
            all_dependencies.extend(deps)

        for req_file in docs_requirements_files:
            if verbose:
                console.print(f"Parsing docs requirements {req_file}...")
            deps = parse_requirements_file(req_file)
            all_dependencies.extend(deps)

        if not all_dependencies:
            console.print("[yellow]No dependencies found in input files.[/yellow]")
            return

        # Group dependencies by type
        grouped_deps = group_dependencies_by_type(all_dependencies)

        if verbose:
            _print_dependency_summary(grouped_deps)

        # Create or update pyproject.toml
        updater = PyProjectUpdater(output_file, options)

        # Set project metadata if provided
        if project_name or project_description:
            config = updater._load_existing_config()
            if project_name:
                config.name = project_name
            if project_description:
                config.description = project_description
            config.version = project_version
            config.requires_python = python_version

        updater.update_with_dependencies(
            main_deps=grouped_deps.get("main", []),
            dev_deps=grouped_deps.get("dev", []),
            test_deps=grouped_deps.get("test", []),
            docs_deps=grouped_deps.get("docs", []),
        )

        console.print(f"[green]Successfully updated {output_file}[/green]")

        if backup and output_file.exists():
            backup_file = output_file.with_suffix(".toml.backup")
            if backup_file.exists():
                console.print(f"[blue]Backup created: {backup_file}[/blue]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        if verbose:
            import traceback

            console.print(traceback.format_exc())
        sys.exit(1)


@main.command()
@click.option(
    "-f",
    "--file",
    "pyproject_file",
    type=click.Path(exists=True, path_type=Path),
    default=Path("pyproject.toml"),
    help="Path to pyproject.toml file",
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["table", "json", "yaml"]),
    default="table",
    help="Output format",
)
def show(pyproject_file: Path, output_format: str):
    """Show dependencies from pyproject.toml file."""
    try:
        updater = PyProjectUpdater(pyproject_file, ConversionOptions())
        config = updater._load_existing_config()

        if output_format == "table":
            _print_dependencies_table(config)
        elif output_format == "json":
            import json

            data = {
                "dependencies": [dep.to_pep621_string() for dep in config.dependencies],
                "optional_dependencies": {
                    name: [dep.to_pep621_string() for dep in group.dependencies]
                    for name, group in config.optional_dependencies.items()
                },
            }
            console.print(json.dumps(data, indent=2))
        elif output_format == "yaml":
            import yaml

            data = {
                "dependencies": [dep.to_pep621_string() for dep in config.dependencies],
                "optional_dependencies": {
                    name: [dep.to_pep621_string() for dep in group.dependencies]
                    for name, group in config.optional_dependencies.items()
                },
            }
            console.print(yaml.dump(data, default_flow_style=False))

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@main.command()
@click.option(
    "-f",
    "--file",
    "pyproject_file",
    type=click.Path(exists=True, path_type=Path),
    default=Path("pyproject.toml"),
    help="Path to pyproject.toml file",
)
@click.option("--group", help="Dependency group to validate (main, dev, test, docs)")
def validate(pyproject_file: Path, group: Optional[str]):
    """Validate pyproject.toml dependencies."""
    try:
        updater = PyProjectUpdater(pyproject_file, ConversionOptions())
        config = updater._load_existing_config()

        errors = []
        warnings = []

        # Validate main dependencies
        if not group or group == "main":
            for dep in config.dependencies:
                if not _validate_dependency(dep):
                    errors.append(f"Invalid dependency: {dep.to_pep621_string()}")

        # Validate optional dependencies
        for group_name, group_deps in config.optional_dependencies.items():
            if not group or group == group_name:
                for dep in group_deps.dependencies:
                    if not _validate_dependency(dep):
                        errors.append(
                            f"Invalid dependency in {group_name}: {dep.to_pep621_string()}"
                        )

        if errors:
            console.print("[red]Validation errors:[/red]")
            for error in errors:
                console.print(f"  - {error}")

        if warnings:
            console.print("[yellow]Validation warnings:[/yellow]")
            for warning in warnings:
                console.print(f"  - {warning}")

        if not errors and not warnings:
            console.print("[green]All dependencies are valid![/green]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


def _print_dependency_summary(grouped_deps: dict[str, List[DependencySpec]]) -> None:
    """Print a summary of grouped dependencies."""
    table = Table(title="Dependency Summary")
    table.add_column("Group", style="cyan")
    table.add_column("Count", style="magenta")
    table.add_column("Dependencies", style="green")

    for group_name, deps in grouped_deps.items():
        if deps:
            dep_names = [dep.name for dep in deps[:5]]  # Show first 5
            if len(deps) > 5:
                dep_names.append(f"... and {len(deps) - 5} more")
            table.add_row(group_name.title(), str(len(deps)), ", ".join(dep_names))

    console.print(table)


def _print_dependencies_table(config: ProjectConfig) -> None:
    """Print dependencies in a table format."""
    if config.dependencies:
        table = Table(title="Main Dependencies")
        table.add_column("Package", style="cyan")
        table.add_column("Version", style="magenta")
        table.add_column("Extras", style="green")

        for dep in config.dependencies:
            table.add_row(
                dep.name,
                ", ".join(dep.version_specs) if dep.version_specs else "latest",
                ", ".join(dep.extras) if dep.extras else "",
            )

        console.print(table)

    for group_name, group in config.optional_dependencies.items():
        if group.dependencies:
            table = Table(title=f"{group_name.title()} Dependencies")
            table.add_column("Package", style="cyan")
            table.add_column("Version", style="magenta")
            table.add_column("Extras", style="green")

            for dep in group.dependencies:
                table.add_row(
                    dep.name,
                    ", ".join(dep.version_specs) if dep.version_specs else "latest",
                    ", ".join(dep.extras) if dep.extras else "",
                )

            console.print(table)


def _validate_dependency(dep: DependencySpec) -> bool:
    """Validate a dependency specification."""
    try:
        # Try to parse the dependency string
        from packaging.requirements import Requirement

        req = Requirement(dep.to_pep621_string())
        return True
    except Exception:
        return False


if __name__ == "__main__":
    main()
