"""Configuration and API key management."""

import os

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


def load_api_key() -> str:
    """Load GEMINI_API_KEY from env var or .env file in project directory."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key

    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() == "GEMINI_API_KEY":
                        return v.strip()

    raise EnvironmentError("GEMINI_API_KEY not configured \u2014 check .env file")
