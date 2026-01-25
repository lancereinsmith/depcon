# API Reference

Manual reference for the depcon API. Source: [src/depcon/](https://github.com/lancereinsmith/depcon/blob/master/src/depcon/).

---

## depcon.models

Data models for dependency conversion.  
[models.py](https://github.com/lancereinsmith/depcon/blob/master/src/depcon/models.py)

### DependencySpec

Represents a single dependency specification (name, version_specs, extras, url, path, editable, markers).  
`to_string()`, `to_pep621_string()`.

### DependencyGroup

Represents a group of dependencies (e.g. dev, test, docs).  
`add_dependency()`, `remove_dependency()`.

### ProjectConfig

Complete project configuration (name, version, dependencies, optional_dependencies, dependency_groups, build_system, etc.).  
`add_dependency()`, `get_dependency_group()`, `create_dependency_group()`.

### ConversionOptions

Options for conversion: input files, output path, backup, append, group names, resolve, sort, build_backend, etc.

---

## depcon.parsers

Parsing of requirements file formats.  
[parsers.py](https://github.com/lancereinsmith/depcon/blob/master/src/depcon/parsers.py)

### RequirementsParser

Parser for `requirements.txt` and `requirements.in`.  
`parse()` → `list[DependencySpec]`.

### parse_requirements_file

`parse_requirements_file(file_path: Path) -> list[DependencySpec]`  
Parse a requirements file and return dependencies. Chooses `RequirementsParser` or `PipToolsParser` by content.

### group_dependencies_by_type

`group_dependencies_by_type(dependencies: list[DependencySpec]) -> dict[str, list[DependencySpec]]`  
Group dependencies into main, dev, test, docs by package-name heuristics.

---

## depcon.generators

Creation and manipulation of pyproject.toml.  
[generators.py](https://github.com/lancereinsmith/depcon/blob/master/src/depcon/generators.py)

### PyProjectGenerator

Generate pyproject.toml from `ProjectConfig`.  
`generate_toml_content()` → dict; writes to file.

### PyProjectUpdater

Update existing pyproject.toml with new dependencies.  
`update_with_dependencies(main_deps, dev_deps, test_deps, docs_deps, use_dependency_groups)`.

---

## depcon.cli

Command-line interface.  
[cli.py](https://github.com/lancereinsmith/depcon/blob/master/src/depcon/cli.py)

| Command   | Description |
|----------|-------------|
| `main`   | Click group; `depcon --version`, `depcon --help`. |
| `convert` | Convert requirements files to pyproject.toml. |
| `show`   | Show dependencies from pyproject.toml (table, json, yaml). |
| `validate` | Validate pyproject.toml dependencies. |
| `list_groups` | List all dependency groups. |
| `check`  | Check for duplicates and other issues. |
| `export` | Export dependencies to requirements.txt. |
| `diff`   | Diff pyproject.toml vs requirements files. |
| `sync`   | Sync pyproject.toml to requirements files. |

Run `depcon --help` and `depcon <command> --help` for options.
