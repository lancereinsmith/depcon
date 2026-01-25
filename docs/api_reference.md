# API Reference

This section provides detailed documentation for the depcon API. The API is organized into several modules.

## depcon.models

The models module contains the core data structures used by depcon.

::: depcon.models
    options:
      show_root_heading: true
      show_symbol_type_heading: true

### DependencySpec

::: depcon.models.DependencySpec
    options:
      show_root_heading: true

### DependencyGroup

::: depcon.models.DependencyGroup
    options:
      show_root_heading: true

### ProjectConfig

::: depcon.models.ProjectConfig
    options:
      show_root_heading: true

### ConversionOptions

::: depcon.models.ConversionOptions
    options:
      show_root_heading: true

## depcon.parsers

The parsers module handles parsing of various requirements file formats.

::: depcon.parsers
    options:
      show_root_heading: true
      show_symbol_type_heading: true

### RequirementsParser

::: depcon.parsers.RequirementsParser
    options:
      show_root_heading: true

### parse_requirements_file

::: depcon.parsers.parse_requirements_file

### group_dependencies_by_type

::: depcon.parsers.group_dependencies_by_type

## depcon.generators

The generators module handles creation and manipulation of pyproject.toml files.

::: depcon.generators
    options:
      show_root_heading: true
      show_symbol_type_heading: true

### PyProjectGenerator

::: depcon.generators.PyProjectGenerator
    options:
      show_root_heading: true

### PyProjectUpdater

::: depcon.generators.PyProjectUpdater
    options:
      show_root_heading: true

## depcon.cli

The CLI module provides the command-line interface for depcon.

::: depcon.cli
    options:
      show_root_heading: true
      show_symbol_type_heading: true

### main

::: depcon.cli.main

### convert

::: depcon.cli.convert

### show

::: depcon.cli.show

### validate

::: depcon.cli.validate

## Exceptions

depcon uses standard Python exceptions for error handling. No custom exceptions are defined.

## Constants

No module-level constants are defined in depcon.
