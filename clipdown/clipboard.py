"""Clipboard image extraction and writing (macOS)."""

import os
import subprocess
import tempfile


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


def write_to_clipboard(text: str) -> None:
    """Write text to the macOS clipboard via pbcopy."""
    subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)


def cleanup_temp_file(path: str) -> None:
    """Silently remove a temp file."""
    try:
        os.unlink(path)
    except OSError:
        pass
