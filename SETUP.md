# Setup Guide

## 1. Install pngpaste

```bash
brew install pngpaste
```

## 2. Install Python dependencies

```bash
cd /path/to/clipdown
pip install -r requirements.txt
```

## 3. Configure API key

Copy the example env file and add your Gemini API key:

```bash
cp .env.example .env
```

Edit `.env` and replace `your_api_key_here` with your actual [Google AI Studio](https://aistudio.google.com/apikey) API key.

## 4. Create macOS Shortcut

1. Open **Shortcuts.app** (search "Shortcuts" in Spotlight)
2. Click **+** to create a new shortcut
3. Name it **"Clipboard to Markdown"**
4. Add a **"Run Shell Script"** action
5. Set the shell to `/bin/bash` and input to **No Input**
6. Enter the following script (adjust paths as needed):

```bash
/usr/bin/python3 /path/to/clipdown/clipboard_to_md.py
```

> **Tip:** To find your Python path, run `which python3` in Terminal. If you use a virtual environment, use that Python path instead.

## 5. Bind keyboard shortcut

1. Open **System Settings**
2. Go to **Keyboard** > **Keyboard Shortcuts...**
3. Select **Services** (or **App Shortcuts** depending on macOS version) in the left sidebar
4. Find **"Clipboard to Markdown"** under **General**
5. Double-click the shortcut column and press **Ctrl+Option+M**

You can now copy any image to your clipboard and press **Ctrl+Option+M** to convert it to markdown.
