# NanoGPT Model Provider Hermes Plugin

This is a model provider plugin for Hermes Agent.

## Why?

I know the plugin is very simple to implement directly in Hermes Agent since NanoGPT provides OpenAI-like API.
It could be as simple as creating an instance of `ProviderProfile` that points to the NanoGPT's API.

However, I avoid making changes directly in Hermes Agent.
I don't want my code become additional burden to the maintainers,
even though I know many of them are AI agents. _(citation needed, but that's the impression I get from skimming the issues and pull requests)_
I simply want to follow the plugin system as its intended: to extend the original software without making direct changes to it.
