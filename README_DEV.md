# filename-manager Development Guide

This document covers local development, testing, building, and release verification for `filename-manager`.

For user-facing installation and CLI usage, see [`README.md`](README.md).

## Development Setup

Clone the repository:

```shell
git clone https://github.com/alexcwarren/filename-manager.git
cd filename-manager
```

Install Hatch if needed:

```shell
pip install hatch
```

Create the Hatch development environment:

```shell
hatch env create
```

## Common Development Commands

Format the codebase:

```shell
hatch run format
```

Lint the codebase and automatically apply supported fixes:

```shell
hatch run lint
```

Run static type checking:

```shell
hatch run typecheck
```

Run the standard test suite:

```shell
hatch run test
```

Run all validation checks without modifying the codebase:

```shell
hatch run check
```

Use `check` before opening or merging a pull request.

## Testing

Run the standard pytest suite:

```shell
pytest
```

Run tests marked as `full`:

```shell
pytest -m "full"
```

Run tests with terminal coverage output:

```shell
pytest --cov=src/filename_manager --cov-report=term-missing
```

Generate an HTML coverage report:

```shell
pytest --cov=src/filename_manager --cov-report=html
```

The generated report is available under:

```text
htmlcov/
```

## Building

Remove previous build artifacts and caches:

```shell
hatch run clean
```

Build the wheel and source distribution:

```shell
hatch run build
```

Build artifacts are written to:

```text
dist/
```

A successful build should produce both:

- a `.whl` wheel
- a `.tar.gz` source distribution

## Release Checks

Before creating a release, run:

```shell
hatch run release-check
```

This performs the automated checks required before building a release artifact.

Afterward, verify the built package from a clean virtual environment.

### Create a clean environment

On Windows PowerShell:

```powershell
python -m venv .release-test
.\.release-test\Scripts\Activate.ps1
```

### Install the built wheel

For example:

```powershell
pip install dist\filename_manager-0.1.0-py3-none-any.whl
```

Adjust the filename for the version being tested.

### Verify the installed CLI

```shell
filename-manager --help
```

Perform a brief smoke test using disposable files and confirm:

- prefix renaming works
- suffix renaming works
- extension replacement works
- an existing destination file is never overwritten
- unsupported regex/substitution options exit without modifying files

When finished:

```shell
deactivate
```

The `.release-test` environment may then be deleted.

## Release Checklist

Before publishing a release:

- [ ] `hatch run release-check` passes
- [ ] the built wheel installs successfully in a clean environment
- [ ] `filename-manager --help` works from the installed package
- [ ] supported rename operations pass a manual smoke test
- [ ] collision protection prevents overwriting existing files
- [ ] GitHub Actions passes on `main`
- [ ] package version is correct in `pyproject.toml`
- [ ] README documentation matches the released functionality
- [ ] release notes are prepared
