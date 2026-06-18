"""NanoGPT image generation plugin"""
import json
import logging
import os
from urllib.error import URLError, HTTPError
from urllib.request import urlopen, Request
from typing import Any, Dict, List

from agent.image_gen_provider import ImageGenProvider, DEFAULT_ASPECT_RATIO, error_response, success_response

logger = logging.getLogger(__name__)

BASE_URL = "https://nano-gpt.com/api/v1"
DEFAULT_MODEL = "hidream"


class NanoGPTImageGenProvider(ImageGenProvider):

    @property
    def name(self) -> str:
        return "nanogpt"

    @property
    def display_name(self) -> str:
        return "NanoGPT"

    def is_available(self) -> bool:
        return True if self.__api_key else False

    def list_models(self) -> List[Dict[str, Any]]:
        request: Request = Request(
            f"{BASE_URL}/image-models?detailed=true",
            headers={
                "Authorization": f"Bearer {self.__api_key}",
                "Content-Type": "application/json",
            },
            method="GET",
        )
        models = []

        try:
            with urlopen(request) as response:
                data = response.read()
        except HTTPError as http_error:
            logger.exception(
                "The server could not fulfill the request. Error code: %s", http_error.code
            )
            return models
        except URLError as url_error:
            logger.exception("The server could not be reached. Reason: %s", url_error.reason)
            return models

        try:
            payload = json.loads(data)
        except json.JSONDecodeError as decode_error:
            logger.exception("Failed to parse image-models response: %s", decode_error)
            return models

        # Response shape: {"object": "list", "data": [<model>, ...], "meta": {...}}
        entries = payload.get("data") if isinstance(payload, dict) else None
        if not isinstance(entries, list):
            logger.warning(
                "Unexpected payload shape: top-level=%s",
                type(payload).__name__,
            )
            return models

        for entry in entries:
            if not isinstance(entry, dict) or "id" not in entry:
                continue
            # Defensive filter: the /image-models endpoint should already be image-only,
            # but trust capabilities over the endpoint name in case that ever changes.
            if not entry.get("capabilities", {}).get("image_generation"):
                continue

            models.append(entry)


        MODELS = [self.__to_model_picker_entry(model) for model in models]
        logger.debug("Loaded %d image generation models from NanoGPT", len(MODELS))

        return MODELS

    def generate(self, prompt: str, aspect_ratio: str = DEFAULT_ASPECT_RATIO, **kwargs: Any) -> Dict[str, Any]:
        if not prompt:
            return error_response(
                error="Prompt is required",
                error_type="invalid_input",
                provider=self.name,
                prompt="",
                aspect_ratio=aspect_ratio,
            )

        # TODO Actually implement the generate image logic
        return {}

    @staticmethod
    def __to_model_picker_entry(model):
        return {
            "id": model["id"],
            "display": model["name"],
            "speed": "varies",
            "strengths": model["description"],
            "price": "varies"
        }

    @property
    def __api_key(self):
        return os.environ.get("NANOGPT_API_KEY")
