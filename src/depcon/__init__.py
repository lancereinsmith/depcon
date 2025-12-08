"""Package for converting requirements files to pyproject.toml format.

A modern, fully-featured tool for converting legacy requirements.txt files
to the standardized pyproject.toml format with full PEP 621 support.
"""

from .cli import main
from .models import ConversionOptions, DependencySpec, ProjectConfig
from .parsers import parse_requirements_file

__version__ = "0.4.0"
__all__ = [
    "main",
    "ConversionOptions",
    "DependencySpec",
    "ProjectConfig",
    "parse_requirements_file",
]
