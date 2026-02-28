#!/usr/bin/env python3
"""
Chat interface server for testing AI Privacy License detection.
Run: pip install flask && python server.py
Then open http://127.0.0.1:5000
"""
import json
import re
from flask import Flask, request, jsonify, send_from_directory
import sys
import os

# Add project root so we can import the detector (works when run from chat_interface/ or project root)
_script_dir = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(_script_dir)
sys.path.insert(0, _root)
os.chdir(_script_dir)  # so static files (index.html) are found
from ai_privacy_license_detector import AIPrivacyLicenseDetector

app = Flask(__name__, static_folder=".", static_url_path="")
detector = None


def get_detector():
    global detector
    if detector is None:
        detector = AIPrivacyLicenseDetector(timeout=15)
    return detector


def extract_url(text):
    """Extract first URL from user message. Accepts full URLs or bare hostnames (e.g. example.com)."""
    text = text.strip()
    # Full URL with scheme
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    match = re.search(url_pattern, text)
    if match:
        return match.group(0).strip()
    # Bare hostname (e.g. example.com or sub.example.com/path)
    hostname_pattern = r'[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)+(?:/[^\s]*)?'
    match = re.search(hostname_pattern, text)
    if match:
        host_part = match.group(0).strip()
        if "/" in host_part or host_part.count(".") >= 1:
            return "https://" + host_part
    return None


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/api/check", methods=["POST"])
def check_url():
    data = request.get_json() or {}
    text = (data.get("message") or data.get("url") or "").strip()
    if not text:
        return jsonify({"ok": False, "error": "Please provide a URL or message containing a URL."})

    url = extract_url(text) if not text.startswith("http") else text
    if not url:
        return jsonify({"ok": False, "error": "No URL found in your message. Try pasting a link like https://example.com"})

    try:
        det = get_detector()
        result = det.check_website(url)
        out = result.as_dict()
        return jsonify({"ok": True, "url": url, "result": out})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "url": url})


if __name__ == "__main__":
    print("AI Privacy License Chat – open http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
