# depcon Documentation

This directory contains the comprehensive documentation for depcon, built with Sphinx.

## Building the Documentation

### Prerequisites

Install the documentation dependencies:

```bash
# Using uv (recommended)
uv pip install -e ".[docs]"

# Or using pip
pip install -e ".[docs]"
```

### Build Commands

```bash
# Build HTML documentation
make html

# Build PDF documentation
make latexpdf

# Build EPUB documentation
make epub

# Check for broken links
make linkcheck

# Clean build directory
make clean

# Show all available commands
make help
```

### Development Server

For development, you can use Sphinx's auto-reload feature:

```bash
# Install sphinx-autobuild
pip install sphinx-autobuild

# Start development server
sphinx-autobuild docs docs/_build/html --open-browser
```

## Documentation Structure

```
docs/
├── conf.py              # Sphinx configuration
├── index.rst            # Main documentation page
├── installation.rst     # Installation guide
├── quickstart.rst       # Quick start guide
├── user_guide.rst       # Comprehensive user guide
├── api_reference.rst    # API documentation
├── examples.rst         # Usage examples
├── contributing.rst     # Contributing guidelines
├── changelog.rst        # Project changelog
├── _static/             # Static assets (CSS, images)
├── _templates/          # Custom templates
└── requirements.txt     # Documentation dependencies
```

## Writing Documentation

### Style Guide

- Use reStructuredText (RST) format
- Follow the existing documentation structure
- Include code examples for all features
- Use proper cross-references between sections
- Include screenshots for UI elements when helpful

### Adding New Sections

1. Create a new `.rst` file in the docs directory
2. Add it to the `toctree` in `index.rst`
3. Follow the existing format and style
4. Update the table of contents as needed

### Code Examples

Use proper syntax highlighting:

```rst
.. code-block:: bash

   depcon convert -r requirements.txt

.. code-block:: python

   from depcon.models import DependencySpec
   dep = DependencySpec(name="requests", version_specs=[">=2.25.0"])
```

### Cross-References

Link between sections:

```rst
See :doc:`installation` for setup instructions.

See :ref:`convert-command` for usage details.

See :func:`depcon.models.DependencySpec` for API reference.
```

## Deployment

The documentation is automatically deployed to GitHub Pages when changes are pushed to the main branch. The deployment is handled by the GitHub Actions workflow in `.github/workflows/docs.yml`.

### Manual Deployment

If you need to deploy manually:

```bash
# Build the documentation
make html

# Deploy to GitHub Pages (requires gh-pages branch)
ghp-import docs/_build/html -p
```

## Contributing to Documentation

1. Make your changes to the `.rst` files
2. Test locally with `make html`
3. Check for broken links with `make linkcheck`
4. Submit a pull request

## Troubleshooting

### Common Issues

**Build Errors:**
- Check that all dependencies are installed
- Verify RST syntax is correct
- Check for missing cross-references

**Missing Modules:**
- Ensure the source code is installed in development mode
- Check that `sys.path` includes the source directory

**Broken Links:**
- Use `make linkcheck` to find broken links
- Update cross-references as needed

### Getting Help

- Check the Sphinx documentation: https://www.sphinx-doc.org/
- Review existing documentation for examples
- Ask questions in the project's issue tracker
