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
uv sync --inexact
uv pip install -r requirements-dev.txt
```

## Working on the Codebase

Make sure to run linters and ensure tests pass for every change:

```shell
uv run ruff check
uv run ruff format --check
uv run pytest --cov=src --cov-report=term-missing
```

## Releasing a New Version

> Note: For maintainers.

You can prepare a new release either when:

- Working on a branch that implements changes to the project that warrant a version update or increment according to the [Semantic Versioning](https://semver.org) guidelines.
- Preparing the release independently on a separate release branch.

Regardless, update the version at [`pyproject.toml`](./pyproject.toml) and [`plugin.yaml`](./plugin.yaml).
Then, run `uv sync` to sync the new version to the auto-generated lockfile.

```shell
uv sync --inexact
```

To be extra sure, run the test suite that verifies version consistency:

```shell
uv run pytest tests/test_version_consistency.py
```

Lastly, save and commit the version update:

```shell
git add pyproject.toml plugin.yaml uv.lock
git commit -m "chore: Bump up project version"
```

Push the latest branch with latest commit to GitHub and merge it to the main branch by making a pull request.
Once the branch has been merged, update the local main branch and tag the release:

```shell
git switch main
git pull
git tag -s v1.2.3 -m "Release v1.2.3"
git push origin v1.2.3
```

> Note: The version number in the example above is just an example.
>       Please adjust to the actual version you want to tag and publish.

A GitHub workflow will draft a release note and publish the plugin to Test PyPI for review/staging.
The draft, by default, contains list of changes since the previous tag up to the new tag.
You can customise it via the project's GitHub release page.

Once the release notes is ready, trigger a release workflow on GitHUb by providing the tag name you want to publish.
GitHub will automatically build and publish the plugin to PyPI.
