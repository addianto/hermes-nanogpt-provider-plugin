"""NanoGPT model provider."""

import logging

from hermes_cli.plugins import PluginContext
from providers import register_provider

from hermes_nanogpt_provider.provider import ModelListEndpoint, nanogpt_model_provider

logger = logging.getLogger(__name__)


def register(_ctx: PluginContext = None) -> None:
    logger.debug("nanogpt: registering provider")
    register_provider(nanogpt_model_provider)


__version__ = "0.3.0"
__all__ = ["register", "ModelListEndpoint"]
