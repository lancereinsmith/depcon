Contributing
=============

We welcome contributions to depcon! This guide will help you get started with contributing to the project.

Getting Started
---------------

Fork and Clone
~~~~~~~~~~~~~~

1. Fork the repository on GitHub
2. Clone your fork locally:

.. code-block:: bash

   git clone https://github.com/your-username/depcon.git
   cd depcon

Development Setup
~~~~~~~~~~~~~~~~~

Set up your development environment:

.. code-block:: bash

   # Install uv (recommended)
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Or install with pip
   pip install uv

   # Install in development mode
   uv pip install -e ".[dev]"

   # Install pre-commit hooks
   pre-commit install

Alternative setup with pip:

.. code-block:: bash

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install in development mode
   pip install -e ".[dev]"

   # Install pre-commit hooks
   pre-commit install

Running Tests
~~~~~~~~~~~~~

Run the test suite:

.. code-block:: bash

   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=depcon

   # Run specific test file
   pytest tests/test_models.py

   # Run with verbose output
   pytest -v

Linting and Formatting
~~~~~~~~~~~~~~~~~~~~~~

Check code quality:

.. code-block:: bash

   # Run ruff linter
   ruff check src/

   # Fix auto-fixable issues
   ruff check src/ --fix

   # Run black formatter
   black src/

   # Check with mypy
   mypy src/

   # Run all checks
   pre-commit run --all-files

Development Workflow
--------------------

Branching
~~~~~~~~~

1. Create a feature branch from main:

.. code-block:: bash

   git checkout -b feature/your-feature-name

2. Make your changes
3. Write tests for new functionality
4. Ensure all tests pass
5. Commit your changes with descriptive messages

Commit Messages
~~~~~~~~~~~~~~~

Follow conventional commit format:

.. code-block:: text

   type(scope): description

   [optional body]

   [optional footer]

Examples:

.. code-block:: text

   feat(parser): add support for pip-tools requirements.in files

   fix(cli): handle missing requirements files gracefully

   docs: update installation instructions

   test(models): add tests for DependencySpec validation

Types:
- ``feat``: New feature
- ``fix``: Bug fix
- ``docs``: Documentation changes
- ``test``: Test changes
- ``refactor``: Code refactoring
- ``perf``: Performance improvements
- ``ci``: CI/CD changes
- ``chore``: Maintenance tasks

Code Style
----------

Python Code
~~~~~~~~~~~

Follow PEP 8 and use the configured tools:

* **Black**: Code formatting (88 character line length)
* **Ruff**: Linting and import sorting
* **MyPy**: Type checking
* **Pre-commit**: Automated checks

Configuration is in ``pyproject.toml``.

Documentation
~~~~~~~~~~~~~

* Use reStructuredText for Sphinx documentation
* Follow the existing documentation structure
* Include docstrings for all public functions and classes
* Use type hints for better documentation

Testing
-------

Test Structure
~~~~~~~~~~~~~~

Tests are organized in the ``tests/`` directory:

.. code-block:: text

   tests/
   ├── test_models.py      # Tests for data models
   ├── test_parsers.py     # Tests for parsers
   ├── test_generators.py  # Tests for generators
   └── test_cli.py         # Tests for CLI

Writing Tests
~~~~~~~~~~~~~

Follow these guidelines:

* Use descriptive test names
* Test both success and failure cases
* Use fixtures for common test data
* Mock external dependencies
* Aim for high test coverage

Example test:

.. code-block:: python

   def test_dependency_spec_creation():
       """Test that DependencySpec can be created with valid data."""
       dep = DependencySpec(name="requests", version_specs=[">=2.25.0"])
       
       assert dep.name == "requests"
       assert dep.version_specs == [">=2.25.0"]
       assert dep.extras == []
       assert dep.url is None

Test Fixtures
~~~~~~~~~~~~~

Use pytest fixtures for common test data:

.. code-block:: python

   @pytest.fixture
   def sample_requirements_file(tmp_path):
       """Create a sample requirements.txt file for testing."""
       req_file = tmp_path / "requirements.txt"
       req_file.write_text("requests>=2.25.0\nnumpy>=1.20.0\n")
       return req_file

Running Specific Tests
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Run specific test
   pytest tests/test_models.py::TestDependencySpec::test_basic_dependency

   # Run tests matching pattern
   pytest -k "test_dependency"

   # Run tests in specific file
   pytest tests/test_models.py

   # Run with coverage
   pytest --cov=depcon --cov-report=html

Pull Request Process
--------------------

Before Submitting
~~~~~~~~~~~~~~~~~

1. Ensure all tests pass
2. Run linting and formatting tools
3. Update documentation if needed
4. Add tests for new functionality
5. Update changelog if applicable

Creating a Pull Request
~~~~~~~~~~~~~~~~~~~~~~~

1. Push your branch to your fork
2. Create a pull request on GitHub
3. Fill out the pull request template
4. Link any related issues
5. Request review from maintainers

Pull Request Template
~~~~~~~~~~~~~~~~~~~~~

Use this template for pull requests:

.. code-block:: text

   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - [ ] Tests pass locally
   - [ ] New tests added for new functionality
   - [ ] All existing tests still pass

   ## Checklist
   - [ ] Code follows project style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] Changelog updated (if applicable)

Issue Reporting
---------------

Bug Reports
~~~~~~~~~~~

When reporting bugs, include:

* Python version
* depcon version
* Operating system
* Steps to reproduce
* Expected behavior
* Actual behavior
* Error messages/logs

Feature Requests
~~~~~~~~~~~~~~~~

For feature requests, include:

* Use case description
* Proposed solution
* Alternative solutions considered
* Additional context

Development Guidelines
------------------------

Architecture
~~~~~~~~~~~~

depcon follows a modular architecture:

* **models**: Data structures and validation
* **parsers**: Requirements file parsing
* **generators**: PyProject.toml generation
* **cli**: Command-line interface

Adding New Features
~~~~~~~~~~~~~~~~~~~

1. Design the feature
2. Update data models if needed
3. Implement parsing/generation logic
4. Add CLI commands
5. Write comprehensive tests
6. Update documentation

Backward Compatibility
~~~~~~~~~~~~~~~~~~~~~~

* Maintain backward compatibility when possible
* Use deprecation warnings for breaking changes
* Update version numbers appropriately
* Document migration paths

Performance
~~~~~~~~~~~

* Profile code for performance bottlenecks
* Use appropriate data structures
* Minimize I/O operations
* Cache expensive operations when possible

Security
~~~~~~~~

* Validate all input data
* Sanitize file paths
* Handle errors gracefully
* Follow security best practices

Release Process
---------------

Version Numbering
~~~~~~~~~~~~~~~~~

Follow semantic versioning (SemVer):

* **MAJOR**: Breaking changes
* **MINOR**: New features (backward compatible)
* **PATCH**: Bug fixes (backward compatible)

Release Checklist
~~~~~~~~~~~~~~~~~

1. Update version in ``pyproject.toml``
2. Update ``__version__`` in ``__init__.py``
3. Update changelog
4. Run full test suite
5. Build and test package
6. Create release on GitHub
7. Publish to PyPI

Getting Help
------------

If you need help:

1. Check the documentation
2. Search existing issues
3. Ask in discussions
4. Create a new issue

Community Guidelines
--------------------

Code of Conduct
~~~~~~~~~~~~~~~

* Be respectful and inclusive
* Focus on constructive feedback
* Help others learn and grow
* Follow the golden rule

Communication
~~~~~~~~~~~~~

* Use clear, descriptive language
* Provide context for questions
* Be patient with responses
* Help others when you can

Recognition
-----------

Contributors are recognized in:

* CONTRIBUTORS.md file
* Release notes
* Project documentation

Thank you for contributing to depcon! 🎉
