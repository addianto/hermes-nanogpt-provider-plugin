# NanoGPT Model Provider Plugin for Hermes Agent

[![CI](https://github.com/addianto/nanogpt-model-provider-hermes-plugin/actions/workflows/ci.yml/badge.svg)](https://github.com/addianto/nanogpt-model-provider-hermes-plugin/actions/workflows/ci.yml)

This is a plugin that lets Hermes Agent use NanoGPT as a model provider.

## Why?

I know the plugin is very simple to implement directly in Hermes Agent since NanoGPT provides OpenAI-like API.
It could be as simple as creating an instance of `ProviderProfile` that points to the NanoGPT's API.

However, I avoid making changes directly in the upstream Hermes Agent codebase.
I don't want to add more code to maintain and review for the maintainers,
even though I know some of the maintainers are automated as AI agents.
_(citation needed, but that's the impression I get from skimming the issues and pull requests)_
I simply want to create and run a plugin as intended: to extend the original software without making direct changes to it.

## Setup (Manual)

1. Clone this repository to `$HERMES_HOME/plugins/model-providers`:
   ```shell
   mkdir -p $HERMES_HOME/plugins/model-providers
   git clone <repository URL> $HERMES_HOME/plugins/model-providers/nanogpt
   ```
2. Add the `providers` section in `config.yaml` with `nanogpt`-specific properties to resolve unknown model warning. 
   At minimum, add these to `config.yaml`:
   ```yaml
   providers:
     nanogpt:
       api_key: NANOGPT_API_KEY
       base_url: https://nano-gpt.com/api/v1
   ```
3. Configure Hermes Agent to use NanoGPT as model provider, either using `hermes model` from the shell or `/model` command from Hermes' TUI.

## Setup (Python Package)

_Note: untested_

According to the Hermes Agent documentation, it should be as simple as `pip install <plugin's package name on PyPI>`.
I haven't tested it nor set up the publishing account on PyPI.

## Acknowledgements

I followed the repository structure of [`mssteuer/lossless-hermes-py`](https://github.com/mssteuer/lossless-hermes-py).

## License

[MIT](./LICENSE).
