from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class GenerationResponseFormat(str, Enum):
    B64_JSON = "b64_json"
    URL = "url"


# TODO Create request & response DTO for list models endpoint

@dataclass(frozen=True)
class GeneratedImageItemDTO:
    b64_json: Optional[str] = None
    url: Optional[str] = None

    @property
    def format(self) -> GenerationResponseFormat:
        return (
            GenerationResponseFormat.URL
            if self.url
            else GenerationResponseFormat.B64_JSON
        )


@dataclass(frozen=True)
class ImageGenerationRequestDTO:
    # Core fields
    prompt: str
    model: str = "hidream"
    n: int = 1
    size: Optional[str] = None
    response_format: GenerationResponseFormat = GenerationResponseFormat.B64_JSON
    user: Optional[str] = None

    # Image inputs (img2img/inpainting)
    image_data_url: Optional[str] = None
    image_data_urls: Optional[List[str]] = None
    mask_data_url: Optional[str] = None

    # Controls (model-specific)
    strength: Optional[int] = None
    guidance_scale: Optional[int] = None
    num_inference_steps: Optional[int] = None
    seed: Optional[int] = None
    kontext_max_mode: Optional[bool] = None

    # Extra arguments passed during construction
    extra_params: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        raw_dict = {
            k: v
            for k, v in asdict(self).items()
            if v is not None and k != "extra_params"
        }
        camel_case_mappings = {
            "image_data_url": "imageDataUrl",
            "image_data_urls": "imageDataUrls",
            "mask_data_url": "maskDataUrl",
        }

        final_dict = {}

        for key, value in raw_dict.items():
            final_key = camel_case_mappings.get(key, key)
            final_dict[final_key] = value

        final_dict.update(self.extra_params)

        return final_dict


@dataclass(frozen=True)
class ImageGenerationResponseDTO:
    created: int
    data: List[GeneratedImageItemDTO]
    cost: int
    payment_source: str
    remaining_balance: int

    @classmethod
    def from_dict(cls, data: dict) -> "ImageGenerationResponseDTO":
        return cls(
            created=data.get("created"),
            data=[
                GeneratedImageItemDTO(
                    b64_json=item.get("b64_json"), url=item.get("url")
                )
                for item in data.get("data", [])
            ],
            cost=data.get("cost"),
            payment_source=data.get("paymentSource"),
            remaining_balance=data.get("remainingBalance"),
        )
