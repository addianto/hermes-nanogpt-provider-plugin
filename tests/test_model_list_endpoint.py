import importlib
import logging
import os
from unittest.mock import patch

import pytest

from hermes_nanogpt_provider import ModelListEndpoint


@pytest.mark.parametrize(
    "option,expected_url",
    [
        ("canonical", ModelListEndpoint.CANONICAL.value),
        ("personalized", ModelListEndpoint.PERSONALIZED.value),
        ("subscription", ModelListEndpoint.SUBSCRIPTION_ONLY.value),
        ("paid", ModelListEndpoint.PAID_ONLY.value),
        ("CANONICAL", ModelListEndpoint.CANONICAL.value),
        ("PERSONALIZED", ModelListEndpoint.PERSONALIZED.value),
        ("SUBSCRIPTION", ModelListEndpoint.SUBSCRIPTION_ONLY.value),
        ("PAID", ModelListEndpoint.PAID_ONLY.value),
        (None, ModelListEndpoint.CANONICAL.value),
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


def test_provider_resolves_invalid_endpoint_to_default(caplog) -> None:
    with patch.dict(os.environ, {"NANOGPT_MODEL_LIST_ENDPOINT": "invalid"}):
        import hermes_nanogpt_provider.provider

        with caplog.at_level(logging.WARNING):
            importlib.reload(hermes_nanogpt_provider.provider)
            provider = hermes_nanogpt_provider.provider.nanogpt_model_provider
            assert provider.models_url == ModelListEndpoint.CANONICAL.value
            assert any(
                "nanogpt: unrecognized model list option 'invalid'" in record.message
                for record in caplog.records
            )
