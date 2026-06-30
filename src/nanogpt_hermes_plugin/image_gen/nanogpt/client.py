import json
import urllib
from urllib.request import urlopen

from nanogpt_hermes_plugin.image_gen.nanogpt.dto import (
    ImageGenerationRequestDTO,
    ImageGenerationResponseDTO,
)


def __execute_request(request: urllib.request.Request) -> ImageGenerationResponseDTO:
    try:
        with urlopen(request) as response:
            response_raw = response.read().decode("utf-8")
            response_json = json.loads(response_raw)

            return ImageGenerationResponseDTO.from_dict(response_json)
    except urllib.request.HTTPError as error:
        error_body = error.read().decode("utf-8")
        raise RuntimeError(f"API Error ({error.code}): {error_body}") from error


def generate_image_txt2img(
    base_url: str, api_key: str, params: ImageGenerationRequestDTO
) -> ImageGenerationResponseDTO:
    url = f"{base_url}/images/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "nanogpt-hermes-plugin",
    }
    encoded_data = json.dumps(params.to_dict()).encode("utf-8")

    return __execute_request(
        urllib.request.Request(url, data=encoded_data, headers=headers)
    )


def generate_image_img2img(
    base_url: str, api_key: str, params: ImageGenerationRequestDTO
) -> ImageGenerationResponseDTO:
    url = f"{base_url}/images/edits"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "nanogpt-hermes-plugin",
    }
    encoded_data = json.dumps(params.to_dict()).encode("utf-8")

    return __execute_request(
        urllib.request.Request(url, data=encoded_data, headers=headers)
    )
