# Step-by-step: Test the SDK with an example

Follow these steps in order. Use Terminal (macOS/Linux) or Command Prompt / PowerShell (Windows).

---

## Step 1: Open a terminal and go to the project folder

```bash
cd "/Users/nabanitade/Desktop/AI Privacy License"
```

(Or your actual path to the `AI Privacy License` folder.)

---

## Step 2: (Optional) Create and activate a virtual environment

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

You should see `(venv)` at the start of your prompt.

---

## Step 3: Install the project and its dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

Wait until both commands finish without errors.

---

## Step 4: Check that the CLI is available

```bash
ai-license --version
```

You should see something like: `ai-license 1.0.0`

If you get “command not found”, make sure the venv is activated (Step 2) and you ran `pip install -e .` (Step 3).

---

## Step 5: Test with a single URL (CLI)

**Example.com (usually no license):**
```bash
ai-license https://example.com
```

**Demo site that has an AI Privacy License:**
```bash
ai-license https://melodious-dango-e6155a.netlify.app/
```

You should get JSON with `has_license`, `restrictions`, etc.

---

## Step 6: Test with Python (optional)

Create a small script. In the same project folder, create a file named `my_test.py` with this content:

```python
from ai_privacy_license_detector import AIPrivacyLicenseDetector

detector = AIPrivacyLicenseDetector()
result = detector.check_website("https://melodious-dango-e6155a.netlify.app/")

print("URL:", result.url)
print("Has license:", result.has_license)
if result.has_license:
    print("License type:", result.license_type)
    print("Allow training:", result.restrictions.allow_training)
    print("Attribution required:", result.restrictions.attribution_required)
else:
    print("No AI Privacy License found.")
```

Save the file, then run:

```bash
python my_test.py
```

(or `python3 my_test.py` if that’s what you use.)

You should see printed lines with the detection result.

---

## Step 7: Run the unit tests (optional)

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

All tests should pass. This confirms the SDK is working correctly.

---

## Troubleshooting

| Problem | What to do |
|--------|------------|
| `ai-license: command not found` | Activate the venv (Step 2) and run `pip install -e .` again (Step 3). |
| `ModuleNotFoundError: ai_privacy_license_detector` | Run `pip install -e .` from the project root (Step 3). |
| Timeout or network error | Check your internet; the demo URLs need to be reachable. |
| Wrong Python version | Use Python 3.8 or newer: `python3 --version` or `python --version`. |

---

## Next steps

- Try more URLs: `ai-license --summary https://site1.com https://site2.com`
- Batch from a file: `cat sample_urls.txt | ai-license - --ndjson --summary -`
- Full docs: [README.md](README.md), [GETTING_STARTED.md](GETTING_STARTED.md), [README_TESTING.md](README_TESTING.md)
