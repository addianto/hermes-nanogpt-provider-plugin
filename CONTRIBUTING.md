# How to Contribute

## Local Development Setup

You will need:

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) for project and package management

To begin development, fork the repository.
Then, clone the fork into your local development machine and install dependencies:

```shell
git clone <your fork> hermes-nanogpt-provider-plugin
cd hermes-nanogpt-provider-plugin
uv sync --all-groups
```

## Working on the Codebase

Make sure to run linters and ensure tests pass for every changes:

```shell
uv run ruff check
uv run ruff format --check
uv run pytest --cov=src --cov-report=term-missing
```
