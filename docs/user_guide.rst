User Guide
===========

This guide covers all the features and options available in depcon. It's organized by functionality to help you find what you need.

Commands Overview
-----------------

depcon provides several commands:

* :ref:`convert-command` - Convert requirements files to pyproject.toml
* :ref:`show-command` - Display dependencies from pyproject.toml
* :ref:`validate-command` - Validate pyproject.toml dependencies
* :ref:`list-command` - List all dependency groups
* :ref:`check-command` - Check for common issues
* ``export`` - Export dependencies to requirements.txt
* ``diff`` - Show differences between files
* ``sync`` - Sync dependencies to requirements files

.. _convert-command:

Convert Command
---------------

The ``convert`` command is the main functionality of depcon. It converts legacy requirements files to modern pyproject.toml format.

Basic Usage
~~~~~~~~~~~

.. code-block:: bash

   depcon convert -r requirements.txt

Options
~~~~~~~

Requirements Files
^^^^^^^^^^^^^^^^^^

* ``-r, --requirements PATH``: Main requirements files (requirements.txt, requirements.in)
* ``-d, --dev-requirements PATH``: Development requirements files
* ``-t, --test-requirements PATH``: Test requirements files
* ``--docs-requirements PATH``: Documentation requirements files

Output Options
^^^^^^^^^^^^^^

* ``-o, --output PATH``: Output pyproject.toml file path (default: pyproject.toml)
* ``--append / --no-append``: Append to existing dependencies instead of replacing
* ``--backup / --no-backup``: Create backup of existing pyproject.toml

Processing Options
^^^^^^^^^^^^^^^^^^

* ``--resolve / --no-resolve``: Resolve and pin dependency versions
* ``--sort / --no-sort``: Sort dependencies alphabetically

Build Backend Options
^^^^^^^^^^^^^^^^^^^^^

* ``--build-backend [hatchling|setuptools|poetry]``: Build backend to use

Group Configuration
^^^^^^^^^^^^^^^^^^^

* ``--dev-group TEXT``: Name for development dependencies group (default: dev)
* ``--test-group TEXT``: Name for test dependencies group (default: test)
* ``--docs-group TEXT``: Name for documentation dependencies group (default: docs)

Project Metadata
^^^^^^^^^^^^^^^^

* ``--project-name TEXT``: Project name (if creating new pyproject.toml)
* ``--project-version TEXT``: Project version (if creating new pyproject.toml)
* ``--project-description TEXT``: Project description (if creating new pyproject.toml)
* ``--python-version TEXT``: Python version requirement (default: >=3.11)
* ``--use-optional-deps / --use-dependency-groups``: Use optional-dependencies (PEP 621 extras) instead of dependency-groups (PEP 735)
* ``--remove-duplicates / --keep-duplicates``: Remove duplicate dependencies across groups (default: remove)
* ``--strict / --no-strict``: Strict mode: fail on parsing errors instead of warning

General Options
^^^^^^^^^^^^^^^

* ``-v, --verbose``: Enable verbose output
* ``--help``: Show help message

Examples
~~~~~~~~

Basic conversion:

.. code-block:: bash

   depcon convert -r requirements.txt

Multiple files:

.. code-block:: bash

   depcon convert \
     -r requirements.txt \
     -d requirements-dev.txt \
     -t requirements-test.txt

With project metadata:

.. code-block:: bash

   depcon convert \
     -r requirements.txt \
     --project-name "my-project" \
     --project-description "A great project" \
     --project-version "1.0.0"

Different build backend:

.. code-block:: bash

   depcon convert -r requirements.txt --build-backend setuptools

Append mode:

.. code-block:: bash

   depcon convert -r new-requirements.txt --append

.. _show-command:

Show Command
------------

The ``show`` command displays dependencies from a pyproject.toml file in various formats.

Usage
~~~~~

.. code-block:: bash

   depcon show [OPTIONS]

Options
~~~~~~~

* ``-f, --file PATH``: Path to pyproject.toml file (default: pyproject.toml)
* ``--format [table|json|yaml]``: Output format (default: table)
* ``--group TEXT``: Show only specific dependency group (main, dev, test, docs, or optional group name)

Examples
~~~~~~~~

Show in table format:

.. code-block:: bash

   depcon show

Show in JSON format:

.. code-block:: bash

   depcon show --format json

Show in YAML format:

.. code-block:: bash

   depcon show --format yaml

Show from specific file:

.. code-block:: bash

   depcon show -f my-project.toml

.. _validate-command:

Validate Command
----------------

The ``validate`` command checks that dependencies in a pyproject.toml file are properly formatted.

Usage
~~~~~

.. code-block:: bash

   depcon validate [OPTIONS]

Options
~~~~~~~

* ``-f, --file PATH``: Path to pyproject.toml file (default: pyproject.toml)
* ``--group TEXT``: Dependency group to validate (main, dev, test, docs)
* ``--check-pypi / --no-check-pypi``: Check if packages exist on PyPI

Examples
~~~~~~~~

Validate all dependencies:

.. code-block:: bash

   depcon validate

Validate specific group:

.. code-block:: bash

   depcon validate --group dev

Validate specific file:

.. code-block:: bash

   depcon validate -f my-project.toml

.. _list-command:

List Command
------------

The ``list`` command lists all dependency groups in a pyproject.toml file.

Usage
~~~~~

.. code-block:: bash

   depcon list [OPTIONS]

Options
~~~~~~~

* ``-f, --file PATH``: Path to pyproject.toml file (default: pyproject.toml)

Examples
~~~~~~~~

List all groups:

.. code-block:: bash

   depcon list

List from specific file:

.. code-block:: bash

   depcon list -f my-project.toml

.. _check-command:

Check Command
-------------

The ``check`` command checks pyproject.toml for common issues.

Usage
~~~~~

.. code-block:: bash

   depcon check [OPTIONS]

Options
~~~~~~~

* ``-f, --file PATH``: Path to pyproject.toml file (default: pyproject.toml)
* ``--check-duplicates / --no-check-duplicates``: Check for duplicate dependencies (default: check)
* ``--check-missing / --no-check-missing``: Check for missing optional dependencies

Examples
~~~~~~~~

Check for issues:

.. code-block:: bash

   depcon check

Check for duplicates:

.. code-block:: bash

   depcon check --check-duplicates

Dependency Grouping
-------------------

depcon intelligently groups dependencies based on common patterns:

Main Dependencies
~~~~~~~~~~~~~~~~~

Core project dependencies that are required for the package to function:

* Web frameworks (Django, Flask, FastAPI)
* Data processing (pandas, numpy, scipy)
* HTTP clients (requests, httpx)
* Database drivers (psycopg2, pymongo)
* And many more...

Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

Tools used during development but not required at runtime:

* Code formatters (black, isort)
* Linters (ruff, flake8, pylint)
* Type checkers (mypy, pyright)
* Testing tools (pytest, pytest-cov)
* Pre-commit hooks
* Build tools

Test Dependencies
~~~~~~~~~~~~~~~~~

Testing frameworks and utilities:

* Testing frameworks (pytest, unittest, nose2)
* Test coverage tools (pytest-cov, coverage)
* Test utilities (pytest-mock, factory-boy)
* Performance testing (pytest-benchmark)

Documentation Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~

Tools for building and maintaining documentation:

* Documentation generators (sphinx, mkdocs)
* Themes and extensions
* Documentation utilities

Supported File Formats
----------------------

depcon supports various requirements file formats:

Standard Requirements Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``requirements.txt`` - Standard pip requirements files
* ``requirements.in`` - pip-tools input files
* ``requirements-dev.txt`` - Development dependencies
* ``requirements-test.txt`` - Test dependencies
* ``requirements-docs.txt`` - Documentation dependencies

Custom Files
~~~~~~~~~~~~

You can use any filename for requirements files:

.. code-block:: bash

   depcon convert -r my-deps.txt -d dev-tools.txt

File Format Support
~~~~~~~~~~~~~~~~~~~

depcon handles various requirement specifications:

* Version specifiers: ``>=2.25.0,<3.0.0``
* Extras: ``requests[security]``
* URLs: ``git+https://github.com/user/repo.git``
* Local paths: ``./local-package``
* Editable installs: ``-e ./local-package``
* Environment markers: ``requests; python_version >= "3.8"``

Build Backends
--------------

depcon supports multiple build backends:

Hatchling
~~~~~~~~~

The default and recommended backend:

.. code-block:: toml

   [build-system]
   requires = ["hatchling"]
   build-backend = "hatchling.build"

Setuptools
~~~~~~~~~~

Traditional Python packaging:

.. code-block:: toml

   [build-system]
   requires = ["setuptools>=61.0", "wheel"]
   build-backend = "setuptools.build_meta"

Poetry
~~~~~~

Poetry-style configuration:

.. code-block:: toml

   [build-system]
   requires = ["poetry-core"]
   build-backend = "poetry.core.masonry.api"

Tool Integration
----------------

depcon automatically configures integration with modern Python tools:

uv Integration
~~~~~~~~~~~~~~

Uses ``[dependency-groups]`` for uv configuration (recommended by uv):

.. code-block:: toml

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

Hatch Integration
~~~~~~~~~~~~~~~~~

Configures hatch build targets:

.. code-block:: toml

   [tool.hatch.build.targets.wheel]
   packages = ["src"]

Advanced Usage
--------------

Custom Group Names
~~~~~~~~~~~~~~~~~~

You can customize the names of dependency groups:

.. code-block:: bash

   depcon convert \
     -r requirements.txt \
     --dev-group "development" \
     --test-group "testing" \
     --docs-group "documentation"

Append Mode
~~~~~~~~~~~

Add dependencies to existing pyproject.toml:

.. code-block:: bash

   depcon convert -r new-requirements.txt --append

Version Resolution
~~~~~~~~~~~~~~~~~~

Resolve and pin dependency versions:

.. code-block:: bash

   depcon convert -r requirements.in --resolve

This will:
- Resolve all dependencies
- Pin exact versions
- Create a lock file (if supported)

Sorting Dependencies
~~~~~~~~~~~~~~~~~~~~

Sort dependencies alphabetically:

.. code-block:: bash

   depcon convert -r requirements.txt --sort

Backup Creation
~~~~~~~~~~~~~~~

Create backups of existing files:

.. code-block:: bash

   depcon convert -r requirements.txt --backup

This creates a ``.bak`` file with the original content.

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

Invalid Version Specifiers
^^^^^^^^^^^^^^^^^^^^^^^^^^

If you see errors about invalid version specifiers:

.. code-block:: bash

   # Check the problematic line
   depcon convert -r requirements.txt --verbose

   # Fix the version specifier in your requirements file
   # Then try again
   depcon convert -r requirements.txt

Missing Dependencies
^^^^^^^^^^^^^^^^^^^^

If dependencies can't be resolved:

.. code-block:: bash

   # Try without resolution
   depcon convert -r requirements.txt --no-resolve

   # Or resolve manually
   pip install -r requirements.txt
   depcon convert -r requirements.txt --resolve

File Not Found
^^^^^^^^^^^^^^

Make sure your requirements files exist:

.. code-block:: bash

   # List files
   ls -la requirements*.txt

   # Use absolute paths if needed
   depcon convert -r /full/path/to/requirements.txt

Getting Help
~~~~~~~~~~~~

For more help:

.. code-block:: bash

   # General help
   depcon --help

   # Command-specific help
   depcon convert --help
   depcon show --help
   depcon validate --help

   # Verbose output
   depcon convert -r requirements.txt --verbose
