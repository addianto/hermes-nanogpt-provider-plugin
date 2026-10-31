# SPDX-License-Identifier: MIT
"""NanoGPT model provider."""

import logging

from hermes_cli.plugins import PluginContext
from providers import register_provider

from hermes_nanogpt_provider.provider import nanogpt_model_provider

logger = logging.getLogger(__name__)


def _resolve_version() -> str:
    import tomllib
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version as distribution_version
    from pathlib import Path

    try:
        return distribution_version("hermes-nanogpt-provider")
    except PackageNotFoundError:
        logger.debug(
            "nanogpt: Plugin not installed in a Python environment and is likely installed via clone method directly to a Hermes plugins directory",
        )

        pyproject_file = Path(__file__).resolve().parents[2] / "pyproject.toml"

        try:
            with pyproject_file.open("rb") as file:
                return tomllib.load(file)["project"]["version"]
        except (OSError, KeyError, tomllib.TOMLDecodeError):
            logger.exception("nanogpt: Unable to read the pyproject.toml field")
            return "0+unknown"


def register(_ctx: PluginContext | None = None) -> None:
    logger.debug("nanogpt: registering provider")
    register_provider(nanogpt_model_provider)


__version__ = _resolve_version()
__all__ = ["register"]
