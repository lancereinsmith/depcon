# depcon

```
   |                             
 __|   _    _   __   __   _  _   
/  |  |/  |/ \_/    /  \_/ |/ |  
\_/|_/|__/|__/ \___/\__/   |  |_/
         /|                      
         \|                      
```

`depcon` is a tool designed to simplify the migration of dependency specifications from traditional `requirements.txt`, `requirements.in`, `requirements-dev.txt`, and `requirements-dev.in` files into the modern `pyproject.toml` format created using the [`uv`](https://docs.astral.sh/uv/) or [`hatch`](https://github.com/pypa/hatch) tools. This allows for a streamlined, standardized, and more maintainable approach to dependency management in Python projects.

## Rationale

Traditional `requirements.txt` files are widely used to manage dependencies in Python projects, but they have limitations:

- They do not natively integrate with modern Python packaging tools.
- Managing separate files for base and development dependencies can be error-prone.
- Adding, updating, or syncing dependencies requires external tools like `pip-tools`.

By migrating dependencies to `pyproject.toml`, you can leverage a unified and declarative format for dependency and project configuration. This format is now the standard for Python packaging and works seamlessly with tools like `uv`.

## Installation

You can install `depcon` via [pipx](https://pypa.github.io/pipx/) or the `uvx` plugin manager:

```bash
# Using uvx
uvx install depcon

# Using pipx
pipx install depcon
```

## Usage

`depcon` integrates into a workflow involving `uv` for project initialization and management. Here’s how you can use it:

Workflow Overview
1.	Initialize your project with uv init.
2.	Migrate your dependencies with depcon.
3.	Sync and lock your dependencies with uv sync.

## Step-by-Step Instructions

1. Initialize your Project

Start by creating a pyproject.toml file for your project using uv init:

```
uv init
```

This will create a pyproject.toml file with basic metadata for your project.

2. Migrate Dependencies with depcon

Run depcon to migrate dependencies from existing requirements files into your pyproject.toml file. For example:

* Migrate base dependencies from requirements.txt:

```
depcon -r requirements.txt
```
or 
```
depcon -r requirements.in
```

* Migrate development dependencies from requirements-dev.txt:

```
depcon -d requirements-dev.txt
```
or
```
depcon -r requirements.txt -d requirements-dev.txt
```

By default, `depcon` will add dependencies to the [project.dependencies] section for base dependencies, and to [tool.uv.dev-dependencies] for development dependencies.

3. Sync and Lock Dependencies

Once dependencies are migrated, sync and lock them with uv:

```
uv sync
```

This will resolve, install, and lock all dependencies into a uv.lock or requirements.lock file.

Additional Options

* Specify requirements.in files for pinned dependency resolution:

```
depcon -r requirements.in
```

### Benefits of this Workflow

* Unified Configuration: Manage dependencies and metadata in a single pyproject.toml file.
* Modern Tools: Leverage the power of uv and other modern packaging workflows.
* Ease of Use: Simplify the migration and maintenance of dependencies.

## Review of command line options

- `-r`, `--requirements`: Path to requirements.txt file
- `-d`, `--requirements-dev`: Path to requirements-dev.txt file
- `-p`, `--pyproject`: Path to target pyproject.toml file (default: ./pyproject.toml)
- `-a`, `--append`: Append to existing dependencies instead of overwriting them

### Examples

```bash
# Overwrite existing dependencies (default behavior)
depcon -r requirements.txt -d requirements-dev.txt -p pyproject.toml

# Append to existing dependencies
depcon -r requirements.txt -d requirements-dev.txt -p pyproject.toml --append

# Append only base requirements
depcon -r requirements.in -p pyproject.toml --append

# Append only dev requirements
depcon -d requirements-dev.txt --append
```

## Contributing

Contributions are welcome! If you’d like to improve depcon or add features, feel free to submit an issue or pull request on the GitHub repository.

## License

depcon is licensed under the MIT License. See the LICENSE file for details.