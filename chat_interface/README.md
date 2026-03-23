# AI Privacy License – Chat Interface

A simple chat-style web UI to test the AI Privacy License detector. Paste a URL and see whether the site has an AI Privacy License and what restrictions apply.

## Quick start

From the **project root** (the folder that contains `ai_privacy_license_detector` and `chat_interface`):

```bash
# 1. Use the project venv (recommended on macOS/Linux so Flask installs here, not system-wide)
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. Install the SDK and Flask
pip install -e .
pip install flask

# 3. Run the chat server
python3 chat_interface/server.py
# or
cd chat_interface && python3 server.py
```

Then open **http://127.0.0.1:5000** in your browser.

## Usage

- Type or paste a URL (e.g. `https://example.com`) and press **Check** or Enter.
- You can also type a sentence that contains a link; the app will detect the first URL.
- Ask questions about a URL; the chat will answer from the detected license (e.g. *Is AI training allowed?*, *Is commercial use allowed?*).

## Example messages to try

Use any of these in the chat (with or without `https://`; the app accepts bare hostnames like `example.com`).

### Just check a URL (full summary)
- `example.com`
- `https://example.com`
- `https://melodious-dango-e6155a.netlify.app/`
- `https://resonant-florentine-24200a.netlify.app/`

### Ask about commercial use
- `example.com is commercial use allowed?`
- `https://melodious-dango-e6155a.netlify.app/ is commercial use allowed?`

### Ask about AI training
- `example.com is AI training allowed?`
- `https://melodious-dango-e6155a.netlify.app/ can I train on this?`
- `melodious-dango-e6155a.netlify.app is training allowed?`

### Ask about attribution
- `example.com how should it be attributed?`
- `https://melodious-dango-e6155a.netlify.app/ attribution?`
- `example.com how to attribute?`

### Ask about do not train
- `example.com is do not train enabled?`
- `https://melodious-dango-e6155a.netlify.app/ do not train?`
- `example.com is don't train enabled?`

### Demo sites
- **With license** (training blocked, attribution required): `https://melodious-dango-e6155a.netlify.app/`
- **Without license**: `https://resonant-florentine-24200a.netlify.app/` or `https://example.com`

## Requirements

- Python 3.8+
- The AI Privacy License Detector SDK installed (`pip install -e .` from project root)
- Flask (`pip install flask`)
