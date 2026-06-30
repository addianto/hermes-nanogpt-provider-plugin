from typing import Dict, Optional, List, Any

from nanogpt_hermes_plugin.image_gen.nanogpt.dto import ResponseFormat, ImageGenerationRequestDTO


class ImageGenerationRequestBuilder:
    def __init__(self) -> None:
        # Image generation parameters according to NanoGPT's official documentation
        self._prompt: Optional[str] = None
        self._model: str = "hidream"
        self._n: int = 1
        self._size: Optional[str] = None
        self._response_format: ResponseFormat = ResponseFormat.B64_JSON
        self._user: Optional[str] = None
        self._image_data_url: Optional[str] = None
        self._image_data_urls: Optional[List[str]] = None
        self._mask_data_url: Optional[str] = None
        self._strength: Optional[int] = None
        self._guidance_scale: Optional[int] = None
        self._num_inference_steps: Optional[int] = None
        self._seed: Optional[int] = None
        self._kontext_max_mode: Optional[bool] = None

        # A dictionary to track varying parameters
        self._extra_params: Dict[str, Any] = {}

    def with_prompt(self, prompt: Optional[str]) -> "ImageGenerationRequestBuilder":
        self._prompt = prompt
        return self

    def with_model(self, model: str) -> "ImageGenerationRequestBuilder":
        self._model = model
        return self

    def with_n(self, n: int) -> "ImageGenerationRequestBuilder":
        self._n = n
        return self

    def with_size(self, size: Optional[str]) -> "ImageGenerationRequestBuilder":
        self._size = size
        return self

    def with_response_format(
        self, response_format: ResponseFormat
    ) -> "ImageGenerationRequestBuilder":
        self._response_format = response_format
        return self

    def with_user(self, user: Optional[str]) -> "ImageGenerationRequestBuilder":
        self._user = user
        return self

    def with_image_data_url(
        self, image_data_url: Optional[str]
    ) -> "ImageGenerationRequestBuilder":
        self._image_data_url = image_data_url
        return self

    def with_image_data_urls(
        self, image_data_urls: Optional[List[str]]
    ) -> "ImageGenerationRequestBuilder":
        self._image_data_urls = image_data_urls
        return self

    def with_mask_data_url(
        self, mask_data_url: Optional[str]
    ) -> "ImageGenerationRequestBuilder":
        self._mask_data_url = mask_data_url
        return self

    def with_strength(self, strength: Optional[int]) -> "ImageGenerationRequestBuilder":
        self._strength = strength
        return self

    def with_guidance_scale(self, guidance_scale: Optional[int]) -> "ImageGenerationRequestBuilder":
        self._guidance_scale = guidance_scale
        return self

    def with_num_inference_steps(self, num_inference_steps: Optional[int]) -> "ImageGenerationRequestBuilder":
        self._num_inference_steps = num_inference_steps
        return self

    def with_seed(self, seed: Optional[int]) -> "ImageGenerationRequestBuilder":
        self._seed = seed
        return self

    def with_kontext_max_mode(
        self, kontext_max_mode: Optional[bool]
    ) -> "ImageGenerationRequestBuilder":
        self._kontext_max_mode = kontext_max_mode
        return self

    def set_custom_parameter(self, key: str, value: Any) -> "ImageGenerationRequestBuilder":
        self._extra_params[key] = value
        return self

    def set_custom_kwargs(self, **kwargs) -> "ImageGenerationRequestBuilder":
        self._extra_params.update(kwargs)
        return self

    def build(self) -> ImageGenerationRequestDTO:
        if not self._prompt:
            raise ValueError("Cannot build ImageGenerationRequestDTO without prompt")

        return ImageGenerationRequestDTO(
            prompt=self._prompt,
            model=self._model,
            n=self._n,
            size=self._size,
            response_format=self._response_format,
            user=self._user,
            image_data_url=self._image_data_url,
            image_data_urls=self._image_data_urls,
            mask_data_url=self._mask_data_url,
            strength=self._strength,
            guidance_scale=self._guidance_scale,
            num_inference_steps=self._num_inference_steps,
            seed=self._seed,
            kontext_max_mode=self._kontext_max_mode,
            extra_params=self._extra_params,
        )