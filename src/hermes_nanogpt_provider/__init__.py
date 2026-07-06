"""NanoGPT provider."""

import logging

from hermes_cli.plugins import PluginContext
from providers import register_provider

from .provider import ModelListEndpoint, nanogpt_model_provider

logger = logging.getLogger(__name__)


def register(_ctx: PluginContext) -> None:
    register_provider(nanogpt_model_provider)


__all__ = ["register", "ModelListEndpoint"]
