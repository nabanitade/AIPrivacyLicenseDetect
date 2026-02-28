# AI Privacy License – Chat Interface

A simple chat-style web UI to test the AI Privacy License detector. Paste a URL and see whether the site has an AI Privacy License and what restrictions apply.

## Quick start

From the **project root** (the folder that contains `ai_privacy_license_detector` and `chat_interface`):

```bash
# 1. Install the SDK and Flask
pip install -e .
pip install flask

# 2. Run the chat server (either way works)
python chat_interface/server.py
# or
cd chat_interface && python server.py
```

Then open **http://127.0.0.1:5000** in your browser.

## Usage

- Type or paste a URL (e.g. `https://example.com`) and press **Check** or Enter.
- You can also type a sentence that contains a link; the app will detect the first URL.
- Try the demo site with a license: `https://melodious-dango-e6155a.netlify.app/`
- Try a site without: `https://resonant-florentine-24200a.netlify.app/`

## Requirements

- Python 3.8+
- The AI Privacy License Detector SDK installed (`pip install -e .` from project root)
- Flask (`pip install flask`)
