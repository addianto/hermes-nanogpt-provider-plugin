import logging
from enum import Enum
from typing import Optional

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


def _resolve_model_list_endpoint(option: Optional[str]) -> ModelListEndpoint:
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
    base_url=BASE_URL,
    # TODO Fix/implement personalized models endpoint
    models_url=_resolve_model_list_endpoint(
        get_env_value("NANOGPT_MODEL_LIST_ENDPOINT")
    ),
    supports_vision=True,
    fallback_models=(
        "hermes-medium",  # Included in subscription; Suitable for agent work according to NanoGPT's documentation
    ),
)

__all__ = ["nanogpt_model_provider", "ModelListEndpoint"]
