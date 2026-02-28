# 🧪 Quick Testing Reference

**Fast reference for using the SDK and testing websites with AI Privacy License Detector**

---

## How to use the SDK

### Install

```bash
# From PyPI (use in your own project)
pip install ai-privacy-license-detector

# Or from this repo (development)
cd /path/to/AI\ Privacy\ License
pip install -r requirements.txt && pip install -e .
```

### Python API

**One-off check (single URL):**
```python
from ai_privacy_license_detector import check_url

result = check_url("https://example.com")
print(result.has_license)
if result.restrictions:
    print("Allow training:", result.restrictions.allow_training)
```

**Detector instance (reuse, more options):**
```python
from ai_privacy_license_detector import AIPrivacyLicenseDetector

detector = AIPrivacyLicenseDetector(timeout=30)
result = detector.check_website("https://example.com")

if result.has_license:
    print(result.license_type, result.license_url)
    if result.restrictions and not result.restrictions.allow_training:
        print("Training blocked — exclude from dataset")
```

**Context manager (recommended for production):**
```python
with AIPrivacyLicenseDetector(timeout=30) as detector:
    result = detector.check_website("https://example.com")
    data = result.as_dict()  # JSON-serializable
```

**Batch (multiple URLs):**
```python
detector = AIPrivacyLicenseDetector()
results = detector.check_batch_urls(["https://a.com", "https://b.com"])
for r in results:
    if r.has_license and not (r.restrictions and r.restrictions.allow_training):
        print(r.url, "— do not train")
```

### CLI

```bash
# Single URL
ai-license https://example.com

# Multiple URLs, summary
ai-license --summary https://site1.com https://site2.com

# From file, NDJSON for pipelines
cat urls.txt | ai-license - --ndjson --summary -
```

---

## How to test

### 1. Prerequisites & setup

From the project root (where `setup.py` and `ai_privacy_license_detector/` are):

```bash
# One-time setup (macOS/Linux)
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

### 2. Quick verification (30 seconds)

```bash
# Check the CLI works
ai-license https://example.com

# Run the quick test script (imports + CLI help + library structure)
./test.sh
# Then choose option 1 (Quick test)
```

### 3. Test a single website

```bash
ai-license https://example.com
ai-license --summary --verbose https://example.com
```

### 4. Test known demo sites

```bash
# Site WITH AI Privacy License (training blocked)
ai-license https://melodious-dango-e6155a.netlify.app/

# Site WITHOUT license
ai-license https://resonant-florentine-24200a.netlify.app/
```

### 5. Run unit tests (pytest)

```bash
pip install -e ".[dev]"   # if not already
pytest tests/ -v
```

### 6. Batch or interactive testing

- **Batch from file**: `cat sample_urls.txt | ai-license - --ndjson --summary -`
- **Interactive menu**: `./run_website_tests.sh` (macOS/Linux) or `run_website_tests.bat` (Windows)
- **Interactive Python**: `python3 interactive_test.py`

For more detail, see the sections below and [TESTING_WEBSITES.md](TESTING_WEBSITES.md).

---

## 🚀 One-Command Testing

```bash
# CLI Tool (Fastest & Most Powerful)
ai-license https://example.com

# Test Suite Runner
./run_website_tests.sh  # macOS/Linux
run_website_tests.bat   # Windows
```

---

## 📁 Test Files Quick Reference

| Command | Purpose | Example |
|---------|---------|---------|
| **`ai-license <url>`** | **CLI tool (recommended)** | `ai-license https://example.com` |
| `pytest tests/ -v` | Unit tests (parse, headers, sanitize, JSON-LD) | `pytest tests/ -v` |
| `python3 test_website.py <url>` | Test single website | `python3 test_website.py https://example.com` |
| `python3 test_multiple_websites.py --from-file <file>` | Batch test from file | `python3 test_multiple_websites.py --from-file urls.txt` |
| `python3 interactive_test.py` | Interactive testing | `python3 interactive_test.py` |
| `./run_website_tests.sh` | Test suite menu | `./run_website_tests.sh` |
| `./test.sh` | Quick test (imports + CLI + structure) | `./test.sh` |

---

## 🎯 Common Testing Scenarios

### **CLI Tool (Fastest)**
```bash
# Single website
ai-license https://example.com

# With summary
ai-license --summary https://example.com

# Verbose output
ai-license --verbose https://example.com
```

### **Python Scripts (Detailed Analysis)**
```bash
python3 test_website.py https://example.com
```

### **Comprehensive Analysis**
```bash
python3 test_website.py --verbose --all-methods https://example.com
```

### **CLI Batch Testing (Recommended)**
```bash
# Multiple URLs
ai-license --ndjson --summary https://site1.com https://site2.com

# From file
cat sample_urls.txt | ai-license --ndjson --summary -

# High performance
ai-license --concurrency 8 --ndjson --summary $(cat sample_urls.txt | grep -v '^#')
```

### **Python Scripts Batch Testing**
```bash
python3 test_multiple_websites.py --from-file sample_urls.txt
```

### **Interactive Mode**
```bash
python3 interactive_test.py
# Then type: test https://example.com
```

---

## 📝 Sample URLs File

**File**: `sample_urls.txt`
**Usage**: `python3 test_multiple_websites.py --from-file sample_urls.txt`

---

## 🔧 Troubleshooting

- **Run from project root**: Commands and scripts expect to be run from the repo root (where `setup.py` and `ai_privacy_license_detector/` are).
- **Activate virtual environment**: `source venv/bin/activate` (Windows: `venv\Scripts\activate`).
- **Make scripts executable**: `chmod +x test.sh run_website_tests.sh examples/testing/*.sh`
- **Check help**: `ai-license --help` or `python3 test_website.py --help`
- **Library not found**: Run `pip install -e .` from the project root.

---

### **📊 CLI vs Python Scripts Comparison**

| Feature | CLI Tool | Python Scripts |
|---------|----------|----------------|
| **Ease of Use** | 🚀 One command | 🐍 Need to run Python |
| **Batch Processing** | ✅ Built-in | ✅ Custom scripts |
| **Performance** | ✅ Concurrency (up to 50) | ✅ Single-threaded |
| **Learning Curve** | 🎯 Simple commands | 📚 Python knowledge needed |
| **CI/CD** | 🚀 Perfect for automation | 🔧 Good for complex logic |

**📚 Full Documentation**: [TESTING_WEBSITES.md](TESTING_WEBSITES.md)
