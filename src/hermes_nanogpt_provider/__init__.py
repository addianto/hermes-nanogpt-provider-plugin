# SPDX-License-Identifier: MIT
"""NanoGPT model provider."""

import logging

from hermes_cli.plugins import PluginContext
from providers import register_provider

from hermes_nanogpt_provider.provider import nanogpt_model_provider

logger = logging.getLogger(__name__)


def register(_ctx: PluginContext | None = None) -> None:
    logger.debug("nanogpt: registering provider")
    register_provider(nanogpt_model_provider)


__version__ = "0.4.3"
__all__ = ["register"]
