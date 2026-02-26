"""Gemini API interaction for image-to-markdown conversion."""

import base64

from google import genai

from .config import SYSTEM_PROMPT


def convert_image_to_markdown(image_path: str, api_key: str) -> str:
    """Send image to Gemini 2.5 Flash and return the markdown response."""
    client = genai.Client(api_key=api_key)

    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            {
                "role": "user",
                "parts": [
                    {"text": SYSTEM_PROMPT},
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": image_data,
                        }
                    },
                ],
            }
        ],
    )

    return response.text
