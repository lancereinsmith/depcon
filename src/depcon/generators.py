"""PyProject.toml generation and manipulation."""

from __future__ import annotations

import logging
import shutil
import tomllib
from pathlib import Path
from typing import Any

import tomli_w
from packaging.requirements import Requirement

from .models import DependencyGroup, DependencySpec, ProjectConfig

logger = logging.getLogger(__name__)


def parse_dep_string(dep_str: str) -> DependencySpec | None:
    """Parse a PEP 621 dependency string into a DependencySpec."""
    try:
        req = Requirement(dep_str)
        return DependencySpec(
            name=req.name,
            version_specs=[str(spec) for spec in req.specifier]
            if req.specifier
            else [],
            extras=list(req.extras),
            markers=str(req.marker) if req.marker else None,
        )
    except Exception:
        return None


class PyProjectGenerator:
    """Generate and manipulate pyproject.toml files."""

    def __init__(self, config: ProjectConfig):
        """Initialize generator with project configuration."""
        self.config = config

    def generate_toml_content(self) -> dict[str, Any]:
        """Generate TOML content from project configuration."""
        content: dict[str, Any] = {}

        # Build system
        content["build-system"] = self.config.build_system

        # Project metadata
        project: dict[str, Any] = {
            "name": self.config.name,
            "version": self.config.version,
            "description": self.config.description,
            "requires-python": self.config.requires_python,
        }

        if self.config.readme:
            project["readme"] = self.config.readme

        if self.config.authors:
            project["authors"] = self.config.authors

        if self.config.license:
            # PEP 639: emit license as a simple SPDX string
            if isinstance(self.config.license, dict):
                project["license"] = self.config.license.get(
                    "text", self.config.license.get("file", "")
                )
            else:
                project["license"] = self.config.license

        if self.config.keywords:
            project["keywords"] = self.config.keywords

        if self.config.classifiers:
            project["classifiers"] = self.config.classifiers

        if self.config.urls:
            project["urls"] = self.config.urls

        # Dependencies
        if self.config.dependencies:
            project["dependencies"] = [
                dep.to_pep621_string() for dep in self.config.dependencies
            ]

        # Optional dependencies (PEP 621 extras)
        if self.config.optional_dependencies:
            project["optional-dependencies"] = {}
            for group_name, group in self.config.optional_dependencies.items():
                project["optional-dependencies"][group_name] = [
                    dep.to_pep621_string() for dep in group.dependencies
                ]

        content["project"] = project

        # Dependency groups (PEP 735)
        if self.config.dependency_groups:
            content["dependency-groups"] = {}
            for group_name, group in self.config.dependency_groups.items():
                group_list: list[str | dict[str, str]] = []
                # Emit include-group entries first
                for included in group.include_groups:
                    group_list.append({"include-group": included})
                # Then regular dependencies
                for dep in group.dependencies:
                    group_list.append(dep.to_pep621_string())
                content["dependency-groups"][group_name] = group_list

        # Tool configurations — pass through, cleaning deprecated keys
        if self.config.tool_configs:
            tool_configs = dict(self.config.tool_configs)
            # Remove deprecated tool.uv.dev-dependencies
            if "uv" in tool_configs and isinstance(tool_configs["uv"], dict):
                tool_configs["uv"].pop("dev-dependencies", None)
                if not tool_configs["uv"]:
                    del tool_configs["uv"]
            if tool_configs:
                content["tool"] = tool_configs

        return content

    def write_to_file(self, file_path: Path, backup: bool = True) -> None:
        """Write configuration to pyproject.toml file."""
        if file_path.exists() and backup:
            backup_path = file_path.with_suffix(".toml.backup")
            shutil.copy2(file_path, backup_path)
            logger.info("Backup created: %s", backup_path)

        content = self.generate_toml_content()
        with open(file_path, "wb") as f:
            tomli_w.dump(content, f)

    def merge_with_existing(self, file_path: Path) -> ProjectConfig:
        """Merge with existing pyproject.toml file."""
        if not file_path.exists():
            return self.config

        with open(file_path, "rb") as f:
            existing_data = tomllib.load(f)

        if "project" in existing_data:
            project_data = existing_data["project"]

            if not self.config.name or self.config.name == "project-name":
                self.config.name = project_data.get("name", self.config.name)

            if not self.config.description:
                self.config.description = project_data.get(
                    "description", self.config.description
                )

            if not self.config.version or self.config.version == "0.1.0":
                self.config.version = project_data.get("version", self.config.version)

            if (
                not self.config.requires_python
                or self.config.requires_python == ">=3.12"
            ):
                self.config.requires_python = project_data.get(
                    "requires-python", self.config.requires_python
                )

            if "authors" in project_data:
                self.config.authors = project_data["authors"]

            if "license" in project_data:
                license_val = project_data["license"]
                if isinstance(license_val, dict) and "text" in license_val:
                    self.config.license = license_val["text"]
                else:
                    self.config.license = license_val

            if "keywords" in project_data:
                self.config.keywords = project_data["keywords"]

            if "classifiers" in project_data:
                self.config.classifiers = project_data["classifiers"]

            if "urls" in project_data:
                self.config.urls = project_data["urls"]

        if "tool" in existing_data:
            self.config.tool_configs = existing_data["tool"]

        return self.config


class DependencyMerger:
    """Merge dependencies from multiple sources."""

    def __init__(self, append_mode: bool = False):
        """Initialize merger with append mode."""
        self.append_mode = append_mode

    def merge_dependencies(
        self, existing: list[DependencySpec], new: list[DependencySpec]
    ) -> list[DependencySpec]:
        """Merge existing and new dependencies."""
        if not self.append_mode:
            return new

        existing_map = {dep.name: dep for dep in existing}
        for new_dep in new:
            existing_map[new_dep.name] = new_dep
        return list(existing_map.values())

    def merge_dependency_groups(
        self, existing: dict[str, DependencyGroup], new: dict[str, DependencyGroup]
    ) -> dict[str, DependencyGroup]:
        """Merge existing and new dependency groups."""
        if not self.append_mode:
            return new

        merged = existing.copy()
        for group_name, new_group in new.items():
            if group_name in merged:
                for dep in new_group.dependencies:
                    merged[group_name].add_dependency(dep)
            else:
                merged[group_name] = new_group
        return merged


class PyProjectUpdater:
    """Update existing pyproject.toml files with new dependencies."""

    def __init__(self, file_path: Path, options: Any):
        """Initialize updater with file path and options."""
        self.file_path = file_path
        self.options = options
        self.merger = DependencyMerger(append_mode=options.append)

    def update_with_dependencies(
        self,
        main_deps: list[DependencySpec],
        dev_deps: list[DependencySpec],
        test_deps: list[DependencySpec],
        docs_deps: list[DependencySpec],
        use_dependency_groups: bool = True,
    ) -> None:
        """Update pyproject.toml with new dependencies.

        Args:
            main_deps: Main runtime dependencies
            dev_deps: Development dependencies
            test_deps: Test dependencies
            docs_deps: Documentation dependencies
            use_dependency_groups: If True, use dependency-groups (PEP 735),
                otherwise use optional-dependencies (PEP 621 extras)
        """
        config = self.load_config()

        if main_deps:
            config.dependencies = self.merger.merge_dependencies(
                config.dependencies, main_deps
            )

        for deps, group_name_attr in [
            (dev_deps, "dev_group_name"),
            (test_deps, "test_group_name"),
            (docs_deps, "docs_group_name"),
        ]:
            if deps:
                name = getattr(self.options, group_name_attr)
                group = config.get_dependency_group(
                    name, use_dependency_groups=use_dependency_groups
                )
                if not group:
                    group = config.create_dependency_group(
                        name, use_dependency_groups=use_dependency_groups
                    )
                group.dependencies = self.merger.merge_dependencies(
                    group.dependencies, deps
                )

        generator = PyProjectGenerator(config)
        generator.write_to_file(self.file_path, backup=self.options.backup)

    def load_config(self) -> ProjectConfig:
        """Load project configuration from pyproject.toml."""
        if not self.file_path.exists():
            return ProjectConfig(name="project-name")

        with open(self.file_path, "rb") as f:
            data = tomllib.load(f)

        project_data = data.get("project", {})

        # Normalize license to string (PEP 639)
        license_val = project_data.get("license")
        if isinstance(license_val, dict):
            license_val = license_val.get("text", license_val.get("file"))

        config = ProjectConfig(
            name=project_data.get("name", "project-name"),
            version=project_data.get("version", "0.1.0"),
            description=project_data.get("description", ""),
            readme=project_data.get("readme"),
            requires_python=project_data.get("requires-python", ">=3.12"),
            authors=project_data.get("authors", []),
            license=license_val,
            keywords=project_data.get("keywords", []),
            classifiers=project_data.get("classifiers", []),
            urls=project_data.get("urls", {}),
        )

        # Extract dependencies
        for dep_str in project_data.get("dependencies", []):
            dep = parse_dep_string(dep_str)
            if dep:
                config.dependencies.append(dep)

        # Extract optional dependencies (PEP 621 extras)
        for group_name, deps in project_data.get("optional-dependencies", {}).items():
            group = DependencyGroup(name=group_name)
            for dep_str in deps:
                dep = parse_dep_string(dep_str)
                if dep:
                    group.add_dependency(dep)
            config.optional_dependencies[group_name] = group

        # Extract dependency groups (PEP 735)
        for group_name, items in data.get("dependency-groups", {}).items():
            group = DependencyGroup(name=group_name)
            for item in items:
                if isinstance(item, dict) and "include-group" in item:
                    group.include_groups.append(item["include-group"])
                elif isinstance(item, str):
                    dep = parse_dep_string(item)
                    if dep:
                        group.add_dependency(dep)
            config.dependency_groups[group_name] = group

        # Extract tool configurations
        if "tool" in data:
            config.tool_configs = data["tool"]

        return config
