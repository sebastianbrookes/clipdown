"""Entry point for `python -m clipdown`."""

import sys

from .clipboard import cleanup_temp_file, extract_clipboard_image, write_to_clipboard
from .config import NOTIFICATION_TITLE, load_api_key
from .gemini import convert_image_to_markdown
from .notify import notify


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
