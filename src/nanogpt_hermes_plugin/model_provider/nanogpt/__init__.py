"""NanoGPT provider."""

from providers import ProviderProfile, register_provider

nanogpt_model_provider = ProviderProfile(
    name="nanogpt",
    aliases=("nanogpt",),
    display_name="NanoGPT",
    signup_url="https://nano-gpt.com",
    env_vars=("NANOGPT_API_KEY",),
    base_url="https://nano-gpt.com/api/v1",
)

register_provider(nanogpt_model_provider)
