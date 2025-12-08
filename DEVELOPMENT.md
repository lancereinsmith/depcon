# Development Guide

This guide covers everything you need to know to contribute to depcon development.

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Git
- uv (recommended) or pip

### Setup

1. **Fork and clone the repository:**

   ```bash
   git clone https://github.com/your-username/depcon.git
   cd depcon
   ```

2. **Install in development mode:**

   ```bash
   # Using uv (recommended)
   uv pip install -e ".[dev]"

   # Or using pip
   pip install -e ".[dev]"
   ```

3. **Install pre-commit hooks:**

   ```bash
   pre-commit install
   ```

4. **Verify installation:**

   ```bash
   depcon --version
   pytest
   ```

## Development Environment

### Recommended Tools

- **uv**: Fast Python package manager
- **pre-commit**: Git hooks for code quality
- **VS Code**: With Python extension
- **Git**: Version control

### IDE Configuration

#### VS Code

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.ruff.enabled": true,
    "python.linting.mypy.enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

#### PyCharm

1. Open project in PyCharm
2. Configure Python interpreter to use virtual environment
3. Enable ruff and mypy inspections
4. Configure black as code formatter

## Code Quality

### Linting and Formatting

We use several tools to maintain code quality:

- **ruff**: Fast Python linter
- **black**: Code formatter
- **mypy**: Type checker
- **pre-commit**: Git hooks

Run all checks:

```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Or run individually
ruff check src/ tests/
black src/ tests/
mypy src/
```

### Code Style

- Follow PEP 8
- Use type hints for all functions
- Write docstrings for all public functions
- Use meaningful variable names
- Keep functions small and focused

### Pre-commit Hooks

Pre-commit hooks run automatically on commit:

```bash
# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files

# Skip hooks (not recommended)
git commit --no-verify
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=depcon

# Run specific test file
pytest tests/test_models.py

# Run specific test
pytest tests/test_models.py::TestDependencySpec::test_basic_dependency

# Run with verbose output
pytest -v

# Run in parallel
pytest -n auto
```

### Writing Tests

Follow these guidelines:

1. **Test structure:**

   ```python
   def test_function_name():
       """Test description."""
       # Arrange
       input_data = "test"

       # Act
       result = function_under_test(input_data)

       # Assert
       assert result == expected_output
   ```

2. **Use fixtures for common data:**

   ```python
   @pytest.fixture
   def sample_requirements_file(tmp_path):
       """Create sample requirements file."""
       req_file = tmp_path / "requirements.txt"
       req_file.write_text("requests>=2.25.0\n")
       return req_file
   ```

3. **Test both success and failure cases:**

   ```python
   def test_valid_input():
       """Test with valid input."""
       assert function("valid") == expected

   def test_invalid_input():
       """Test with invalid input."""
       with pytest.raises(ValueError):
           function("invalid")
   ```

### Test Coverage

We aim for high test coverage:

```bash
# Generate coverage report
pytest --cov=depcon --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Documentation

### Building Documentation

```bash
# Install docs dependencies
uv pip install -e ".[docs]"

# Build HTML docs
cd docs
make html

# View docs
open _build/html/index.html
```

### Writing Documentation

- Use reStructuredText (RST) format
- Include code examples
- Use proper cross-references
- Follow the existing structure

## Git Workflow

### Branching

1. **Create feature branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and commit:**

   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

3. **Push and create PR:**

   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Messages

Follow conventional commits:

```text
type(scope): description

[optional body]

[optional footer]
```

Types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `ci`: CI/CD changes
- `chore`: Maintenance tasks

Examples:

```text
feat(parser): add support for pip-tools requirements.in files

fix(cli): handle missing requirements files gracefully

docs: update installation instructions
```

## Release Process

### Version Bumping

1. Update version in `pyproject.toml`
2. Update `__version__` in `__init__.py`
3. Update changelog
4. Create release commit
5. Tag release
6. Push tags

### Pre-release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version bumped
- [ ] No linting errors
- [ ] Type checking passes

## Debugging

### Common Issues

**Import Errors:**

```bash
# Ensure package is installed in dev mode
uv pip install -e ".[dev]"

# Check Python path
python -c "import sys; print(sys.path)"
```

**Test Failures:**

```bash
# Run with verbose output
pytest -v -s

# Run specific test with debugging
pytest -v -s tests/test_specific.py::test_function
```

**Linting Errors:**

```bash
# Fix auto-fixable issues
ruff check src/ --fix

# Check specific file
ruff check src/specific_file.py
```

### Debugging Tools

**pdb:**

```python
import pdb; pdb.set_trace()
```

**ipdb:**

```python
import ipdb; ipdb.set_trace()
```

**VS Code Debugger:**

- Set breakpoints in code
- Use "Debug Python File" option

## Performance

### Profiling

```bash
# Install profiling tools
uv pip install line_profiler memory_profiler

# Profile function
python -m line_profiler script.py

# Memory profiling
python -m memory_profiler script.py
```

### Benchmarking

```bash
# Install pytest-benchmark
uv pip install pytest-benchmark

# Run benchmarks
pytest --benchmark-only
```

## Contributing

### Pull Request Process

1. Fork repository
2. Create feature branch
3. Make changes
4. Write tests
5. Update documentation
6. Run all checks
7. Submit PR

### Code Review

- Review code for correctness
- Check test coverage
- Verify documentation
- Ensure performance is acceptable
- Check for security issues

## Getting Help

- Check existing issues
- Ask in discussions
- Create new issue
- Join community chat

## Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Pre-commit Hooks](https://pre-commit.com/)
