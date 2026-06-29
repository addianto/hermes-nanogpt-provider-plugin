"""NanoGPT image generation backend.

API documentation: https://docs.nano-gpt.com/api-reference/image-generation
"""
import json
import logging
import os
from typing import Dict, Any, List, Optional

from agent.image_gen_provider import ImageGenProvider, DEFAULT_ASPECT_RATIO

logger = logging.getLogger(__name__)

# ---------
# Constants
# ---------

BASE_URL = "https://nano-gpt.com/api/v1"

# ---------------------
# Default model catalog
# ---------------------

# We included the subscription models as default models since the image generation is free for subscriber plan.
# Last update: 2026-06-29

_MODELS: Dict[str, Dict[str, Any]] = {
    # Reference: https://nano-gpt.com/models/image/chroma
    "chroma": {
        "id": "chroma",
        "display": "Chroma",
        "strengths": "Uncensored text-to-image model. Supports custom resolution up to 1536x1536.",
        "price": "0.025 USD per image",
        "modality": "text->image",
    },
    # Reference: https://nano-gpt.com/models/image/hidream
    "hidream": {
        "id": "hidream",
        "display": "Hidream",
        "strengths": "Hidream I1 Full, the latest and greatest image generation model from Hidream.",
        "price": "0.015 USD per image",
        "modality": "text->image",
    },
    # Reference: https://nano-gpt.com/models/image/qwen-image
    "qwen-image": {
        "id": "qwen-image",
        "display": "Qwen Image",
        "strengths": "Latest release (v2509, 25-09). Qwen-Image is an image generation foundation model that excels at complex text rendering and precise image editing, with support for multi-image editing.",
        "price": "0.020 USD per image",
        "modality": "text+image->image",
    },
    # Reference: https://nano-gpt.com/models/image/step-image-edit-2
    "step-image-edit-2": {
        "id": "step-image-edit-2",
        "display": "Step Image Edit 2",
        "strengths": "A lightweight image generation and editing model for fast text-to-image and prompt-guided image edits. Supports single-image edits and returns edited images at the input image size. Prompts are limited to 512 characters; negative prompts have the same limit.",
        "price": "0.003 USD per image",
        "modality": "text+image->image",
    },
    # Reference: https://nano-gpt.com/models/image/z-image-turbo
    "z-image-turbo": {
        "id": "z-image-turbo",
        "display": "Z Image Turbo",
        "strengths": "Z Image Turbo is a fast, high-quality image generation model optimized for speed. Generate detailed images with cinematic quality, film grain effects, and artistic styles.",
        "price": "0.012 USD per image",
        "modality": "text->image",
    },
}

_DEFAULT_MODEL = "chroma"

# --------
# Provider
# --------


class NanoGPTImageGenProvider(ImageGenProvider):
    @property
    def name(self) -> str:
        return "nanogpt"

    @property
    def display_name(self) -> str:
        return "NanoGPT"

    def is_available(self) -> bool:
        return bool(os.environ.get("NANOGPT_API_KEY", False))

    def list_models(self) -> List[Dict[str, Any]]:
        from urllib.request import Request, urlopen

        request: Request = Request(
            url=f"{BASE_URL}/image-models?detailed=true",
            headers={
                "User-Agent": "nanogpt-hermes-plugin",
                "Content-Type": "application/json",
            },
            method="GET",
        )

        with urlopen(request) as response:
            raw_data = response.read().decode("utf-8")
            json_data = json.loads(raw_data)
            models = json_data.get("data") if isinstance(json_data, dict) else None

        return [
            {
                "id": model.get("id"),
            } for model in models
        ]

    def get_setup_schema(self) -> Dict[str, Any]:
        return {
            "name": "NanoGPT",
            "badge": "paid",
            "env_vars": [
                {
                    "key": "NANOGPT_API_KEY",
                    "prompt": "NanoGPT API key",
                    "url": "https://nano-gpt.com/api",
                }
            ],
        }

    def default_model(self) -> Optional[str]:
        return _DEFAULT_MODEL

    def capabilities(self) -> Dict[str, Any]:
        return super().capabilities()

    def generate(
        self,
        prompt: str,
        aspect_ratio: str = DEFAULT_ASPECT_RATIO,
        *,
        image_url: Optional[str] = None,
        reference_image_urls: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        pass


# -----------------
# Plugin entrypoint
# -----------------


def register(ctx) -> None:
    ctx.register_image_gen_provider(NanoGPTImageGenProvider())
