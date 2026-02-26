"""macOS notification support."""

import subprocess


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
