"""OpenRouter API interaction for image-to-markdown conversion."""

import base64

import requests

from .config import SYSTEM_PROMPT


def convert_image_to_markdown(image_path: str, api_key: str, model: str) -> str:
    """Send image to OpenRouter and return the markdown response."""
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_data}",
                            },
                        },
                    ],
                },
            ],
        },
    )

    if not response.ok:
        raise ConnectionError(f"OpenRouter API error: {response.status_code} {response.text}")

    return response.json()["choices"][0]["message"]["content"]
