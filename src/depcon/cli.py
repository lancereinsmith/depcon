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
@click.version_option(version="0.4.1")
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
@click.option("--python-version", default=">=3.11", help="Python version requirement")
@click.option(
    "--use-optional-deps/--use-dependency-groups",
    "use_optional_deps",
    default=False,
    help="Use optional-dependencies (PEP 621 extras) instead of dependency-groups (PEP 735)",
)
@click.option(
    "--remove-duplicates/--keep-duplicates",
    default=True,
    help="Remove duplicate dependencies across groups",
)
@click.option(
    "--strict/--no-strict",
    default=False,
    help="Strict mode: fail on parsing errors instead of warning",
)
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
    use_optional_deps: bool,
    remove_duplicates: bool,
    strict: bool,
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

        # Remove duplicates if requested
        if remove_duplicates:
            _remove_duplicate_dependencies(grouped_deps)

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

        # Determine whether to use dependency-groups or optional-dependencies
        use_dependency_groups = not use_optional_deps

        updater.update_with_dependencies(
            main_deps=grouped_deps.get("main", []),
            dev_deps=grouped_deps.get("dev", []),
            test_deps=grouped_deps.get("test", []),
            docs_deps=grouped_deps.get("docs", []),
            use_dependency_groups=use_dependency_groups,
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
@click.option(
    "--group",
    help="Show only specific dependency group (main, dev, test, docs, or optional group name)",
)
def show(pyproject_file: Path, output_format: str, group: Optional[str]):
    """Show dependencies from pyproject.toml file."""
    try:
        updater = PyProjectUpdater(pyproject_file, ConversionOptions())
        config = updater._load_existing_config()

        # Filter by group if specified
        if group:
            if group == "main":
                config.dependencies = config.dependencies
                config.optional_dependencies = {}
                config.dependency_groups = {}
            elif group in config.optional_dependencies:
                config.dependencies = []
                config.dependency_groups = {}
                # Keep only the specified optional dependency group
                filtered_optional = {group: config.optional_dependencies[group]}
                config.optional_dependencies = filtered_optional
            elif group in config.dependency_groups:
                config.dependencies = []
                config.optional_dependencies = {}
                # Keep only the specified dependency group
                filtered_groups = {group: config.dependency_groups[group]}
                config.dependency_groups = filtered_groups
            else:
                console.print(f"[yellow]Group '{group}' not found[/yellow]")
                return

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
                "dependency_groups": {
                    name: [dep.to_pep621_string() for dep in group.dependencies]
                    for name, group in config.dependency_groups.items()
                },
            }
            console.print(json.dumps(data, indent=2))
        elif output_format == "yaml":
            try:
                import yaml
            except ImportError:
                console.print(
                    "[red]yaml format requires PyYAML. Install with: pip install pyyaml[/red]"
                )
                sys.exit(1)

            data = {
                "dependencies": [dep.to_pep621_string() for dep in config.dependencies],
                "optional_dependencies": {
                    name: [dep.to_pep621_string() for dep in group.dependencies]
                    for name, group in config.optional_dependencies.items()
                },
                "dependency_groups": {
                    name: [dep.to_pep621_string() for dep in group.dependencies]
                    for name, group in config.dependency_groups.items()
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
@click.option(
    "--check-pypi/--no-check-pypi",
    default=False,
    help="Check if packages exist on PyPI",
)
def validate(pyproject_file: Path, group: Optional[str], check_pypi: bool):
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
                            f"Invalid dependency in optional-dependencies.{group_name}: {dep.to_pep621_string()}"
                        )

        # Validate dependency groups
        for group_name, group_deps in config.dependency_groups.items():
            if not group or group == group_name:
                for dep in group_deps.dependencies:
                    if not _validate_dependency(dep):
                        errors.append(
                            f"Invalid dependency in dependency-groups.{group_name}: {dep.to_pep621_string()}"
                        )

        if errors:
            console.print("[red]Validation errors:[/red]")
            for error in errors:
                console.print(f"  - {error}")

        if warnings:
            console.print("[yellow]Validation warnings:[/yellow]")
            for warning in warnings:
                console.print(f"  - {warning}")

        if check_pypi:
            _check_pypi_availability(config, group)

        if not errors and not warnings:
            console.print("[green]All dependencies are valid![/green]")
        else:
            sys.exit(1)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@main.command(name="list")
@click.option(
    "-f",
    "--file",
    "pyproject_file",
    type=click.Path(exists=True, path_type=Path),
    default=Path("pyproject.toml"),
    help="Path to pyproject.toml file",
)
def list_groups(pyproject_file: Path):
    """List all dependency groups in pyproject.toml."""
    try:
        updater = PyProjectUpdater(pyproject_file, ConversionOptions())
        config = updater._load_existing_config()

        table = Table(title="Dependency Groups")
        table.add_column("Type", style="cyan")
        table.add_column("Group Name", style="magenta")
        table.add_column("Count", style="green")

        if config.dependencies:
            table.add_row("Main", "dependencies", str(len(config.dependencies)))

        for name, group in config.optional_dependencies.items():
            table.add_row("Optional (PEP 621)", name, str(len(group.dependencies)))

        for name, group in config.dependency_groups.items():
            table.add_row("Group (PEP 735)", name, str(len(group.dependencies)))

        console.print(table)

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
@click.option(
    "--check-duplicates/--no-check-duplicates",
    default=True,
    help="Check for duplicate dependencies",
)
@click.option(
    "--check-missing/--no-check-missing",
    default=False,
    help="Check for missing optional dependencies",
)
def check(pyproject_file: Path, check_duplicates: bool, check_missing: bool):
    """Check pyproject.toml for common issues."""
    try:
        updater = PyProjectUpdater(pyproject_file, ConversionOptions())
        config = updater._load_existing_config()

        issues = []
        warnings = []

        if check_duplicates:
            # Check for duplicates across groups
            all_dep_names = {}
            for dep in config.dependencies:
                if dep.name in all_dep_names:
                    issues.append(
                        f"Duplicate dependency '{dep.name}' found in main dependencies and {all_dep_names[dep.name]}"
                    )
                all_dep_names[dep.name] = "main dependencies"

            for name, group in config.optional_dependencies.items():
                for dep in group.dependencies:
                    if dep.name in all_dep_names:
                        issues.append(
                            f"Duplicate dependency '{dep.name}' found in optional-dependencies.{name} and {all_dep_names[dep.name]}"
                        )
                    all_dep_names[dep.name] = f"optional-dependencies.{name}"

            for name, group in config.dependency_groups.items():
                for dep in group.dependencies:
                    if dep.name in all_dep_names:
                        warnings.append(
                            f"Duplicate dependency '{dep.name}' found in dependency-groups.{name} and {all_dep_names[dep.name]} (this may be intentional)"
                        )
                    all_dep_names[dep.name] = f"dependency-groups.{name}"

        if check_missing:
            # Check if optional dependencies reference missing main dependencies
            main_dep_names = {dep.name for dep in config.dependencies}
            for name, group in config.optional_dependencies.items():
                for dep in group.dependencies:
                    if dep.name not in main_dep_names:
                        # This is fine, just a note
                        pass

        if issues:
            console.print("[red]Issues found:[/red]")
            for issue in issues:
                console.print(f"  - {issue}")

        if warnings:
            console.print("[yellow]Warnings:[/yellow]")
            for warning in warnings:
                console.print(f"  - {warning}")

        if not issues and not warnings:
            console.print("[green]No issues found![/green]")
        elif issues:
            sys.exit(1)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


def _check_pypi_availability(config: ProjectConfig, group: Optional[str]) -> None:
    """Check if packages are available on PyPI."""
    try:
        import json
        import urllib.request

        packages_to_check = []
        if not group or group == "main":
            packages_to_check.extend([dep.name for dep in config.dependencies])

        if not group:
            for group_deps in config.optional_dependencies.values():
                packages_to_check.extend([dep.name for dep in group_deps.dependencies])
            for group_deps in config.dependency_groups.values():
                packages_to_check.extend([dep.name for dep in group_deps.dependencies])
        elif group in config.optional_dependencies:
            packages_to_check.extend(
                [dep.name for dep in config.optional_dependencies[group].dependencies]
            )
        elif group in config.dependency_groups:
            packages_to_check.extend(
                [dep.name for dep in config.dependency_groups[group].dependencies]
            )

        unavailable = []
        for package in set(packages_to_check):
            try:
                url = f"https://pypi.org/pypi/{package}/json"
                with urllib.request.urlopen(url, timeout=5) as response:
                    json.loads(response.read())
            except Exception:
                unavailable.append(package)

        if unavailable:
            console.print("[yellow]Packages not found on PyPI:[/yellow]")
            for package in unavailable:
                console.print(f"  - {package}")

    except ImportError:
        console.print(
            "[yellow]PyPI check requires urllib (built-in) or requests[/yellow]"
        )
    except Exception as e:
        console.print(f"[yellow]Could not check PyPI availability: {e}[/yellow]")


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
    "-o",
    "--output",
    "output_file",
    type=click.Path(path_type=Path),
    default=Path("requirements.txt"),
    help="Output requirements.txt file path",
)
@click.option(
    "--group",
    help="Dependency group to export (main, dev, test, docs, or all)",
    default="main",
)
@click.option("--include-hashes", is_flag=True, help="Include package hashes")
def export(pyproject_file: Path, output_file: Path, group: str, include_hashes: bool):
    """Export dependencies from pyproject.toml to requirements.txt format."""
    try:
        updater = PyProjectUpdater(pyproject_file, ConversionOptions())
        config = updater._load_existing_config()

        dependencies = []
        if group == "main" or group == "all":
            dependencies.extend(config.dependencies)

        if group == "all":
            for group_name, group_deps in config.optional_dependencies.items():
                dependencies.extend(group_deps.dependencies)
            for group_name, group_deps in config.dependency_groups.items():
                dependencies.extend(group_deps.dependencies)
        elif group in config.optional_dependencies:
            dependencies.extend(config.optional_dependencies[group].dependencies)
        elif group in config.dependency_groups:
            dependencies.extend(config.dependency_groups[group].dependencies)

        if not dependencies:
            console.print(f"[yellow]No dependencies found for group: {group}[/yellow]")
            return

        # Write to requirements.txt
        with open(output_file, "w", encoding="utf-8") as f:
            for dep in sorted(dependencies, key=lambda d: d.name):
                f.write(dep.to_string() + "\n")

        console.print(
            f"[green]Exported {len(dependencies)} dependencies to {output_file}[/green]"
        )

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
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
    "-r",
    "--requirements",
    "requirements_file",
    type=click.Path(exists=True, path_type=Path),
    help="Path to requirements.txt file to compare",
)
@click.option("--group", help="Dependency group to compare (main, dev, test, docs)")
def diff(pyproject_file: Path, requirements_file: Optional[Path], group: Optional[str]):
    """Show differences between pyproject.toml and requirements files."""
    try:
        try:
            from rich.diff import Diff
        except ImportError:
            # Fallback if rich.diff is not available
            Diff = None

        updater = PyProjectUpdater(pyproject_file, ConversionOptions())
        config = updater._load_existing_config()

        # Get dependencies from pyproject.toml
        pyproject_deps = []
        if not group or group == "main":
            pyproject_deps.extend(config.dependencies)
        if not group or group in config.optional_dependencies:
            if group in config.optional_dependencies:
                pyproject_deps.extend(config.optional_dependencies[group].dependencies)
        if not group or group in config.dependency_groups:
            if group in config.dependency_groups:
                pyproject_deps.extend(config.dependency_groups[group].dependencies)

        pyproject_lines = sorted([dep.to_string() for dep in pyproject_deps])

        if requirements_file:
            # Get dependencies from requirements file
            req_deps = parse_requirements_file(requirements_file)
            req_lines = sorted([dep.to_string() for dep in req_deps])

            # Show diff
            console.print("[bold]Differences:[/bold]")
            if Diff:
                diff = Diff(pyproject_lines, req_lines)
                console.print(diff)
            else:
                # Simple text diff
                only_in_pyproject = set(pyproject_lines) - set(req_lines)
                only_in_req = set(req_lines) - set(pyproject_lines)
                if only_in_pyproject:
                    console.print("[green]Only in pyproject.toml:[/green]")
                    for line in sorted(only_in_pyproject):
                        console.print(f"  + {line}")
                if only_in_req:
                    console.print("[red]Only in requirements.txt:[/red]")
                    for line in sorted(only_in_req):
                        console.print(f"  - {line}")
                if not only_in_pyproject and not only_in_req:
                    console.print("[green]No differences found[/green]")
        else:
            # Just show pyproject.toml dependencies
            console.print("[bold]Dependencies in pyproject.toml:[/bold]")
            for line in pyproject_lines:
                console.print(f"  {line}")

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
@click.option(
    "--group",
    multiple=True,
    help="Dependency groups to sync (default: all)",
    default=["main", "dev", "test", "docs"],
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be synced without making changes"
)
def sync(pyproject_file: Path, group: tuple, dry_run: bool):
    """Sync dependencies from pyproject.toml to requirements files."""
    try:
        updater = PyProjectUpdater(pyproject_file, ConversionOptions())
        config = updater._load_existing_config()

        group_list = list(group) if group else ["main", "dev", "test", "docs"]

        for grp in group_list:
            if grp == "main":
                deps = config.dependencies
                output_file = Path("requirements.txt")
            elif grp in config.optional_dependencies:
                deps = config.optional_dependencies[grp].dependencies
                output_file = Path(f"requirements-{grp}.txt")
            elif grp in config.dependency_groups:
                deps = config.dependency_groups[grp].dependencies
                output_file = Path(f"requirements-{grp}.txt")
            else:
                console.print(f"[yellow]Group '{grp}' not found, skipping[/yellow]")
                continue

            if not deps:
                continue

            if dry_run:
                console.print(
                    f"[cyan]Would sync {len(deps)} dependencies to {output_file}[/cyan]"
                )
                for dep in sorted(deps, key=lambda d: d.name):
                    console.print(f"  {dep.to_string()}")
            else:
                with open(output_file, "w", encoding="utf-8") as f:
                    for dep in sorted(deps, key=lambda d: d.name):
                        f.write(dep.to_string() + "\n")
                console.print(
                    f"[green]Synced {len(deps)} dependencies to {output_file}[/green]"
                )

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
            table = Table(title=f"Optional Dependencies: {group_name.title()}")
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

    for group_name, group in config.dependency_groups.items():
        if group.dependencies:
            table = Table(title=f"Dependency Group: {group_name.title()}")
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

        Requirement(dep.to_pep621_string())
        return True
    except Exception:
        return False


def _remove_duplicate_dependencies(
    grouped_deps: dict[str, List[DependencySpec]],
) -> None:
    """Remove duplicate dependencies across groups, keeping the first occurrence."""
    seen_names = set()

    # Process main dependencies first
    if "main" in grouped_deps:
        main_deps = []
        for dep in grouped_deps["main"]:
            if dep.name not in seen_names:
                main_deps.append(dep)
                seen_names.add(dep.name)
        grouped_deps["main"] = main_deps

    # Process other groups
    for group_name in ["dev", "test", "docs"]:
        if group_name in grouped_deps:
            filtered_deps = []
            for dep in grouped_deps[group_name]:
                if dep.name not in seen_names:
                    filtered_deps.append(dep)
                    seen_names.add(dep.name)
            grouped_deps[group_name] = filtered_deps


if __name__ == "__main__":
    main()
