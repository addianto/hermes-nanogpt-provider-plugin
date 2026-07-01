"""NanoGPT provider."""

from providers import ProviderProfile, register_provider

nanogpt_model_provider = ProviderProfile(
    name="nanogpt",
    aliases=("nanogpt",),
    display_name="NanoGPT",
    description="NanoGPT",
    signup_url="https://nano-gpt.com",
    env_vars=("NANOGPT_API_KEY",),
    base_url="https://nano-gpt.com/api/v1",
    auth_type="api_key",
    default_aux_model="xiaomi/mimo-v2.5",
    fallback_models=(
        "ibm-granite/granite-4.1-8b",
        "nvidia/nemotron-3-super-120b-a12b",
        "deepseek/deepseek-v4-flash",
        "hermes-medium",
    ),
)

register_provider(nanogpt_model_provider)
