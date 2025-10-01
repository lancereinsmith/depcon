depcon Documentation
====================

.. image:: https://img.shields.io/pypi/v/depcon.svg
   :target: https://pypi.org/project/depcon/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/depcon.svg
   :target: https://pypi.org/project/depcon/
   :alt: Python versions

.. image:: https://img.shields.io/github/license/lancereinsmith/depcon.svg
   :target: https://github.com/lancereinsmith/depcon/blob/master/LICENSE
   :alt: License

.. image:: https://img.shields.io/github/actions/workflow/status/lancereinsmith/depcon/ci.yml
   :target: https://github.com/lancereinsmith/depcon/actions
   :alt: CI Status

``depcon`` is a modern, fully-featured tool for converting legacy ``requirements.txt`` files to the standardized ``pyproject.toml`` format with full PEP 621 support. It provides intelligent dependency grouping, validation, and seamless integration with modern Python packaging tools like ``uv``, ``hatchling``, and ``setuptools``.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   user_guide
   api_reference
   examples
   contributing
   changelog

Features
--------

* **🔄 Full PEP 621 Support**: Complete support for the modern Python packaging standard
* **📦 Intelligent Dependency Grouping**: Automatically categorizes dependencies into main, dev, test, and docs groups
* **🔍 Advanced Parsing**: Handles complex requirements files including pip-tools, editable installs, and URLs
* **✅ Validation**: Built-in dependency validation and error checking
* **🎯 Multiple Build Backends**: Support for hatchling, setuptools, and poetry
* **🛠️ Tool Integration**: Automatic configuration for uv, hatch, and other modern tools
* **📊 Rich CLI**: Beautiful command-line interface with progress indicators and summaries
* **🔧 Flexible Configuration**: Extensive options for customization and control

Quick Start
-----------

Install depcon:

.. code-block:: bash

   # Using uv (recommended)
   uv tool install depcon

   # Or using pipx
   pipx install depcon

   # Or using pip
   pip install depcon

Convert your requirements:

.. code-block:: bash

   # Basic conversion
   depcon convert -r requirements.txt

   # Full project migration
   depcon convert \
     -r requirements.txt \
     -d requirements-dev.txt \
     -t requirements-test.txt \
     --docs-requirements requirements-docs.txt \
     --project-name "my-awesome-project"

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
