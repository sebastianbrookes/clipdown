"""Configuration and API key management."""

import os

NOTIFICATION_TITLE = "Clipboard \u2192 MD"

DEFAULT_MODEL = "google/gemini-2.5-flash"

SYSTEM_PROMPT = """\
Convert this image to clean, well-structured markdown.
Rules:
- Output ONLY the markdown content, no commentary or explanation
- No wrapping code fences (do not wrap output in ```markdown``` blocks)
- Preserve the logical structure: headings, lists, tables, code blocks
- For code snippets in the image, use appropriate fenced code blocks with language tags
- For tables, use standard markdown table syntax
- Be precise with the text content \u2014 do not paraphrase or summarize"""


def load_config() -> tuple[str, str]:
    """Load OpenRouter API key and model from env vars or .env file.

    Returns (api_key, model) tuple.
    """
    api_key = os.environ.get("OPENROUTER_API_KEY")
    model = os.environ.get("OPENROUTER_MODEL")

    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip()
                    if k == "OPENROUTER_API_KEY" and not api_key:
                        api_key = v
                    elif k == "OPENROUTER_MODEL" and not model:
                        model = v

    if not api_key:
        raise EnvironmentError("OPENROUTER_API_KEY not configured \u2014 check .env file")

    return api_key, model or DEFAULT_MODEL
