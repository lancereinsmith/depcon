Quick Start Guide
==================

This guide will help you get started with depcon quickly. We'll cover the most common use cases and show you how to convert your existing requirements files to modern pyproject.toml format.

Basic Conversion
----------------

The simplest way to use depcon is to convert a single requirements.txt file:

.. code-block:: bash

   depcon convert -r requirements.txt

This will:
- Parse your requirements.txt file
- Convert it to pyproject.toml format
- Use intelligent dependency grouping
- Create a backup of any existing pyproject.toml

Full Project Migration
----------------------

For a complete project migration, you can convert multiple requirement files:

.. code-block:: bash

   depcon convert \
     -r requirements.txt \
     -d requirements-dev.txt \
     -t requirements-test.txt \
     --docs-requirements requirements-docs.txt \
     --project-name "my-awesome-project" \
     --project-description "An awesome Python project"

This will:
- Convert main dependencies from requirements.txt
- Group development tools into the dev group
- Group testing tools into the test group
- Group documentation tools into the docs group
- Set project metadata

Viewing Dependencies
--------------------

After conversion, you can view your dependencies in various formats:

.. code-block:: bash

   # Show in table format (default)
   depcon show

   # Show in JSON format
   depcon show --format json

   # Show in YAML format
   depcon show --format yaml

Validating Dependencies
-----------------------

Validate that your dependencies are properly formatted:

.. code-block:: bash

   # Validate all dependencies
   depcon validate

   # Validate specific group
   depcon validate --group dev

Example Workflow
----------------

Here's a complete example of migrating a project:

.. code-block:: bash

   # 1. Check current state
   ls -la *.txt

   # 2. Convert requirements
   depcon convert \
     -r requirements.txt \
     -d requirements-dev.txt \
     -t requirements-test.txt \
     --project-name "my-project" \
     --project-description "My awesome project" \
     --verbose

   # 3. Review the generated pyproject.toml
   cat pyproject.toml

   # 4. Validate dependencies
   depcon validate

   # 5. Test installation
   uv sync

   # 6. Build the package
   uv build

Next Steps
----------

Now that you've converted your requirements, you can:

1. **Review the generated pyproject.toml** - Check that all dependencies are correctly grouped
2. **Test installation** - Use ``uv sync`` or ``pip install -e .`` to test
3. **Build your package** - Use ``uv build`` or ``hatch build``
4. **Clean up old files** - Remove old requirements.txt files once you're satisfied
5. **Update your CI/CD** - Update your build scripts to use the new format

For more advanced usage, see the :doc:`user_guide` and :doc:`examples`.
