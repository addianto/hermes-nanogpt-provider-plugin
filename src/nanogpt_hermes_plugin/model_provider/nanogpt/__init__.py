"""NanoGPT provider."""

from providers import ProviderProfile, register_provider

nanogpt_model_provider = ProviderProfile(
    name="nanogpt",
    aliases=("nanogpt",),
    display_name="NanoGPT",
    signup_url="https://nano-gpt.com",
    env_vars=("NANOGPT_API_KEY",),
    base_url="https://nano-gpt.com/api/v1",
    default_aux_model="xiaomi/mimo-v2.5:thinking",
)


def register() -> None:
    register_provider(nanogpt_model_provider)
