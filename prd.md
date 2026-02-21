# PRD: Clipboard-to-Markdown Converter (macOS)

## Overview

A lightweight Python script that converts screenshot/image content on the macOS clipboard into clean markdown text using Google's Gemini 2.5 Flash API, then writes the resulting markdown back to the clipboard. Designed to be triggered via a macOS Shortcut bound to `Ctrl+Shift+M`.

## Problem

Converting screenshots and PDFs to markdown for LLM input currently requires manually uploading images to a chat interface, prompting for conversion, and copying the result. This is tedious when done repeatedly. The user wants a single keyboard shortcut that handles the entire pipeline invisibly.

## User Flow

1. User takes a screenshot (or copies an image/PDF to clipboard)
2. User presses `Ctrl+Shift+M`
3. macOS Shortcut triggers the Python script
4. Script grabs the clipboard image, sends it to Gemini 3 Flash (no reasoning), and writes the returned markdown to the clipboard (the markdown should be optimized for LLM input.
5. User pastes clean markdown wherever they need it (`Cmd+V`)

The entire process should feel near-instant (1-3 seconds depending on API latency). The user should receive a macOS notification indicating success or failure.

## Technical Architecture

### Script: `clipboard_to_md.py`

**Location:** `~/scripts/clipboard-to-md/clipboard_to_md.py`

**Dependencies (requirements.txt):**
- `google-genai` — Google's Gemini Python SDK
- `Pillow` — for clipboard image handling as a fallback

**System dependencies (Homebrew):**
- `pngpaste` — reliable clipboard-to-image extraction on macOS (`brew install pngpaste`)

**No other third-party dependencies.** Use built-in macOS tools wherever possible:
- `pngpaste` to extract clipboard image to a temp file
- `pbcopy` (built-in) to write markdown back to clipboard
- `osascript` (built-in) to send macOS notifications
- `subprocess` and `tempfile` from Python's standard library

### Core Logic (step by step)

1. **Extract clipboard image:**
   - Use `pngpaste` via `subprocess.run()` to save clipboard contents to a temp `.png` file
   - If `pngpaste` exits with a non-zero code (no image on clipboard), send an error notification and exit gracefully

2. **Send image to Gemini 2.5 Flash:**
   - Read the temp image file as bytes
   - Use the `google-genai` SDK to call `gemini-2.0-flash` (NOT gemini-1.5 — use the latest 2.0 flash model)
   - Use the following system prompt:

   ```
   Convert this image to clean, well-structured markdown. 
   Rules:
   - Output ONLY the markdown content, no commentary or explanation
   - No wrapping code fences (do not wrap output in ```markdown``` blocks)
   - Preserve the logical structure: headings, lists, tables, code blocks
   - For code snippets in the image, use appropriate fenced code blocks with language tags
   - For tables, use standard markdown table syntax
   - Be precise with the text content — do not paraphrase or summarize
   ```

3. **Write markdown to clipboard:**
   - Pipe the Gemini response text into `pbcopy` via `subprocess.run()`
   
4. **Send macOS notification:**
   - On success: notification with title "Clipboard → MD" and message "Markdown copied to clipboard ✓"
   - On failure: notification with title "Clipboard → MD" and a descriptive error message (e.g., "No image found on clipboard", "API error: [details]")

5. **Cleanup:**
   - Delete the temp image file

### API Key Management

- Read the Gemini API key from an environment variable: `GEMINI_API_KEY`
- If the env var is not set, check for a `.env` file in the script's directory and load it using standard file reading (no `python-dotenv` dependency — just read and parse the file manually to keep deps minimal)
- If no key is found in either location, send an error notification and exit

### macOS Shortcut Setup

Create a macOS Shortcut named **"Clipboard to Markdown"** with a single action:

- **"Run Shell Script"** action with:
  ```bash
  /path/to/python3 ~/scripts/clipboard-to-md/clipboard_to_md.py
  ```
  
The user will then manually bind this shortcut to `Ctrl+Shift+M` via:  
System Settings → Keyboard → Keyboard Shortcuts → Services

Include a `SETUP.md` file in the project directory with clear step-by-step instructions for:
1. Installing `pngpaste` via Homebrew
2. Installing Python dependencies via `pip install -r requirements.txt`
3. Setting up the `GEMINI_API_KEY` (via `.env` file in the project directory)
4. Creating the macOS Shortcut
5. Binding the shortcut to `Ctrl+Shift+M`

Include screenshots descriptions or exact menu paths so the setup is unambiguous.

## File Structure

```
~/scripts/clipboard-to-md/
├── clipboard_to_md.py      # Main script
├── requirements.txt         # Python dependencies
├── .env.example             # Template for API key
├── SETUP.md                 # Setup instructions
└── README.md                # Project overview
```

## Error Handling

Every failure mode should result in a macOS notification (never fail silently):

| Scenario | Notification Message |
|---|---|
| No image on clipboard | "No image found on clipboard" |
| `pngpaste` not installed | "pngpaste not found — run: brew install pngpaste" |
| `GEMINI_API_KEY` not set | "GEMINI_API_KEY not configured — check .env file" |
| Gemini API error | "API error: {error_message}" |
| Network error | "Network error — check your connection" |

## Constraints

- **Python 3.10+** (assume the user has this already)
- **Minimal dependencies** — prefer built-in macOS tools and Python stdlib over third-party packages
- **No daemon / background process** — the script runs on-demand, does its job, and exits
- **No GUI** — all feedback via macOS notifications
- **Idempotent** — safe to trigger multiple times; always cleans up temp files even on failure (use `try/finally`)

## Out of Scope (for now)

- PDF clipboard handling (macOS clipboard doesn't natively hold PDFs from screenshots — this is an image-first tool)
- Configurable prompts or model selection
- Caching or history of past conversions
- Menu bar app / tray icon