# NanoGPT Model Provider Plugin for Hermes Agent

[![CI](https://github.com/addianto/hermes-nanogpt-provider-plugin/actions/workflows/ci.yml/badge.svg)](https://github.com/addianto/hermes-nanogpt-provider-plugin/actions/workflows/ci.yml)

This is a plugin that lets Hermes Agent to use NanoGPT as a model provider.

## Why?

I know the plugin is very simple to implement directly in Hermes Agent since NanoGPT provides OpenAI-like API.
It could be as simple as creating an instance of `ProviderProfile` that points to the NanoGPT's API.

However, I avoid making changes directly in the upstream Hermes Agent codebase.
I don't want to add more code for the maintainers to maintain and review,
although I know most of the development is automated using AI agents.
_(citation needed, but that's the impression I get from skimming the issues and pull requests)._
I simply want to create and run a plugin as intended: to extend the original software without making direct changes to it.

## Installation (Recommended)

Use `hermes plugins install` command to install this plugin:

```shell
hermes plugins install addianto/hermes-nanogpt-provider-plugin
```

Verify the plugin is installed and recognised by Hermes Agent
If you see `nanogpt-provider` listed, enable the plugin:

```shell
hermes plugins list
hermes plugins enable nanogpt-provider
```

## Installation (via PyPI)

Locate where your Hermes Agent's Python virtual environment:

```shell
hermes pm env
```

Go to the parent directory of the virtual environment,
activate it and install the plugin:

```shell
source .venv/bin/activate
pip install hermes-nanogpt-provider
```

Verify the plugin is installed and recognised by Hermes Agent
If you see `nanogpt-provider` listed, enable the plugin:

```shell
hermes plugins list
hermes plugins enable nanogpt-provider
```

## Configuration

Add the following environment variables to your Hermes Agent's `.env` located at `$HERMES_HOME/.env`:

> Note: `$HERMES_HOME` can be a path to your default Hermes Agent installation or a path to a Hermes Agent profile.

- `NANOGPT_API_KEY` (mandatory): NanoGPT API key. Get it from https://nano-gpt.com/api.
- `NANOGPT_MODEL_LIST_ENDPOINT` (optional): NanoGPT model list endpoint. Four possible values:
  `canonical`, `personalized`, `subscription`, `paid`. Defaults to `canonical` if not set.

## How to Develop & Contribute

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Acknowledgements

I followed the repository structure of [`mssteuer/lossless-hermes-py`](https://github.com/mssteuer/lossless-hermes-py).

## License

[MIT](./LICENSE).
