#!/usr/bin/env python3
"""Demo script showing depcon's capabilities."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and display the result."""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}")
    print()

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False
    return True


def main():
    """Run the demo."""
    print("🚀 depcon Demo - Modern Python Dependency Management")
    print("=" * 60)

    # Check if depcon is installed
    try:
        subprocess.run(["depcon", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ depcon is not installed. Please install it first:")
        print("   uv tool install depcon")
        print("   or")
        print("   pipx install depcon")
        sys.exit(1)

    # Demo 1: Basic conversion
    run_command(
        [
            "depcon",
            "convert",
            "-r",
            "examples/requirements.txt",
            "--output",
            "demo-pyproject.toml",
            "--verbose",
        ],
        "Basic Conversion - Single requirements.txt file",
    )

    # Demo 2: Full project conversion
    run_command(
        [
            "depcon",
            "convert",
            "-r",
            "examples/requirements.txt",
            "-d",
            "examples/requirements-dev.txt",
            "-t",
            "examples/requirements-test.txt",
            "--docs-requirements",
            "examples/requirements-docs.txt",
            "--project-name",
            "demo-project",
            "--project-description",
            "A demonstration project",
            "--output",
            "demo-full-pyproject.toml",
            "--verbose",
        ],
        "Full Project Conversion - Multiple requirement files with metadata",
    )

    # Demo 3: Show dependencies
    run_command(
        ["depcon", "show"],
        "Show Dependencies - Display current pyproject.toml dependencies",
    )

    # Demo 4: Show in JSON format
    run_command(
        ["depcon", "show", "--format", "json"],
        "Show Dependencies (JSON) - Machine-readable output",
    )

    # Demo 5: Validate dependencies
    run_command(["depcon", "validate"], "Validate Dependencies - Check for issues")

    # Demo 6: Different build backends
    run_command(
        [
            "depcon",
            "convert",
            "-r",
            "examples/requirements.txt",
            "--build-backend",
            "setuptools",
            "--output",
            "pyproject-setuptools.toml",
        ],
        "Different Build Backend - Using setuptools instead of hatchling",
    )

    # Demo 7: Append mode
    run_command(
        [
            "depcon",
            "convert",
            "-r",
            "examples/requirements-dev.txt",
            "--append",
            "--output",
            "demo-append-pyproject.toml",
            "--verbose",
        ],
        "Append Mode - Add to existing dependencies",
    )

    print(f"\n{'='*60}")
    print("🎉 Demo completed!")
    print("=" * 60)
    print("\nGenerated files:")
    for file in [
        "demo-pyproject.toml",
        "demo-full-pyproject.toml",
        "pyproject-setuptools.toml",
        "demo-append-pyproject.toml",
    ]:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")

    print("\nNext steps:")
    print("1. Review the generated pyproject.toml files")
    print("2. Test installation: uv sync")
    print("3. Build your package: uv build")
    print("4. Clean up old requirements files")


if __name__ == "__main__":
    main()
