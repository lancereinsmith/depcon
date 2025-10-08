# depcon

```text
   |                             
 __|   _    _   __   __   _  _   
/  |  |/  |/ \_/    /  \_/ |/ |  
\_/|_/|__/|__/ \___/\__/   |  |_/
         /|                      
         \|                      
```

`depcon` is a modern, fully-featured tool for converting legacy `requirements.txt` files to the standardized `pyproject.toml` format with full PEP 621 support. It provides intelligent dependency grouping, validation, and seamless integration with modern Python packaging tools like `uv`, `hatchling`, and `setuptools`.

## Features

- **🔄 Full PEP 621 Support**: Complete support for the modern Python packaging standard
- **📦 Intelligent Dependency Grouping**: Automatically categorizes dependencies into main, dev, test, and docs groups
- **🔍 Advanced Parsing**: Handles complex requirements files including pip-tools, editable installs, and URLs
- **✅ Validation**: Built-in dependency validation and error checking
- **🎯 Multiple Build Backends**: Support for hatchling, setuptools, and poetry
- **🛠️ Tool Integration**: Automatic configuration for uv, hatch, and other modern tools
- **📊 Rich CLI**: Beautiful command-line interface with progress indicators and summaries
- **🔧 Flexible Configuration**: Extensive options for customization and control

## Installation

### Using uv (Recommended)

```bash
# Install with uv
uv tool install depcon

# Or run directly without installing
uvx depcon
```

### Using pipx

```bash
pipx install depcon
```

### Using pip

```bash
pip install depcon
```

## Quick Start

### Basic Conversion

Convert a simple requirements.txt file:

```bash
depcon convert -r requirements.txt
```

### Full Project Migration

Convert multiple requirement files with proper grouping:

```bash
depcon convert \
  -r requirements.txt \
  -d requirements-dev.txt \
  -t requirements-test.txt \
  --docs-requirements requirements-docs.txt \
  --project-name "my-awesome-project" \
  --project-description "An awesome Python project"
```

## Commands

### `convert` - Convert requirements files to pyproject.toml

The main command for converting requirements files.

**Options:**

- `-r, --requirements PATH`: Requirements files to process (requirements.txt, requirements.in)
- `-d, --dev-requirements PATH`: Development requirements files to process
- `-t, --test-requirements PATH`: Test requirements files to process
- `--docs-requirements PATH`: Documentation requirements files to process
- `-o, --output PATH`: Output pyproject.toml file path (default: pyproject.toml)
- `--append / --no-append`: Append to existing dependencies instead of replacing
- `--backup / --no-backup`: Create backup of existing pyproject.toml
- `--resolve / --no-resolve`: Resolve and pin dependency versions
- `--sort / --no-sort`: Sort dependencies alphabetically
- `--build-backend [hatchling|setuptools|poetry]`: Build backend to use
- `--dev-group TEXT`: Name for development dependencies group (default: dev)
- `--test-group TEXT`: Name for test dependencies group (default: test)
- `--docs-group TEXT`: Name for documentation dependencies group (default: docs)
- `--project-name TEXT`: Project name (if creating new pyproject.toml)
- `--project-version TEXT`: Project version (if creating new pyproject.toml)
- `--project-description TEXT`: Project description (if creating new pyproject.toml)
- `--python-version TEXT`: Python version requirement (default: >=3.8)
- `-v, --verbose`: Enable verbose output

### `show` - Display dependencies from pyproject.toml

Show dependencies in a formatted table.

**Options:**

- `-f, --file PATH`: Path to pyproject.toml file (default: pyproject.toml)
- `--format [table|json|yaml]`: Output format (default: table)

### `validate` - Validate pyproject.toml dependencies

Validate that all dependencies are properly formatted.

**Options:**

- `-f, --file PATH`: Path to pyproject.toml file (default: pyproject.toml)
- `--group TEXT`: Dependency group to validate (main, dev, test, docs)

## Examples

### Basic Usage

```bash
# Convert a single requirements file
depcon convert -r requirements.txt

# Convert with development dependencies
depcon convert -r requirements.txt -d requirements-dev.txt

# Convert with all dependency types
depcon convert \
  -r requirements.txt \
  -d requirements-dev.txt \
  -t requirements-test.txt \
  --docs-requirements requirements-docs.txt
```

### Advanced Usage

```bash
# Create a new project with custom metadata
depcon convert \
  -r requirements.txt \
  --project-name "my-project" \
  --project-description "A great Python project" \
  --project-version "1.0.0" \
  --python-version ">=3.9"

# Use different build backend
depcon convert -r requirements.txt --build-backend setuptools

# Append to existing dependencies
depcon convert -r new-requirements.txt --append

# Resolve and pin versions
depcon convert -r requirements.in --resolve
```

### Viewing Dependencies

```bash
# Show dependencies in table format
depcon show

# Show in JSON format
depcon show --format json

# Show in YAML format
depcon show --format yaml
```

### Validation

```bash
# Validate all dependencies
depcon validate

# Validate specific group
depcon validate --group dev
```

## Generated pyproject.toml Structure

The tool generates modern `pyproject.toml` files following PEP 621 standards:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-project"
version = "1.0.0"
description = "A great Python project"
requires-python = ">=3.8"
dependencies = [
    "requests>=2.25.0",
    "numpy>=1.20.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]
test = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
]
docs = [
    "sphinx>=5.0.0",
    "sphinx-rtd-theme>=1.0.0",
]

[dependency-groups]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]
test = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
]
docs = [
    "sphinx>=5.0.0",
    "sphinx-rtd-theme>=1.0.0",
]

[tool.hatch.build.targets.wheel]
packages = ["src"]
```

## Supported File Formats

- `requirements.txt` - Standard pip requirements files
- `requirements.in` - pip-tools input files
- `requirements-dev.txt` - Development dependencies
- `requirements-test.txt` - Test dependencies
- `requirements-docs.txt` - Documentation dependencies
- Custom requirement files with any name

## Dependency Grouping

The tool intelligently groups dependencies based on common patterns:

- **Main Dependencies**: Core project dependencies
- **Development Dependencies**: Tools like pytest, black, ruff, mypy, pre-commit
- **Test Dependencies**: Testing frameworks and utilities
- **Documentation Dependencies**: Sphinx, mkdocs, and related tools

## Integration with Modern Tools

### uv Integration

```bash
# Initialize project with uv
uv init

# Convert dependencies
depcon convert -r requirements.txt

# Sync dependencies
uv sync
```

### Hatch Integration

```bash
# Convert with hatchling backend
depcon convert -r requirements.txt --build-backend hatchling

# Build with hatch
hatch build
```

### Poetry Integration

```bash
# Convert with poetry backend
depcon convert -r requirements.txt --build-backend poetry

# Install dependencies
poetry install
```

## Migration Workflow

1. **Backup**: The tool automatically creates backups of existing `pyproject.toml` files
2. **Convert**: Run `depcon convert` with your requirements files
3. **Validate**: Use `depcon validate` to check for issues
4. **Review**: Examine the generated `pyproject.toml` file
5. **Test**: Install dependencies and test your project
6. **Cleanup**: Remove old requirements files once satisfied

## Documentation

Comprehensive documentation is available at [https://lancereinsmith.github.io/depcon/](https://lancereinsmith.github.io/depcon/).

- **[Installation Guide](https://lancereinsmith.github.io/depcon/installation.html)** - Detailed installation instructions
- **[Quick Start](https://lancereinsmith.github.io/depcon/quickstart.html)** - Get up and running quickly
- **[User Guide](https://lancereinsmith.github.io/depcon/user_guide.html)** - Complete feature reference
- **[API Reference](https://lancereinsmith.github.io/depcon/api_reference.html)** - Detailed API documentation
- **[Examples](https://lancereinsmith.github.io/depcon/examples.html)** - Real-world usage examples
- **[Contributing](https://lancereinsmith.github.io/depcon/contributing.html)** - How to contribute to the project

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTORS.md) and [Development Guide](DEVELOPMENT.md) for details.

### Quick Development Setup

```bash
# Clone the repository
git clone https://github.com/lancereinsmith/depcon.git
cd depcon

# Install in development mode
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run all checks
make check
```

## License

depcon is licensed under the MIT License. See the LICENSE file for details.

## Changelog

### v0.2.0 (Latest)
- Complete rewrite with modern architecture
- Full PEP 621 support
- Intelligent dependency grouping
- Rich CLI interface
- Advanced validation
- Multiple build backend support
- Tool integration (uv, hatch, poetry)

### v0.1.x (Legacy)
- Basic requirements.txt to pyproject.toml conversion
- Limited feature set