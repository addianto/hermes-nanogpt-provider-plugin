from hermes_nanogpt_provider import ModelListEndpoint


def test_model_list_endpoint_values():
    assert ModelListEndpoint.CANONICAL == "https://nano-gpt.com/api/v1/models"
    assert (
        ModelListEndpoint.PERSONALIZED
        == "https://nano-gpt.com/api/personalized/v1/models"
    )
    assert ModelListEndpoint.PAID_ONLY == "https://nano-gpt.com/api/paid/v1/models"
    assert (
        ModelListEndpoint.SUBSCRIPTION_ONLY
        == "https://nano-gpt.com/api/subscription/v1/models"
    )
