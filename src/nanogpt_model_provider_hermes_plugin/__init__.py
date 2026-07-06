"""NanoGPT provider."""

import os
from enum import Enum
from typing import Optional

from providers import ProviderProfile, register_provider

BASE_URL = "https://nano-gpt.com/api/v1"


class ModelListEndpoint(str, Enum):
    CANONICAL = f"{BASE_URL}/models"
    PERSONALIZED = f"{BASE_URL[: BASE_URL.rfind('/')]}/personalized/v1/models"
    SUBSCRIPTION_ONLY = f"{BASE_URL[: BASE_URL.rfind('/')]}/subscription/v1/models"
    PAID_ONLY = f"{BASE_URL[: BASE_URL.rfind('/')]}/paid/v1/models"


DEFAULT_MODEL_ENDPOINT = ModelListEndpoint.CANONICAL


def _resolve_model_list_endpoint(option: Optional[str]) -> ModelListEndpoint:
    if option is None:
        return DEFAULT_MODEL_ENDPOINT

    if option.lower() == "canonical":
        return ModelListEndpoint.CANONICAL
    if option.lower() == "personalized":
        return ModelListEndpoint.PERSONALIZED
    if option.lower() == "subscriptiononly":
        return ModelListEndpoint.SUBSCRIPTION_ONLY
    if option.lower() == "paidonly":
        return ModelListEndpoint.PAID_ONLY

    return DEFAULT_MODEL_ENDPOINT


nanogpt_model_provider = ProviderProfile(
    name="nanogpt",
    aliases=("nanogpt",),
    display_name="NanoGPT",
    description="NanoGPT is a pay-as-you-go, OpenAI-compatible AI platform that provides routing to frontier models and open-source models.",
    signup_url="https://nano-gpt.com",
    env_vars=("NANOGPT_API_KEY",),
    base_url=BASE_URL,
    models_url=_resolve_model_list_endpoint(
        os.environ.get("NANOGPT_MODEL_LIST_ENDPOINT")
    ),
    supports_vision=True,
    fallback_models=(
        "hermes-medium",  # Included in subscription; Suitable for agent work according to NanoGPT's documentation
    ),
)


def register() -> None:
    register_provider(nanogpt_model_provider)
