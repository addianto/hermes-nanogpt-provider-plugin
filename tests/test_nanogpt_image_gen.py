import os
from typing import Any, Dict, List
from unittest.mock import patch

import pytest

from nanogpt_hermes_plugin.image_gen.nanogpt import NanoGPTImageGenProvider


@pytest.fixture
def provider() -> NanoGPTImageGenProvider:
    return NanoGPTImageGenProvider()


@pytest.fixture
def sample_models_json_data() -> List[Dict[str, Any]]:
    return [
        {
            "id": "chroma",
            "object": "model",
            "created": 1754956800,
            "owned_by": "chroma",
            "name": "Chroma",
            "description": "Uncensored text-to-image model. Supports custom resolutions up to 1536x1536.",
            "architecture": {
                "modality": "text->image",
                "input_modalities": ["text"],
                "output_modalities": ["image"],
            },
            "pricing": {
                "per_image": {
                    "1536x1536": 0.0255,
                    "1536x1024": 0.0255,
                    "1024x1536": 0.0255,
                    "1024x1024": 0.0255,
                    "512x512": 0.0255,
                    "768x1024": 0.0255,
                    "576x1024": 0.0255,
                    "1024x768": 0.0255,
                    "1024x576": 0.0255,
                    "1024*1024": 0.0255,
                    "512*512": 0.0255,
                    "768*1024": 0.0255,
                    "576*1024": 0.0255,
                    "1024*768": 0.0255,
                    "1024*576": 0.0255,
                    "1536*1536": 0.0255,
                    "1536*1024": 0.0255,
                    "1024*1536": 0.0255,
                    "auto": 0.0255,
                },
                "currency": "USD",
            },
            "capabilities": {
                "image_generation": True,
                "image_to_image": False,
                "inpainting": False,
                "nsfw": False,
            },
            "supported_parameters": {
                "resolutions": [
                    "1536x1536",
                    "1536x1024",
                    "1024x1536",
                    "1024x1024",
                    "512x512",
                    "768x1024",
                    "576x1024",
                    "1024x768",
                    "1024x576",
                ],
                "max_images": 4,
                "max_output_images": 4,
            },
            "category": "More",
        },
        {
            "id": "hidream",
            "object": "model",
            "created": 1704067200,
            "owned_by": "hidream",
            "name": "Hidream",
            "description": "Hidream I1 Full, the latest and greatest image generation model from Hidream.",
            "architecture": {
                "modality": "text->image",
                "input_modalities": ["text"],
                "output_modalities": ["image"],
            },
            "pricing": {
                "per_image": {
                    "1024x1024": 0.0153,
                    "768x1360": 0.0153,
                    "1360x768": 0.0153,
                    "880x1168": 0.0153,
                    "1168x880": 0.0153,
                    "1248x832": 0.0153,
                    "832x1248": 0.0153,
                    "1024x768": 0.0153,
                    "768x1024": 0.0153,
                    "1024x576": 0.0153,
                    "576x1024": 0.0153,
                    "1408x1024": 0.0153,
                    "1024x1408": 0.0153,
                    "512x512": 0.0153,
                    "2048x2048": 0.0153,
                    "1920x1088": 0.0153,
                    "1088x1920": 0.0153,
                },
                "currency": "USD",
            },
            "capabilities": {
                "image_generation": True,
                "image_to_image": False,
                "inpainting": False,
                "nsfw": False,
            },
            "supported_parameters": {
                "resolutions": [
                    "1024x1024",
                    "768x1360",
                    "1360x768",
                    "880x1168",
                    "1168x880",
                    "1248x832",
                    "832x1248",
                ],
                "max_images": 20,
                "max_output_images": 20,
            },
            "icon_url": "/icons/Hidream.webp",
            "category": "image",
        },
        {
            "id": "qwen-image",
            "object": "model",
            "created": 1754524800,
            "owned_by": "qwen",
            "name": "Qwen Image",
            "description": "Latest release (v2509, 25-09). Qwen-Image is an image generation foundation model that excels at complex text rendering and precise image editing, with support for multi-image editing.",
            "architecture": {
                "modality": "text+image->image",
                "input_modalities": ["text", "image"],
                "output_modalities": ["image"],
            },
            "pricing": {
                "per_image": {
                    "1024x1024": 0.02,
                    "512x512": 0.02,
                    "768x1024": 0.02,
                    "576x1024": 0.02,
                    "1024x768": 0.02,
                    "1024x576": 0.02,
                    "auto": 0.02,
                },
                "currency": "USD",
            },
            "capabilities": {
                "image_generation": True,
                "image_to_image": True,
                "inpainting": False,
                "nsfw": False,
            },
            "supported_parameters": {
                "resolutions": [
                    "auto",
                    "1024x1024",
                    "512x512",
                    "768x1024",
                    "576x1024",
                    "1024x768",
                    "1024x576",
                ],
                "max_images": 4,
                "max_output_images": 4,
                "max_input_images": 3,
                "input_image_constraints": {
                    "max_items": 3,
                    "route": {
                        "min_width": 8,
                        "min_height": 8,
                        "max_bytes": 31457280,
                        "formats": ["png", "jpeg", "webp"],
                        "source": "route-preflight",
                        "note": "NanoGPT route-level validation before provider submission.",
                    },
                },
            },
            "icon_url": "/icons/Qwen.svg",
            "category": "image",
        },
    ]


class TestIsAvailable:
    """Test suite for NanoGPTImageGenProvider.is_available()."""

    def test_available_when_api_key_set(self, provider: NanoGPTImageGenProvider):
        with patch.dict(os.environ, {"NANOGPT_API_KEY": "sk-test"}):
            assert provider.is_available() is True

    def test_unavailable_when_api_key_missing(self, provider: NanoGPTImageGenProvider):
        with patch.dict(os.environ, {}, clear=True):
            # Remove NANOGPT_API_KEY if it exists in the real environment
            env = os.environ.copy()
            env.pop("NANOGPT_API_KEY", None)
            with patch.dict(os.environ, env, clear=True):
                assert provider.is_available() is False

    def test_unavailable_when_api_key_empty(self, provider: NanoGPTImageGenProvider):
        with patch.dict(os.environ, {"NANOGPT_API_KEY": ""}):
            assert provider.is_available() is False


class TestListModels:
    """Test suite for NanoGPTImageGenProvider.list_models()."""

    def test_returns_list_success(
        self,
        provider: NanoGPTImageGenProvider,
        sample_models_json_data: List[Dict[str, Any]],
    ):
        with patch(
            "nanogpt_hermes_plugin.image_gen.nanogpt.list_image_models"
        ) as mock_list_image_models:
            mock_list_image_models.return_value = sample_models_json_data

            models = provider.list_models()

            assert isinstance(models, list)
            assert all(model.get("id", "") != "" for model in models)

    # TODO Add negative & edge test cases such as: network failure