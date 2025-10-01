Installation
============

depcon can be installed using several methods. We recommend using ``uv`` for the best experience.

Using uv (Recommended)
----------------------

``uv`` is a fast Python package installer and resolver. It's the recommended way to install depcon:

.. code-block:: bash

   # Install depcon globally
   uv tool install depcon

   # Or run directly without installing
   uvx depcon

   # Install in a specific project
   uv add depcon

Using pipx
----------

``pipx`` is another great option for installing Python applications in isolated environments:

.. code-block:: bash

   # Install depcon
   pipx install depcon

   # Update depcon
   pipx upgrade depcon

   # Run without installing
   pipx run depcon

Using pip
---------

You can also install depcon using pip:

.. code-block:: bash

   # Install from PyPI
   pip install depcon

   # Install with development dependencies
   pip install depcon[dev]

   # Install with all optional dependencies
   pip install depcon[all]

From Source
-----------

To install from source for development:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/lancereinsmith/depcon.git
   cd depcon

   # Install in development mode
   uv pip install -e ".[dev]"

   # Or with pip
   pip install -e ".[dev]"

Verification
------------

After installation, verify that depcon is working correctly:

.. code-block:: bash

   # Check version
   depcon --version

   # Check help
   depcon --help

   # Run a quick test
   depcon convert --help

Requirements
------------

* Python 3.8 or higher
* Modern Python packaging tools (uv, pip, or pipx)

Optional Dependencies
---------------------

depcon has several optional dependency groups:

* ``dev``: Development tools (pytest, black, ruff, mypy, pre-commit)
* ``test``: Testing tools (pytest, pytest-cov, pytest-mock)
* ``docs``: Documentation tools (sphinx, sphinx-rtd-theme, myst-parser)
* ``all``: All optional dependencies

Install with optional dependencies:

.. code-block:: bash

   # Install with specific groups
   uv tool install depcon[dev,docs]

   # Install with all optional dependencies
   uv tool install depcon[all]
