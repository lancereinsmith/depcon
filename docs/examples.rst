Examples
=========

This section provides comprehensive examples of using depcon in various scenarios.

Basic Examples
--------------

Simple Requirements Conversion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Convert a basic requirements.txt file:

.. code-block:: bash

   # requirements.txt
   requests>=2.25.0
   numpy>=1.20.0
   pandas>=1.3.0

   # Convert
   depcon convert -r requirements.txt

   # Result: pyproject.toml
   [build-system]
   requires = ["hatchling"]
   build-backend = "hatchling.build"

   [project]
   name = "my-project"
   version = "0.1.0"
   description = ""
   requires-python = ">=3.8"
   dependencies = [
       "numpy>=1.20.0",
       "pandas>=1.3.0",
       "requests>=2.25.0",
   ]

Multiple Requirements Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Convert multiple requirement files with proper grouping:

.. code-block:: bash

   # requirements.txt
   requests>=2.25.0
   numpy>=1.20.0

   # requirements-dev.txt
   pytest>=7.0.0
   black>=23.0.0
   ruff>=0.1.0

   # requirements-test.txt
   pytest-cov>=4.0.0
   pytest-mock>=3.10.0

   # Convert
   depcon convert \
     -r requirements.txt \
     -d requirements-dev.txt \
     -t requirements-test.txt

   # Result: pyproject.toml
   [build-system]
   requires = ["hatchling"]
   build-backend = "hatchling.build"

   [project]
   name = "my-project"
   version = "0.1.0"
   description = ""
   requires-python = ">=3.8"
   dependencies = [
       "numpy>=1.20.0",
       "requests>=2.25.0",
   ]

   [project.optional-dependencies]
   dev = [
       "black>=23.0.0",
       "pytest>=7.0.0",
       "ruff>=0.1.0",
   ]
   test = [
       "pytest-cov>=4.0.0",
       "pytest-mock>=3.10.0",
   ]

Advanced Examples
-----------------

Complete Project Migration
~~~~~~~~~~~~~~~~~~~~~~~~~~

Migrate a complete project with all metadata:

.. code-block:: bash

   depcon convert \
     -r requirements.txt \
     -d requirements-dev.txt \
     -t requirements-test.txt \
     --docs-requirements requirements-docs.txt \
     --project-name "awesome-project" \
     --project-description "An awesome Python project" \
     --project-version "1.0.0" \
     --python-version ">=3.9" \
     --build-backend hatchling

Custom Group Names
~~~~~~~~~~~~~~~~~~

Use custom names for dependency groups:

.. code-block:: bash

   depcon convert \
     -r requirements.txt \
     -d requirements-dev.txt \
     --dev-group "development" \
     --test-group "testing"

Different Build Backends
~~~~~~~~~~~~~~~~~~~~~~~~

Use setuptools instead of hatchling:

.. code-block:: bash

   depcon convert \
     -r requirements.txt \
     --build-backend setuptools

Append Mode
~~~~~~~~~~~

Add new dependencies to existing pyproject.toml:

.. code-block:: bash

   # Add new requirements
   depcon convert \
     -r new-requirements.txt \
     --append

Version Resolution
~~~~~~~~~~~~~~~~~~

Resolve and pin all dependency versions:

.. code-block:: bash

   depcon convert \
     -r requirements.in \
     --resolve

Real-World Examples
-------------------

Django Project
~~~~~~~~~~~~~~

Convert a Django project with development and testing dependencies:

.. code-block:: bash

   # requirements.txt
   Django>=4.2.0
   psycopg2-binary>=2.9.0
   redis>=4.5.0
   celery>=5.3.0

   # requirements-dev.txt
   pytest>=7.0.0
   pytest-django>=4.5.0
   black>=23.0.0
   ruff>=0.1.0
   mypy>=1.0.0

   # Convert
   depcon convert \
     -r requirements.txt \
     -d requirements-dev.txt \
     --project-name "my-django-app" \
     --project-description "A Django web application"

Data Science Project
~~~~~~~~~~~~~~~~~~~~

Convert a data science project with multiple dependency types:

.. code-block:: bash

   # requirements.txt
   pandas>=2.0.0
   numpy>=1.24.0
   scikit-learn>=1.3.0
   matplotlib>=3.7.0
   jupyter>=1.0.0

   # requirements-dev.txt
   pytest>=7.0.0
   black>=23.0.0
   ruff>=0.1.0
   pre-commit>=3.0.0

   # requirements-docs.txt
   sphinx>=5.0.0
   sphinx-rtd-theme>=1.0.0
   myst-parser>=1.0.0

   # Convert
   depcon convert \
     -r requirements.txt \
     -d requirements-dev.txt \
     --docs-requirements requirements-docs.txt \
     --project-name "data-analysis-tool" \
     --project-description "A tool for data analysis and visualization"

FastAPI Project
~~~~~~~~~~~~~~~

Convert a FastAPI project with async dependencies:

.. code-block:: bash

   # requirements.txt
   fastapi>=0.100.0
   uvicorn>=0.23.0
   pydantic>=2.0.0
   sqlalchemy>=2.0.0
   alembic>=2.0.0

   # requirements-dev.txt
   pytest>=7.0.0
   pytest-asyncio>=0.21.0
   httpx>=0.24.0
   black>=23.0.0
   ruff>=0.1.0

   # Convert
   depcon convert \
     -r requirements.txt \
     -d requirements-dev.txt \
     --project-name "my-fastapi-app" \
     --project-description "A FastAPI web service"

CLI Examples
------------

Viewing Dependencies
~~~~~~~~~~~~~~~~~~~~

Display dependencies in different formats:

.. code-block:: bash

   # Table format (default)
   depcon show

   # JSON format
   depcon show --format json

   # YAML format
   depcon show --format yaml

   # Specific file
   depcon show -f my-project.toml

Validating Dependencies
~~~~~~~~~~~~~~~~~~~~~~~

Validate dependency specifications:

.. code-block:: bash

   # Validate all dependencies
   depcon validate

   # Validate specific group
   depcon validate --group dev

   # Validate specific file
   depcon validate -f my-project.toml

Integration Examples
---------------------

uv Integration
~~~~~~~~~~~~~~

Work with uv for dependency management:

.. code-block:: bash

   # Initialize project
   uv init

   # Convert requirements
   depcon convert -r requirements.txt

   # Sync dependencies
   uv sync

   # Add new dependency
   uv add requests

   # Update pyproject.toml
   depcon convert -r requirements.txt --append

Hatch Integration
~~~~~~~~~~~~~~~~~

Use with hatch for building and publishing:

.. code-block:: bash

   # Convert with hatchling backend
   depcon convert -r requirements.txt --build-backend hatchling

   # Build package
   hatch build

   # Publish package
   hatch publish

Poetry Integration
~~~~~~~~~~~~~~~~~~

Convert to poetry-style configuration:

.. code-block:: bash

   # Convert with poetry backend
   depcon convert -r requirements.txt --build-backend poetry

   # Install dependencies
   poetry install

   # Build package
   poetry build

CI/CD Integration
-----------------

GitHub Actions
~~~~~~~~~~~~~~

Example GitHub Actions workflow:

.. code-block:: yaml

   name: CI
   on: [push, pull_request]
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
           with:
             python-version: '3.11'
         - name: Install uv
           run: pip install uv
         - name: Convert requirements
           run: uvx depcon convert -r requirements.txt
         - name: Install dependencies
           run: uv sync
         - name: Run tests
           run: uv run pytest

Docker Integration
~~~~~~~~~~~~~~~~~~

Example Dockerfile:

.. code-block:: dockerfile

   FROM python:3.11-slim

   # Install uv
   RUN pip install uv

   # Copy requirements and convert
   COPY requirements.txt .
   RUN uvx depcon convert -r requirements.txt

   # Install dependencies
   RUN uv sync

   # Copy source code
   COPY src/ /app/src/
   COPY pyproject.toml /app/

   # Set working directory
   WORKDIR /app

   # Run application
   CMD ["uv", "run", "python", "-m", "src.main"]

Troubleshooting Examples
------------------------

Common Issues and Solutions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Invalid Version Specifiers
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Problem: Invalid version specifier
   # requirements.txt contains: requests>=2.25.0,<3.0.0

   # Solution: Check with verbose output
   depcon convert -r requirements.txt --verbose

   # Fix the version specifier in requirements.txt
   # Then convert again
   depcon convert -r requirements.txt

Missing Dependencies
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Problem: Dependencies can't be resolved
   # Solution: Try without resolution first
   depcon convert -r requirements.txt --no-resolve

   # Or resolve manually
   pip install -r requirements.txt
   depcon convert -r requirements.txt --resolve

File Not Found
^^^^^^^^^^^^^^

.. code-block:: bash

   # Problem: Requirements file not found
   # Solution: Check file exists and use correct path
   ls -la requirements*.txt
   depcon convert -r ./requirements.txt

Complex Requirements
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Problem: Complex requirements with URLs and markers
   # requirements.txt contains:
   # git+https://github.com/user/repo.git
   # requests; python_version >= "3.8"

   # Solution: depcon handles these automatically
   depcon convert -r requirements.txt --verbose

Best Practices
--------------

Project Structure
~~~~~~~~~~~~~~~~~

Organize your requirements files:

.. code-block:: text

   my-project/
   ├── requirements.txt          # Main dependencies
   ├── requirements-dev.txt      # Development tools
   ├── requirements-test.txt     # Testing tools
   ├── requirements-docs.txt     # Documentation tools
   ├── pyproject.toml           # Generated by depcon
   └── src/
       └── my_project/

Version Management
~~~~~~~~~~~~~~~~~~

Use appropriate version specifiers:

.. code-block:: text

   # Good: Specific versions for production
   requests>=2.25.0,<3.0.0

   # Good: Minimum versions for development
   pytest>=7.0.0

   # Avoid: Exact versions unless necessary
   requests==2.28.0

Dependency Grouping
~~~~~~~~~~~~~~~~~~~

Group dependencies logically:

.. code-block:: text

   # requirements.txt - Core functionality
   requests
   numpy
   pandas

   # requirements-dev.txt - Development tools
   pytest
   black
   ruff
   mypy

   # requirements-test.txt - Testing tools
   pytest-cov
   pytest-mock
   factory-boy

   # requirements-docs.txt - Documentation
   sphinx
   sphinx-rtd-theme
   myst-parser
