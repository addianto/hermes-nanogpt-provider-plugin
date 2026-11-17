# SPDX-License-Identifier: MIT
import logging
from enum import Enum

from hermes_cli.config import get_env_value
from providers import ProviderProfile

logger = logging.getLogger(__name__)

BASE_URL = "https://nano-gpt.com/api/v1"


class ModelListEndpoint(str, Enum):
    CANONICAL = f"{BASE_URL}/models"
    PERSONALIZED = f"{BASE_URL[: BASE_URL.rfind('/')]}/personalized/v1/models"
    SUBSCRIPTION_ONLY = f"{BASE_URL[: BASE_URL.rfind('/')]}/subscription/v1/models"
    PAID_ONLY = f"{BASE_URL[: BASE_URL.rfind('/')]}/paid/v1/models"


ENDPOINT_MAP = {
    "canonical": ModelListEndpoint.CANONICAL,
    "personalized": ModelListEndpoint.PERSONALIZED,
    "subscription": ModelListEndpoint.SUBSCRIPTION_ONLY,
    "paid": ModelListEndpoint.PAID_ONLY,
}

DEFAULT_MODEL_ENDPOINT = ModelListEndpoint.CANONICAL


def _resolve_model_list_endpoint(option: str | None) -> ModelListEndpoint:
    if option is None:
        logger.debug("nanogpt: empty model list option was provided")
        return DEFAULT_MODEL_ENDPOINT

    if option.lower() in ENDPOINT_MAP:
        logger.debug(
            f"nanogpt: resolved model list option '{option}' to '{ENDPOINT_MAP[option.lower()]}'"
        )
        return ENDPOINT_MAP[option.lower()]

    logger.warning(f"nanogpt: unrecognized model list option '{option}'")

    return DEFAULT_MODEL_ENDPOINT

def _hermes_agent_version() -> str:
    hermes_agent_version: str = ""

    # Newer Hermes Agent version has version_info module that provides version resolver function
    # The following checker and resolver code adapted from [hermes-ngrok plugin](https://github.com/ngrok/hermes-ngrok/blob/fe3ed32/model-providers/ngrok/__init__.py),
    # licensed under MIT
    try:
        from hermes_cli.version_info import get_version_info
    except ImportError:
        get_version_info = None

    if get_version_info is not None:
        hermes_agent_version = get_version_info().base_version
    else:
        try:
            from hermes_cli import __version__ as version

            hermes_agent_version = str(version)
        except ImportError:
            hermes_agent_version = ""

    return hermes_agent_version if hermes_agent_version not in ("unknown", "0.0.0") else ""

def _default_headers() -> dict[str, str]:
    version = _hermes_agent_version()
    default_headers: dict[str, str] = {
        "User-Agent": f"hermes-agent/{version} (nanogpt-provider)" if version else "hermes-agent (nanogpt-provider)"
    }

    return default_headers

nanogpt_model_provider = ProviderProfile(
    name="nanogpt",
    aliases=("nanogpt",),
    display_name="NanoGPT",
    description="NanoGPT (pay-as-you-go, OpenAI-compatible AI platform)",
    signup_url="https://nano-gpt.com",
    env_vars=(
        "NANOGPT_API_KEY",
        "NANOGPT_MODEL_LIST_ENDPOINT",
    ),
    default_headers=_default_headers(),
    base_url=BASE_URL,
    models_url=_resolve_model_list_endpoint(
        get_env_value("NANOGPT_MODEL_LIST_ENDPOINT")
    ),
    supports_vision=True,
    fallback_models=(
        "hermes-medium",  # Included in subscription; Suitable for agent work according to NanoGPT's documentation
    ),
)

__all__ = ["nanogpt_model_provider"]
