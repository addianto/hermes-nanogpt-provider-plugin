"""NanoGPT image generation backend.

API documentation: https://docs.nano-gpt.com/api-reference/image-generation
"""
import json
import logging
import os
from functools import cache
from typing import Dict, Any, List, Optional
from urllib.request import Request, urlopen

from agent.image_gen_provider import ImageGenProvider, DEFAULT_ASPECT_RATIO, error_response, resolve_aspect_ratio, \
    success_response

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

# -------------
# Configuration
# -------------

def _load_nanogpt_config() -> Dict[str, Any]:
    """Read NanoGPT configuration section from config.yaml."""
    try:
        from hermes_cli.config import load_config

        config = load_config()
        section = config.get("nanogpt") if isinstance(config, dict) else {}

        return section
    except Exception as exception:
        # TODO: Does debug level appropriate in this exception handling?
        logger.debug("Failed to load NanoGPT config: %s", exception)
        return {}

def _resolve_nanogpt_model() -> str:
    env_override_model = os.environ.get("NANOGPT_IMAGE_MODEL")

    if env_override_model:
        return env_override_model

    config = _load_nanogpt_config()
    nanogpt_config = config.get("nanogpt") if isinstance(config, dict) else {}
    candidate_model: Optional[str] = None

    if nanogpt_config:
        model = nanogpt_config.get("model")
        candidate_model = model if isinstance(model, str) else None

    if candidate_model is None:
        model = config.get("model") if isinstance(config, dict) else {}
        candidate_model = model if isinstance(model, str) else None

    if candidate_model is not None:
        return candidate_model

    return _DEFAULT_MODEL

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
                "display": model.get("name", model.get("id")),
                "strengths": model.get("description", "Unknown"),
                "price": f"{self.__get_average_price_or_none(model)} USD (average)" if self.__get_average_price_or_none(model) else "Unknown",
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
        model = _resolve_nanogpt_model()

        # TODO Use image endpoint query (https://docs.nano-gpt.com/api-reference/endpoint/image-api-model-endpoints)

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
        prompt = (prompt or "").strip()
        aspect = resolve_aspect_ratio(aspect_ratio)
        model = _resolve_nanogpt_model()

        if not prompt:
            return error_response(
                error="Prompt is required and must be a non-empty string",
                error_type="invalid_argument",
                provider="nanogpt",
                model=model,
                aspect_ratio=aspect,
            )

        if not os.environ.get("NANOGPT_API_KEY"):
            return error_response(
                error="NANOGPT_API_KEY is not set",
                error_type="auth_required",
                provider="nanogpt",
                model=model,
                aspect_ratio=aspect,
            )

        # TODO: Properly handle img2img here. Return error_response for now since we haven't implemented img2img
        if image_url or reference_image_urls:
            return self.__handle_img2img()

        # TODO: Create a builder function/method for composing the payload based on the capabilities of the selected model
        payload: Dict[str, Any] = {
            "prompt": prompt,
            "model": model,
            "n": 1,
            "response_format": "b64_json",
        }

        request: Request = Request(
            url=f"{BASE_URL}/images/generations",
            headers={
                "Authorization": f"Bearer {os.environ.get('NANOGPT_API_KEY')}",
                "User-Agent": "nanogpt-hermes-plugin",
                "Content-Type": "application/json",
            },
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
        )

        with urlopen(request) as response:
            raw_data = response.read().decode("utf-8")
            json_data = json.loads(raw_data)
            generated_images: List = json_data.get("data") if isinstance(json_data, dict) else []

        return success_response(
            image=generated_images[0],
            model=model,
            prompt=prompt,
            aspect_ratio=aspect,
            modality="text",
            provider="nanogpt",
        )

    def __handle_img2img(self):
        return error_response(
            error="Image-to-image (img2img) not yet implemented",
            error_type="not_implemented",
            provider="nanogpt",
        )

    @staticmethod
    @cache
    def __get_average_price_or_none(model: Dict[str, Any]) -> Optional[float]:
        pricing = model.get("pricing", None)
        per_image = None if not pricing else pricing.get("per_image", None)

        if not pricing or not per_image:
            return None

        prices = [float(price) for price in per_image.values()]

        return sum(prices) / len(prices)

# -----------------
# Plugin entrypoint
# -----------------

def register(ctx) -> None:
    ctx.register_image_gen_provider(NanoGPTImageGenProvider())
