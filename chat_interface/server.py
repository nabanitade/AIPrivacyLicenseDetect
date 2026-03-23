#!/usr/bin/env python3
"""
Chat interface server for testing AI Privacy License detection.
Run: pip install flask && python3 server.py
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


def detect_question_type(text):
    """Detect what the user is asking about. Returns: 'training', 'commercial', 'attribution', 'do_not_train', or None for full summary."""
    t = text.lower().strip()
    if re.search(r'\b(ai\s+)?training\s+allowed\b|can\s+(i|we)\s+train|is\s+(ai\s+)?training\s+allowed|allow(s)?\s+training', t):
        return "training"
    if re.search(r'\bcommercial\s+use\s+(allowed|permitted)?\b|is\s+commercial\s+(use\s+)?allowed|monetization', t):
        return "commercial"
    if re.search(r'\battribut(e|ion)\b|how\s+should\s+it\s+be\s+attributed|attribution\s+(text|required)|how\s+to\s+attribute', t):
        return "attribution"
    if re.search(r'\bdo\s*[- ]?not\s+train\b|don\'?t\s+train|do\s+not\s+train\s+enabled|training\s+blocked', t):
        return "do_not_train"
    return None


def build_answer(url, result_dict, question_type):
    """Build a natural-language answer from the detection result and optional question type."""
    has_license = result_dict.get("has_license") is True
    restrictions = result_dict.get("restrictions") or {}

    if not has_license:
        return (
            f"**{url}**\n\n"
            "No AI Privacy License was found on this site. "
            "There are no machine-readable restrictions, so training and commercial use are typically allowed by default (subject to normal law)."
        )

    # Has license – answer by question type
    if question_type == "training":
        allowed = restrictions.get("allow_training", True)
        return (
            f"**{url}**\n\n"
            f"**Is AI training allowed?** {'Yes.' if allowed else 'No. Training is blocked for this content.'}"
        )
    if question_type == "commercial":
        allowed = restrictions.get("allow_commercial", True)
        return (
            f"**{url}**\n\n"
            f"**Is commercial use allowed?** {'Yes.' if allowed else 'No. Commercial use is not permitted.'}"
        )
    if question_type == "attribution":
        req = restrictions.get("attribution_required", False)
        text = (restrictions.get("attribution_text") or "").strip() or None
        if not req:
            return f"**{url}**\n\n**Attribution:** Not required."
        msg = f"**{url}**\n\n**Attribution:** Required."
        if text:
            msg += f" Use this text: \"{text}\""
        else:
            msg += " No specific attribution text was set; including an unmodified copy of the license satisfies attribution."
        return msg
    if question_type == "do_not_train":
        allowed = restrictions.get("allow_training", True)
        flag = (restrictions.get("do_not_train") or "").strip() or None
        return (
            f"**{url}**\n\n"
            f"**Do not train:** {'Yes, enabled (training is blocked).' if not allowed else 'No.'}"
            + (f" Flag value: {flag}." if flag else "")
        )

    # Full summary
    parts = [f"**{url}**\n\n**Has AI Privacy License:** Yes."]
    parts.append(f"**AI training allowed:** {'Yes' if restrictions.get('allow_training', True) else 'No (do not train).'}")
    parts.append(f"**Commercial use allowed:** {'Yes' if restrictions.get('allow_commercial', True) else 'No'}.")
    attr = restrictions.get('attribution_required')
    attr_text = (restrictions.get('attribution_text') or 'see license') if attr else ''
    parts.append(f"**Attribution required:** {'Yes — ' + attr_text if attr else 'No'}.")
    if restrictions.get("data_owner"):
        parts.append(f"**Data owner:** {restrictions.get('data_owner')}.")
    return "\n".join(parts)


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
        question_type = detect_question_type(text)
        answer = build_answer(url, out, question_type)
        return jsonify({"ok": True, "url": url, "result": out, "answer": answer})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "url": url})


if __name__ == "__main__":
    print("AI Privacy License Chat – open http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
