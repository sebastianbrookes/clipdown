#!/usr/bin/env python3
"""Convert clipboard images to markdown via Google Gemini 2.0 Flash."""

import base64
import os
import subprocess
import sys
import tempfile

from google import genai

NOTIFICATION_TITLE = "Clipboard \u2192 MD"

SYSTEM_PROMPT = """\
Convert this image to clean, well-structured markdown.
Rules:
- Output ONLY the markdown content, no commentary or explanation
- No wrapping code fences (do not wrap output in ```markdown``` blocks)
- Preserve the logical structure: headings, lists, tables, code blocks
- For code snippets in the image, use appropriate fenced code blocks with language tags
- For tables, use standard markdown table syntax
- Be precise with the text content \u2014 do not paraphrase or summarize"""


def notify(title: str, message: str) -> None:
    """Send a macOS notification via osascript."""
    subprocess.run(
        [
            "osascript",
            "-e",
            f'display notification "{message}" with title "{title}"',
        ],
        check=False,
    )


def load_api_key() -> str:
    """Load GEMINI_API_KEY from env var or .env file in script directory."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key

    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() == "GEMINI_API_KEY":
                        return v.strip()

    raise EnvironmentError("GEMINI_API_KEY not configured \u2014 check .env file")


def extract_clipboard_image() -> str:
    """Extract clipboard image to a temp PNG file using pngpaste.

    Returns the path to the temp file.
    Raises FileNotFoundError if pngpaste is not installed.
    Raises RuntimeError if no image is on the clipboard.
    """
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    tmp.close()

    try:
        result = subprocess.run(
            ["pngpaste", tmp.name],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        os.unlink(tmp.name)
        raise FileNotFoundError(
            "pngpaste not found \u2014 run: brew install pngpaste"
        ) from exc

    if result.returncode != 0:
        os.unlink(tmp.name)
        raise RuntimeError("No image found on clipboard")

    return tmp.name


def convert_image_to_markdown(image_path: str, api_key: str) -> str:
    """Send image to Gemini 2.0 Flash and return the markdown response."""
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


def write_to_clipboard(text: str) -> None:
    """Write text to the macOS clipboard via pbcopy."""
    subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)


def cleanup_temp_file(path: str) -> None:
    """Silently remove a temp file."""
    try:
        os.unlink(path)
    except OSError:
        pass


def main() -> None:
    """Orchestrate the clipboard-to-markdown pipeline."""
    image_path = None
    try:
        api_key = load_api_key()
        image_path = extract_clipboard_image()
        markdown = convert_image_to_markdown(image_path, api_key)
        write_to_clipboard(markdown)
        notify(NOTIFICATION_TITLE, "Markdown copied to clipboard \u2713")

    except FileNotFoundError as e:
        notify(NOTIFICATION_TITLE, str(e))
        sys.exit(1)

    except RuntimeError as e:
        notify(NOTIFICATION_TITLE, str(e))
        sys.exit(1)

    except ConnectionError:
        notify(NOTIFICATION_TITLE, "Network error \u2014 check your connection")
        sys.exit(1)

    except EnvironmentError as e:
        notify(NOTIFICATION_TITLE, str(e))
        sys.exit(1)

    except Exception as e:  # noqa: BLE001
        notify(NOTIFICATION_TITLE, f"API error: {e}")
        sys.exit(1)

    finally:
        if image_path:
            cleanup_temp_file(image_path)


if __name__ == "__main__":
    main()
