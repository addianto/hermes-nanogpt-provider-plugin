# SPDX-License-Identifier: MIT
import importlib
import logging
import os
from unittest.mock import patch

import pytest


@pytest.mark.parametrize(
    "option,expected_url",
    [
        ("canonical", "https://nano-gpt.com/api/v1/models"),
        ("personalized", "https://nano-gpt.com/api/personalized/v1/models"),
        ("subscription", "https://nano-gpt.com/api/subscription/v1/models"),
        ("paid", "https://nano-gpt.com/api/paid/v1/models"),
        ("CANONICAL", "https://nano-gpt.com/api/v1/models"),
        ("PERSONALIZED", "https://nano-gpt.com/api/personalized/v1/models"),
        ("SUBSCRIPTION", "https://nano-gpt.com/api/subscription/v1/models"),
        ("PAID", "https://nano-gpt.com/api/paid/v1/models"),
    ],
)
def test_provider_resolves_correct_endpoint(
    option: str | None, expected_url: str
) -> None:
    env = {} if option is None else {"NANOGPT_MODEL_LIST_ENDPOINT": option}
    with patch.dict(os.environ, env, clear=(option is None)):
        import hermes_nanogpt_provider.provider

        importlib.reload(hermes_nanogpt_provider.provider)
        provider = hermes_nanogpt_provider.provider.nanogpt_model_provider
        assert provider.models_url == expected_url


def test_provider_resolves_default_endpoint_when_option_not_set() -> None:
    with patch("hermes_cli.config.get_env_value") as mock_get_env_value:
        mock_get_env_value.side_effect = lambda _: None
        import hermes_nanogpt_provider.provider

        importlib.reload(hermes_nanogpt_provider.provider)
        provider = hermes_nanogpt_provider.provider.nanogpt_model_provider
        assert provider.models_url == "https://nano-gpt.com/api/v1/models"


def test_provider_resolves_invalid_endpoint_to_default(caplog) -> None:
    with patch.dict(os.environ, {"NANOGPT_MODEL_LIST_ENDPOINT": "invalid"}):
        import hermes_nanogpt_provider.provider

        with caplog.at_level(logging.WARNING):
            importlib.reload(hermes_nanogpt_provider.provider)
            provider = hermes_nanogpt_provider.provider.nanogpt_model_provider
            assert provider.models_url == "https://nano-gpt.com/api/v1/models"
            assert any(
                "nanogpt: unrecognized model list option 'invalid'" in record.message
                for record in caplog.records
            )
