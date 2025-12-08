Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[Unreleased]
------------

[0.4.0] - 2024-12-XX
---------------------

Added
~~~~~

* New ``list`` command to list all dependency groups in pyproject.toml
* New ``check`` command to check for common issues (duplicates, missing dependencies)
* Enhanced ``convert`` command with ``--use-optional-deps`` flag to choose between dependency-groups (PEP 735) and optional-dependencies (PEP 621 extras)
* Enhanced ``convert`` command with ``--remove-duplicates`` flag to automatically remove duplicate dependencies
* Enhanced ``convert`` command with ``--strict`` flag for strict error handling
* Enhanced ``show`` command with ``--group`` option to filter by specific dependency group
* Enhanced ``validate`` command with ``--check-pypi`` flag to verify packages exist on PyPI
* Improved duplicate dependency detection and removal
* Better error messages and validation output
* Default Python version requirement updated to >=3.11

Changed
~~~~~~~

* Default Python version requirement changed from >=3.8 to >=3.11 to align with modern standards
* Improved handling of dependency-groups vs optional-dependencies
* Enhanced CLI help text and error messages
* Better integration with uv and modern Python packaging tools

Fixed
~~~~~

* Fixed duplicate dependency handling across groups
* Improved error handling in various commands
* Better validation of dependency specifications

[0.3.0] - 2024-12-XX
---------------------

Added
~~~~~

* Full PEP 735 support for dependency-groups
* New ``export`` command to export dependencies to requirements.txt format
* New ``diff`` command to compare dependencies between pyproject.toml and requirements files
* New ``sync`` command to sync dependencies from pyproject.toml to requirements files
* Enhanced ``show`` command to display both dependency-groups and optional-dependencies
* Support for distinguishing between dependency-groups (PEP 735) and optional-dependencies (PEP 621 extras)
* Improved validation for both dependency types
* Comprehensive tests for new CLI features

Changed
~~~~~~~

* Properly distinguish between dependency-groups (PEP 735) and optional-dependencies (PEP 621)
* Development dependencies now use dependency-groups by default for better uv compatibility
* Updated documentation to reflect latest PEP standards
* Improved error messages and validation output
* Enhanced CLI help text and examples

Fixed
~~~~~

* Fixed handling of dependency-groups vs optional-dependencies in pyproject.toml
* Improved parsing of both dependency types from existing pyproject.toml files

[0.2.1] - 2024-01-XX
---------------------

Added
~~~~~

* Initial release of depcon
* Full PEP 621 support
* Intelligent dependency grouping
* Rich CLI interface
* Multiple build backend support
* Tool integration (uv, hatch, poetry)
* Advanced validation
* Comprehensive test suite

[0.2.0] - 2024-01-XX
---------------------

Added
~~~~~

* Complete rewrite with modern architecture
* Full PEP 621 support
* Intelligent dependency grouping
* Rich CLI interface
* Advanced validation
* Multiple build backend support
* Tool integration (uv, hatch, poetry)

Changed
~~~~~~~

* Modernized codebase
* Improved error handling
* Enhanced user experience

[0.1.x] - 2024-01-XX
--------------------

Added
~~~~~

* Basic requirements.txt to pyproject.toml conversion
* Limited feature set

Changed
~~~~~~~

* Initial implementation
