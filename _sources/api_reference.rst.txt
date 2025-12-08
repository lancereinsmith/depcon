API Reference
==============

This section provides detailed documentation for the depcon API. The API is organized into several modules:

* :ref:`models` - Data models and configuration
* :ref:`parsers` - Dependency parsing functionality
* :ref:`generators` - PyProject.toml generation
* :ref:`cli` - Command-line interface

.. _models:

Models Module
-------------

The models module contains the core data structures used by depcon.

.. automodule:: depcon.models
   :members:
   :undoc-members:
   :show-inheritance:

DependencySpec
~~~~~~~~~~~~~~

.. autoclass:: depcon.models.DependencySpec
   :members:
   :undoc-members:
   :show-inheritance:

DependencyGroup
~~~~~~~~~~~~~~~

.. autoclass:: depcon.models.DependencyGroup
   :members:
   :undoc-members:
   :show-inheritance:

ProjectConfig
~~~~~~~~~~~~~

.. autoclass:: depcon.models.ProjectConfig
   :members:
   :undoc-members:
   :show-inheritance:

ConversionOptions
~~~~~~~~~~~~~~~~~

.. autoclass:: depcon.models.ConversionOptions
   :members:
   :undoc-members:
   :show-inheritance:

.. _parsers:

Parsers Module
--------------

The parsers module handles parsing of various requirements file formats.

.. automodule:: depcon.parsers
   :members:
   :undoc-members:
   :show-inheritance:

RequirementsParser
~~~~~~~~~~~~~~~~~~

.. autoclass:: depcon.parsers.RequirementsParser
   :members:
   :undoc-members:
   :show-inheritance:

parse_requirements_file
~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: depcon.parsers.parse_requirements_file

group_dependencies_by_type
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: depcon.parsers.group_dependencies_by_type

.. _generators:

Generators Module
-----------------

The generators module handles creation and manipulation of pyproject.toml files.

.. automodule:: depcon.generators
   :members:
   :undoc-members:
   :show-inheritance:

PyProjectGenerator
~~~~~~~~~~~~~~~~~~

.. autoclass:: depcon.generators.PyProjectGenerator
   :members:
   :undoc-members:
   :show-inheritance:

PyProjectUpdater
~~~~~~~~~~~~~~~~

.. autoclass:: depcon.generators.PyProjectUpdater
   :members:
   :undoc-members:
   :show-inheritance:

.. _cli:

CLI Module
----------

The CLI module provides the command-line interface for depcon.

.. automodule:: depcon.cli
   :members:
   :undoc-members:
   :show-inheritance:

main
~~~~

.. autofunction:: depcon.cli.main

convert
~~~~~~~

.. autofunction:: depcon.cli.convert

show
~~~~

.. autofunction:: depcon.cli.show

validate
~~~~~~~~

.. autofunction:: depcon.cli.validate

Utility Functions
-----------------

.. autofunction:: depcon.cli._print_dependency_summary

.. autofunction:: depcon.cli._print_dependencies_table

.. autofunction:: depcon.cli._validate_dependency

Exceptions
----------

depcon uses standard Python exceptions for error handling. No custom exceptions are defined.

Constants
---------

No module-level constants are defined in depcon.
