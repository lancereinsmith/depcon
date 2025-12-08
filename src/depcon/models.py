"""Data models for dependency conversion."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class DependencySpec(BaseModel):
    """Represents a single dependency specification."""

    name: str = Field(..., description="Package name")
    version_specs: List[str] = Field(
        default_factory=list, description="Version specifications"
    )
    extras: List[str] = Field(default_factory=list, description="Package extras")
    url: Optional[str] = Field(None, description="Direct URL to package")
    path: Optional[str] = Field(None, description="Local path to package")
    editable: bool = Field(False, description="Whether this is an editable install")
    markers: Optional[str] = Field(None, description="Environment markers")

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        """Validate package name format."""
        if not v or not v.strip():
            raise ValueError("Package name cannot be empty")
        return v.strip().lower()

    @field_validator("version_specs")
    def validate_version_specs(cls, v: List[str]) -> List[str]:
        """Validate version specifications."""
        for spec in v:
            if not re.match(r"^[<>=!~]+[0-9]", spec):
                raise ValueError(f"Invalid version spec: {spec}")
        return v

    def to_string(self) -> str:
        """Convert to pip-compatible string format."""
        parts = [self.name]

        if self.extras:
            parts[0] += f"[{','.join(self.extras)}]"

        if self.version_specs:
            parts.extend(self.version_specs)

        if self.url:
            parts.append(f" @ {self.url}")
        elif self.path:
            prefix = "-e " if self.editable else ""
            parts = [f"{prefix}{self.path}"]

        if self.markers:
            parts.append(f"; {self.markers}")

        return "".join(parts)

    def to_pep621_string(self) -> str:
        """Convert to PEP 621 compatible string format."""
        return self.to_string()


class DependencyGroup(BaseModel):
    """Represents a group of dependencies (e.g., dev, test, docs)."""

    name: str = Field(..., description="Group name")
    dependencies: List[DependencySpec] = Field(
        default_factory=list, description="Dependencies in this group"
    )
    description: Optional[str] = Field(
        None, description="Optional description of the group"
    )

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        """Validate group name."""
        if not v or not v.strip():
            raise ValueError("Group name cannot be empty")
        return v.strip().lower()

    def add_dependency(self, dep: DependencySpec) -> None:
        """Add a dependency to this group."""
        # Check if dependency already exists and update if needed
        for i, existing in enumerate(self.dependencies):
            if existing.name == dep.name:
                self.dependencies[i] = dep
                return
        self.dependencies.append(dep)

    def remove_dependency(self, name: str) -> bool:
        """Remove a dependency by name."""
        for i, dep in enumerate(self.dependencies):
            if dep.name == name:
                del self.dependencies[i]
                return True
        return False


class ProjectConfig(BaseModel):
    """Represents a complete project configuration."""

    name: str = Field(..., description="Project name")
    version: str = Field(default="0.1.0", description="Project version")
    description: str = Field(default="", description="Project description")
    readme: Optional[str] = Field(None, description="Path to README file")
    requires_python: str = Field(
        default=">=3.8", description="Python version requirement"
    )
    authors: List[Dict[str, str]] = Field(
        default_factory=list, description="Project authors"
    )
    license: Optional[Dict[str, str]] = Field(None, description="Project license")
    keywords: List[str] = Field(default_factory=list, description="Project keywords")
    classifiers: List[str] = Field(
        default_factory=list, description="Project classifiers"
    )
    urls: Dict[str, str] = Field(default_factory=dict, description="Project URLs")

    # Dependencies
    dependencies: List[DependencySpec] = Field(
        default_factory=list, description="Main dependencies"
    )
    optional_dependencies: Dict[str, DependencyGroup] = Field(
        default_factory=dict, description="Optional dependency groups (PEP 621 extras)"
    )
    dependency_groups: Dict[str, DependencyGroup] = Field(
        default_factory=dict, description="Dependency groups (PEP 735, for uv, etc.)"
    )

    # Build system
    build_system: Dict[str, Any] = Field(
        default_factory=lambda: {
            "requires": ["hatchling"],
            "build-backend": "hatchling.build",
        },
        description="Build system configuration",
    )

    # Tool-specific configurations
    tool_configs: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict, description="Tool-specific configurations"
    )

    def add_dependency(
        self,
        dep: DependencySpec,
        group: Optional[str] = None,
        use_dependency_groups: bool = True,
    ) -> None:
        """Add a dependency to the project.
        
        Args:
            dep: The dependency to add
            group: Optional group name (dev, test, docs, etc.)
            use_dependency_groups: If True, use dependency-groups (PEP 735),
                otherwise use optional-dependencies (PEP 621 extras)
        """
        if group:
            if use_dependency_groups:
                target_dict = self.dependency_groups
            else:
                target_dict = self.optional_dependencies
                
            if group not in target_dict:
                target_dict[group] = DependencyGroup(name=group)
            target_dict[group].add_dependency(dep)
        else:
            # Check if dependency already exists and update if needed
            for i, existing in enumerate(self.dependencies):
                if existing.name == dep.name:
                    self.dependencies[i] = dep
                    return
            self.dependencies.append(dep)

    def get_dependency_group(
        self, name: str, use_dependency_groups: bool = True
    ) -> Optional[DependencyGroup]:
        """Get a dependency group by name.
        
        Args:
            name: Group name
            use_dependency_groups: If True, check dependency-groups,
                otherwise check optional-dependencies
        """
        if use_dependency_groups:
            return self.dependency_groups.get(name)
        return self.optional_dependencies.get(name)

    def create_dependency_group(
        self,
        name: str,
        description: Optional[str] = None,
        use_dependency_groups: bool = True,
    ) -> DependencyGroup:
        """Create a new dependency group.
        
        Args:
            name: Group name
            description: Optional description
            use_dependency_groups: If True, create in dependency-groups,
                otherwise in optional-dependencies
        """
        group = DependencyGroup(name=name, description=description)
        if use_dependency_groups:
            self.dependency_groups[name] = group
        else:
            self.optional_dependencies[name] = group
        return group


class ConversionOptions(BaseModel):
    """Options for dependency conversion."""

    # Input files
    requirements_files: List[Path] = Field(
        default_factory=list, description="Requirements files to process"
    )
    requirements_in_files: List[Path] = Field(
        default_factory=list, description="Requirements.in files to process"
    )

    # Output configuration
    output_file: Path = Field(
        default=Path("pyproject.toml"), description="Output pyproject.toml file"
    )
    backup: bool = Field(
        default=True, description="Create backup of existing pyproject.toml"
    )
    append: bool = Field(
        default=False,
        description="Append to existing dependencies instead of replacing",
    )

    # Dependency grouping
    dev_group_name: str = Field(
        default="dev", description="Name for development dependencies group"
    )
    test_group_name: str = Field(
        default="test", description="Name for test dependencies group"
    )
    docs_group_name: str = Field(
        default="docs", description="Name for documentation dependencies group"
    )

    # Processing options
    resolve_dependencies: bool = Field(
        default=False, description="Resolve and pin dependency versions"
    )
    include_hashes: bool = Field(default=False, description="Include package hashes")
    sort_dependencies: bool = Field(
        default=True, description="Sort dependencies alphabetically"
    )

    # Build system
    build_backend: str = Field(default="hatchling", description="Build backend to use")
    build_requires: List[str] = Field(
        default_factory=lambda: ["hatchling"], description="Build system requirements"
    )

    # Tool configurations
    enable_uv: bool = Field(default=True, description="Enable uv tool configuration")
    enable_hatch: bool = Field(
        default=True, description="Enable hatch tool configuration"
    )

    @field_validator("requirements_files", "requirements_in_files")
    def validate_files_exist(cls, v: List[Path]) -> List[Path]:
        """Validate that input files exist."""
        for file_path in v:
            if not file_path.exists():
                raise ValueError(f"File does not exist: {file_path}")
        return v
