# Clipdown

A macOS utility that converts clipboard images to markdown using Google Gemini 2.5 Flash.

Copy a screenshot, press **Ctrl+Option+M**, and paste clean markdown.

## How it works

1. Extracts the image from your clipboard via `pngpaste`
2. Sends it to Gemini 2.5 Flash for conversion
3. Writes the resulting markdown back to your clipboard
4. Shows a macOS notification confirming success or describing any error

## Quick start

```bash
brew install pngpaste
pip install -r requirements.txt
cp .env.example .env   # add your Gemini API key
python3 clipboard_to_md.py
```

See [SETUP.md](SETUP.md) for full setup instructions including the keyboard shortcut.
