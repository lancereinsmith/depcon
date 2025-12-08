"""PyProject.toml generation and manipulation."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any, Dict, List

from .models import DependencyGroup, DependencySpec, ProjectConfig


class PyProjectGenerator:
    """Generate and manipulate pyproject.toml files."""

    def __init__(self, config: ProjectConfig):
        """Initialize generator with project configuration."""
        self.config = config

    def generate_toml_content(self) -> Dict[str, Any]:
        """Generate TOML content from project configuration."""
        content = {}

        # Build system
        content["build-system"] = self.config.build_system

        # Project metadata
        project = {
            "name": self.config.name,
            "version": self.config.version,
            "description": self.config.description,
            "requires-python": self.config.requires_python,
        }

        # Add optional fields
        if self.config.readme:
            project["readme"] = self.config.readme

        if self.config.authors:
            project["authors"] = self.config.authors

        if self.config.license:
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

        # Optional dependencies (PEP 621 extras - installable features)
        if self.config.optional_dependencies:
            project["optional-dependencies"] = {}
            for group_name, group in self.config.optional_dependencies.items():
                project["optional-dependencies"][group_name] = [
                    dep.to_pep621_string() for dep in group.dependencies
                ]

        content["project"] = project

        # Dependency groups (PEP 735 - for uv, etc., not installable extras)
        if self.config.dependency_groups:
            content["dependency-groups"] = {}
            for group_name, group in self.config.dependency_groups.items():
                content["dependency-groups"][group_name] = [
                    dep.to_pep621_string() for dep in group.dependencies
                ]

        # Tool configurations (do not emit deprecated tool.uv.dev-dependencies)
        if self.config.tool_configs:
            # Remove any deprecated uv dev-dependencies if present
            tool_configs = dict(self.config.tool_configs)
            if "uv" in tool_configs and isinstance(tool_configs["uv"], dict):
                tool_configs["uv"].pop("dev-dependencies", None)
                if not tool_configs["uv"]:
                    # keep empty table if user expects [tool.uv], else it would be dropped
                    tool_configs["uv"] = {}
            content["tool"] = tool_configs

        return content

    def write_to_file(self, file_path: Path, backup: bool = True) -> None:
        """Write configuration to pyproject.toml file."""
        if file_path.exists() and backup:
            backup_path = file_path.with_suffix(".toml.backup")
            shutil.copy2(file_path, backup_path)
            print(f"Backup created: {backup_path}")

        content = self.generate_toml_content()

        # Write TOML content
        try:
            import tomli_w

            with open(file_path, "wb") as f:
                tomli_w.dump(content, f)
        except ImportError:
            # Fallback to toml library
            try:
                import toml

                with open(file_path, "w", encoding="utf-8") as f:
                    toml.dump(content, f)
            except ImportError:
                # Last resort: write basic TOML manually
                self._write_toml_manually(content, file_path)

    def merge_with_existing(self, file_path: Path) -> ProjectConfig:
        """Merge with existing pyproject.toml file."""
        if not file_path.exists():
            return self.config

        try:
            import tomli

            with open(file_path, "rb") as f:
                existing_data = tomli.load(f)
        except ImportError:
            try:
                import toml

                with open(file_path, "r", encoding="utf-8") as f:
                    existing_data = toml.load(f)
            except ImportError:
                # If no TOML library is available, return empty config
                return self.config

        # Merge project metadata
        if "project" in existing_data:
            project_data = existing_data["project"]

            # Update basic fields if not set
            if not self.config.name or self.config.name == "project-name":
                self.config.name = project_data.get("name", self.config.name)

            if not self.config.description or self.config.description == "":
                self.config.description = project_data.get(
                    "description", self.config.description
                )

            if not self.config.version or self.config.version == "0.1.0":
                self.config.version = project_data.get("version", self.config.version)

            if (
                not self.config.requires_python
                or self.config.requires_python == ">=3.8"
            ):
                self.config.requires_python = project_data.get(
                    "requires-python", self.config.requires_python
                )

            # Merge other metadata
            if "authors" in project_data:
                self.config.authors = project_data["authors"]

            if "license" in project_data:
                self.config.license = project_data["license"]

            if "keywords" in project_data:
                self.config.keywords = project_data["keywords"]

            if "classifiers" in project_data:
                self.config.classifiers = project_data["classifiers"]

            if "urls" in project_data:
                self.config.urls = project_data["urls"]

        # Merge tool configurations
        if "tool" in existing_data:
            self.config.tool_configs = existing_data["tool"]

        return self.config


class DependencyMerger:
    """Merge dependencies from multiple sources."""

    def __init__(self, append_mode: bool = False):
        """Initialize merger with append mode."""
        self.append_mode = append_mode

    def merge_dependencies(
        self, existing: List[DependencySpec], new: List[DependencySpec]
    ) -> List[DependencySpec]:
        """Merge existing and new dependencies."""
        if not self.append_mode:
            return new

        # Create a map of existing dependencies by name
        existing_map = {dep.name: dep for dep in existing}

        # Merge new dependencies
        for new_dep in new:
            if new_dep.name in existing_map:
                # Update existing dependency
                existing_map[new_dep.name] = new_dep
            else:
                # Add new dependency
                existing_map[new_dep.name] = new_dep

        return list(existing_map.values())

    def merge_dependency_groups(
        self, existing: Dict[str, DependencyGroup], new: Dict[str, DependencyGroup]
    ) -> Dict[str, DependencyGroup]:
        """Merge existing and new dependency groups."""
        if not self.append_mode:
            return new

        # Start with existing groups
        merged = existing.copy()

        # Merge new groups
        for group_name, new_group in new.items():
            if group_name in merged:
                # Merge dependencies within the group
                existing_group = merged[group_name]
                for dep in new_group.dependencies:
                    existing_group.add_dependency(dep)
            else:
                # Add new group
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
        main_deps: List[DependencySpec],
        dev_deps: List[DependencySpec],
        test_deps: List[DependencySpec],
        docs_deps: List[DependencySpec],
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
        # Load existing configuration
        config = self._load_existing_config()

        # Merge main dependencies
        if main_deps:
            config.dependencies = self.merger.merge_dependencies(
                config.dependencies, main_deps
            )

        # Merge development dependencies
        if dev_deps:
            dev_group = config.get_dependency_group(
                self.options.dev_group_name, use_dependency_groups=use_dependency_groups
            )
            if not dev_group:
                dev_group = config.create_dependency_group(
                    self.options.dev_group_name,
                    "Development dependencies",
                    use_dependency_groups=use_dependency_groups,
                )

            existing_dev_deps = dev_group.dependencies
            dev_group.dependencies = self.merger.merge_dependencies(
                existing_dev_deps, dev_deps
            )

        # Merge test dependencies
        if test_deps:
            test_group = config.get_dependency_group(
                self.options.test_group_name, use_dependency_groups=use_dependency_groups
            )
            if not test_group:
                test_group = config.create_dependency_group(
                    self.options.test_group_name,
                    "Test dependencies",
                    use_dependency_groups=use_dependency_groups,
                )

            existing_test_deps = test_group.dependencies
            test_group.dependencies = self.merger.merge_dependencies(
                existing_test_deps, test_deps
            )

        # Merge documentation dependencies
        if docs_deps:
            docs_group = config.get_dependency_group(
                self.options.docs_group_name, use_dependency_groups=use_dependency_groups
            )
            if not docs_group:
                docs_group = config.create_dependency_group(
                    self.options.docs_group_name,
                    "Documentation dependencies",
                    use_dependency_groups=use_dependency_groups,
                )

            existing_docs_deps = docs_group.dependencies
            docs_group.dependencies = self.merger.merge_dependencies(
                existing_docs_deps, docs_deps
            )

        # Update tool configurations
        self._update_tool_configs(config)

        # Write updated configuration
        generator = PyProjectGenerator(config)
        generator.write_to_file(self.file_path, backup=self.options.backup)

    def _load_existing_config(self) -> ProjectConfig:
        """Load existing project configuration."""
        if not self.file_path.exists():
            return ProjectConfig(name="project-name")

        data = None

        # Try different TOML libraries in order of preference
        try:
            # Python 3.11+ built-in tomllib
            import tomllib

            with open(self.file_path, "rb") as f:
                data = tomllib.load(f)
        except ImportError:
            try:
                # tomli (faster, more modern)
                import tomli

                with open(self.file_path, "rb") as f:
                    data = tomli.load(f)
            except ImportError:
                try:
                    # toml (older, more compatible)
                    import toml

                    with open(self.file_path, "r", encoding="utf-8") as f:
                        data = toml.load(f)
                except ImportError:
                    # If no TOML library is available, return empty config
                    return ProjectConfig(name="project-name")

        if data is None:
            return ProjectConfig(name="project-name")

        # Extract project metadata
        project_data = data.get("project", {})

        config = ProjectConfig(
            name=project_data.get("name", "project-name"),
            version=project_data.get("version", "0.1.0"),
            description=project_data.get("description", ""),
            readme=project_data.get("readme"),
            requires_python=project_data.get("requires-python", ">=3.8"),
            authors=project_data.get("authors", []),
            license=project_data.get("license"),
            keywords=project_data.get("keywords", []),
            classifiers=project_data.get("classifiers", []),
            urls=project_data.get("urls", {}),
        )

        # Extract dependencies
        if "dependencies" in project_data:
            # Convert dependency strings back to DependencySpec objects
            for dep_str in project_data["dependencies"]:
                try:
                    from packaging.requirements import Requirement

                    req = Requirement(dep_str)
                    dep = DependencySpec(
                        name=req.name,
                        version_specs=(
                            [str(spec) for spec in req.specifier]
                            if req.specifier
                            else []
                        ),
                        extras=list(req.extras),
                        markers=str(req.marker) if req.marker else None,
                    )
                    config.dependencies.append(dep)
                except Exception:
                    # Skip invalid dependencies
                    continue

        # Extract optional dependencies (PEP 621 extras)
        if "optional-dependencies" in project_data:
            for group_name, deps in project_data["optional-dependencies"].items():
                group = DependencyGroup(name=group_name)
                for dep_str in deps:
                    try:
                        from packaging.requirements import Requirement

                        req = Requirement(dep_str)
                        dep = DependencySpec(
                            name=req.name,
                            version_specs=(
                                [str(spec) for spec in req.specifier]
                                if req.specifier
                                else []
                            ),
                            extras=list(req.extras),
                            markers=str(req.marker) if req.marker else None,
                        )
                        group.add_dependency(dep)
                    except Exception:
                        # Skip invalid dependencies
                        continue
                config.optional_dependencies[group_name] = group

        # Extract dependency groups (PEP 735)
        if "dependency-groups" in data:
            for group_name, deps in data["dependency-groups"].items():
                group = DependencyGroup(name=group_name)
                for dep_str in deps:
                    try:
                        from packaging.requirements import Requirement

                        req = Requirement(dep_str)
                        dep = DependencySpec(
                            name=req.name,
                            version_specs=(
                                [str(spec) for spec in req.specifier]
                                if req.specifier
                                else []
                            ),
                            extras=list(req.extras),
                            markers=str(req.marker) if req.marker else None,
                        )
                        group.add_dependency(dep)
                    except Exception:
                        # Skip invalid dependencies
                        continue
                config.dependency_groups[group_name] = group

        # Extract tool configurations
        if "tool" in data:
            config.tool_configs = data["tool"]

        return config

    def _update_tool_configs(self, config: ProjectConfig) -> None:
        """Update tool-specific configurations."""
        if self.options.enable_uv:
            # No longer write deprecated tool.uv.dev-dependencies; uv reads dependency-groups
            if "uv" not in config.tool_configs:
                config.tool_configs["uv"] = {}

        if self.options.enable_hatch:
            if "hatch" not in config.tool_configs:
                config.tool_configs["hatch"] = {}

            # Add build configuration
            config.tool_configs["hatch"]["build"] = {
                "targets": {"wheel": {"packages": ["src"]}}
            }

    def _write_toml_manually(self, content: Dict[str, Any], file_path: Path) -> None:
        """Write TOML content manually as a fallback."""
        lines = []

        # Write build-system
        if "build-system" in content:
            lines.append("[build-system]")
            for key, value in content["build-system"].items():
                if isinstance(value, list):
                    lines.append(f"{key} = {value}")
                else:
                    lines.append(f'{key} = "{value}"')
            lines.append("")

        # Write project section
        if "project" in content:
            lines.append("[project]")
            project = content["project"]

            # Basic fields
            for field in [
                "name",
                "version",
                "description",
                "readme",
                "requires-python",
            ]:
                if field in project:
                    value = project[field]
                    if isinstance(value, str):
                        lines.append(f'{field} = "{value}"')
                    else:
                        lines.append(f"{field} = {value}")

            # Dependencies
            if "dependencies" in project and project["dependencies"]:
                lines.append("dependencies = [")
                for dep in project["dependencies"]:
                    lines.append(f'    "{dep}",')
                lines.append("]")

            # Optional dependencies
            if "optional-dependencies" in project and project["optional-dependencies"]:
                lines.append("")
                lines.append("[project.optional-dependencies]")
                for group_name, deps in project["optional-dependencies"].items():
                    lines.append(f"{group_name} = [")
                    for dep in deps:
                        lines.append(f'    "{dep}",')
                    lines.append("]")

            lines.append("")

        # Write tool sections
        if "tool" in content:
            for tool_name, tool_config in content["tool"].items():
                lines.append(f"[tool.{tool_name}]")
                for key, value in tool_config.items():
                    if isinstance(value, dict):
                        lines.append(f"[tool.{tool_name}.{key}]")
                        for sub_key, sub_value in value.items():
                            if isinstance(sub_value, list):
                                lines.append(f"{sub_key} = {sub_value}")
                            else:
                                lines.append(f'{sub_key} = "{sub_value}"')
                    elif isinstance(value, list):
                        lines.append(f"{key} = {value}")
                    else:
                        lines.append(f'{key} = "{value}"')
                lines.append("")

        # Write dependency-groups (PEP 735 - uv modern config)
        if "dependency-groups" in content and content["dependency-groups"]:
            lines.append("[dependency-groups]")
            for group_name, deps in content["dependency-groups"].items():
                lines.append(f"{group_name} = [")
                for dep in deps:
                    lines.append(f'    "{dep}",')
                lines.append("]")
            lines.append("")

        # Write to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
