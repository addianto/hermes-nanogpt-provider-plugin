# SPDX-License-Identifier: MIT
"""NanoGPT model provider plugin entrypoint."""

import logging
import sys
from pathlib import Path

from hermes_cli.plugins import PluginContext

logger = logging.getLogger(__name__)


def register(_ctx: PluginContext | None = None) -> None:
    src_dir = str(Path(__file__).parent / "src")
    logger.debug(f"nanogpt: src_dir: {src_dir}")

    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
        logger.debug(f"nanogpt: appended src_dir to sys.path: {sys.path}")

    from hermes_nanogpt_provider import register as nanogpt_register

    nanogpt_register(_ctx)


register()
