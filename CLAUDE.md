# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Clipdown is a macOS utility that converts clipboard images to markdown using OpenRouter. Triggered via keyboard shortcut (Ctrl+Shift+M) through macOS Shortcuts app, it extracts the clipboard image, sends it to OpenRouter, and writes the resulting markdown back to the clipboard.

## Running

```bash
python3 clipboard_to_md.py
```

No build step. No test suite. No linter configured. Single-file Python application requiring Python 3.10+.

## Dependencies

- `requests` and `Pillow` (see `requirements.txt`)
- `pngpaste` (Homebrew) for clipboard image extraction
- macOS built-ins: `pbcopy`, `osascript`, `tempfile`

## Architecture

Everything lives in `clipdown/`. The pipeline is:

1. `load_config()` — reads `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` from env vars or `.env` file (manual parsing, no dotenv library)
2. `extract_clipboard_image()` — calls `pngpaste` to save clipboard image to a temp PNG
3. `convert_image_to_markdown()` — base64-encodes the image and sends to OpenRouter's `/api/v1/chat/completions` endpoint with a system prompt
4. `write_to_clipboard()` — pipes markdown to `pbcopy`
5. `notify()` — sends macOS notifications via `osascript`
6. `cleanup_temp_file()` — removes temp files in `finally` block

All errors surface as macOS notifications before exiting. The system prompt instructs the model to output only raw markdown (no code fences, no commentary).

## Key Files

- `clipboard_to_md.py` — entry point (delegates to `clipdown.__main__`)
- `clipdown/openrouter.py` — OpenRouter API interaction
- `clipdown/config.py` — configuration, env var loading, system prompt
- `clipdown/clipboard.py` — clipboard image extraction & writing
- `clipdown/notify.py` — macOS notification support
- `.env` — `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` (not tracked in git)
- `prd.md` — product requirements document
- `SETUP.md` — installation and macOS Shortcut configuration
