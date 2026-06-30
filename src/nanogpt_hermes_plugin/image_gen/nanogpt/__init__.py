"""NanoGPT image generation backend.

API documentation: https://docs.nano-gpt.com/api-reference/image-generation
"""

import logging
import os
from typing import Any, Dict, List, Optional

from agent.image_gen_provider import (
    DEFAULT_ASPECT_RATIO,
    ImageGenProvider,
    error_response,
    resolve_aspect_ratio,
    save_b64_image,
    save_url_image,
    success_response,
)

from nanogpt_hermes_plugin.image_gen.nanogpt.builder import (
    ImageGenerationRequestBuilder,
)
from nanogpt_hermes_plugin.image_gen.nanogpt.client import (
    generate_image_img2img,
    generate_image_txt2img, list_image_models,
)
from nanogpt_hermes_plugin.image_gen.nanogpt.dto import (
    GenerationResponseFormat,
)

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

_DEFAULT_MODEL = "hidream"

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
        logger.debug("Failed to load NanoGPT config: %s", exception)
        return {}


def _resolve_nanogpt_model() -> str:
    env_override_model = os.environ.get("NANOGPT_IMAGE_MODEL")

    if env_override_model:
        return env_override_model

    config = _load_nanogpt_config()
    candidate_model: Optional[str] = None

    if isinstance(config, dict) and len(config) != 0:
        model = config.get("model")
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
        models = list_image_models(BASE_URL)

        return [
            {
                "id": model.get("id"),
                "display": model.get("name", model.get("id")),
                "strengths": model.get("description", "Unknown"),
                "price": f"{self.__get_average_price_or_none(model)} USD (average)"
                if self.__get_average_price_or_none(model)
                else "Unknown",
            }
            for model in models
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
        models = list_image_models(BASE_URL)
        current_model = _resolve_nanogpt_model()

        for model in models:
            if model.get("id") == current_model:
                return {
                    "modalities": model.get("architecture").get("input_modalities")
                }

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
                prompt=prompt,
                aspect_ratio=aspect,
            )

        # TODO Build the request payload according to the model capabilities. Right now it is still hardcoded and not dynamic.
        generation_request_builder = (
            ImageGenerationRequestBuilder().with_prompt(prompt).with_model(model)
        )
        payload = generation_request_builder.build()

        # TODO Handle img2img properly. Currently this implementation is only a placeholder and not working.
        response = (
            generate_image_txt2img(BASE_URL, os.environ.get("NANOGPT_API_KEY"), payload)
            if not image_url and not reference_image_urls
            else generate_image_img2img(
                BASE_URL, os.environ.get("NANOGPT_API_KEY"), payload
            )
        )
        image_data = response.data[0]
        saved_image = (
            save_url_image(image_data.url)
            if image_data.format == GenerationResponseFormat.URL
            else save_b64_image(image_data.b64_json)
        )

        return success_response(
            image=str(saved_image),
            model=model,
            prompt=prompt,
            aspect_ratio=aspect,
            provider="nanogpt",
            modality="text",
        )

    @staticmethod
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
