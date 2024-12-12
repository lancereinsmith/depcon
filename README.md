# depcon

Convert requirements files to pyproject.toml format.

## Installation

```
pipx install depcon
```

or 

```
uvx install depcon
```

## Usage

```
depcon -r requirements.txt -d requirements-dev.txt -p pyproject.toml
depcon -r requirements.in -p pyproject.toml
depcon -r requirements.txt 
```

## Options

- `-r`, `--requirements`: Path to requirements.txt file
- `-d`, `--requirements-dev`: Path to requirements-dev.txt file
- `-p`, `--pyproject`: Path to target pyproject.toml file (default: ./pyproject.toml)
