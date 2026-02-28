# 🚀 Getting Started with AI Privacy License Detector

**Complete setup guide for developers, DevOps engineers, and users getting started with the AI Privacy License Detector library.**

---

## 🔗 Connect & Learn More

**🌐 [Visit AI Privacy License Website](https://www.aiprivacylicense.com)**

**📱 Follow Us:**
- 🐦 [Follow on X (Twitter)](https://twitter.com/aiprivacylicense)
- 💼 [Follow on LinkedIn](https://linkedin.com/company/ai-privacy-license)
- 👥 [Join our Community](https://discord.gg/aiprivacylicense)

**⭐ GitHub:**
- ⭐ [Star this Repository](https://github.com/nabanitade/aiprivacylicenseSDK)
- 🍴 [Fork on GitHub](https://github.com/nabanitade/aiprivacylicenseSDK/fork)
- 📝 [Report Issues](https://github.com/nabanitade/aiprivacylicenseSDK/issues)
- 🔄 [Pull Requests](https://github.com/nabanitade/aiprivacylicenseSDK/pulls)

**💪 Support the Project:**
- 🌟 **Star this repo** if it helps you!
- 🚀 **Share with your team** - spread AI privacy awareness
- 💡 **Contribute ideas** - help shape the future of AI ethics
- 🔗 **Link to us** - reference in your AI projects

---

---

## 🚀 Quick Setup (One Command)

```bash
# macOS/Linux
./setup.sh

# Windows
setup.bat

# Or use requirements.txt directly
pip install -r requirements.txt && pip install -e .
```

**What this does:**
- ✅ Checks Python version (3.8+)
- ✅ Creates virtual environment
- ✅ Installs all dependencies
- ✅ Installs the library
- ✅ Runs tests to verify setup
- ✅ Makes test scripts executable

---

## 🛠️ Setup & Installation

### **System Requirements**

- **Python**: 3.8 or higher (3.8, 3.9, 3.10, 3.11, 3.12, 3.13)
- **Operating System**: Linux, macOS, Windows
- **Memory**: 50MB minimum, 100MB recommended
- **Network**: Internet access for fetching licenses

### **Dependencies**

| Package | Version | Purpose |
|---------|---------|---------|
| `requests` | ≥2.25.0 | HTTP client for fetching licenses |
| `beautifulsoup4` | ≥4.9.0 | HTML parsing for meta tags and JSON-LD |
| `urllib3` | ≥1.26.0 | HTTP connection pooling and retries |

---

## 🔧 Setup Options

### **1. Setup Python Environment**

#### **Option A: Automated Setup (Recommended)**
```bash
# macOS/Linux
./setup.sh

# Windows
setup.bat
```

#### **Option B: Manual Setup with Virtual Environment**
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install requests beautifulsoup4 urllib3

# Install the library in development mode
pip install -e .
```

#### **Option C: Using pip directly**
```bash
# Install dependencies globally
pip3 install requests beautifulsoup4 urllib3

# Install the library
pip3 install -e .
```

#### **Option D: Using conda**
```bash
# Create conda environment
conda create -n ai-privacy-license python=3.8
conda activate ai-privacy-license

# Install dependencies
conda install requests beautifulsoup4 urllib3

# Install the library
pip install -e .
```

### **2. Verify Installation**
```bash
# Test import
python3 -c "import ai_privacy_license_detector; print('✅ Library installed successfully!')"

# Test CLI
python3 -m ai_privacy_license_detector.cli --version
```

### **3. Production Installation**
```bash
pip install ai-privacy-license-detector
```

---

## 🧪 Testing Your Installation

After setup, verify everything works:

```bash
# Quick test (30 seconds)
cd examples/testing
./quick_test.sh

# Comprehensive test suite (2-3 minutes)
./run_tests.sh

# Interactive test runner
cd ../..
./test.sh
```

**Expected Results:**
- ✅ Library import successful
- ✅ Detector creation successful
- ✅ License parsing working
- ✅ CLI tool functional
- ✅ All tests passing

---

## 🐳 Docker Setup

```dockerfile
# Dockerfile example
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the library
RUN pip install -e .

# Run tests
RUN cd examples/testing && ./quick_test.sh

# Default command
CMD ["python", "-m", "ai_privacy_license_detector.cli", "--help"]
```

```yaml
# docker-compose.yml example
version: '3.8'
services:
  ai-privacy-license-detector:
    build: .
    environment:
      - PYTHONPATH=/app
    volumes:
      - ./data:/app/data
    command: ["python", "-m", "ai_privacy_license_detector.cli", "--help"]
```

---

## 🔄 CI/CD Integration

```yaml
# GitHub Actions example
name: Test AI Privacy License Detector
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: |
          python -m pip install --upgrade pip
          pip install requests beautifulsoup4 urllib3
          pip install -e .
      - run: |
          cd examples/testing
          ./quick_test.sh
```

---

## ⚙️ Environment Variables & Configuration

```bash
# Set custom timeout (default: 10 seconds)
export AI_PRIVACY_LICENSE_TIMEOUT=30

# Enable verbose logging
export AI_PRIVACY_LICENSE_VERBOSE=true

# Custom user agent
export AI_PRIVACY_LICENSE_USER_AGENT="MyApp/1.0 (AI Privacy License Compliant)"

# Disable SSL verification (development only)
export AI_PRIVACY_LICENSE_INSECURE_SSL=true
```

---

## 🚀 Production Deployment

```bash
# Install production version
pip install ai-privacy-license-detector

# Or pin specific version
pip install ai-privacy-license-detector==1.0.0

# Verify installation
python -c "import ai_privacy_license_detector; print('Production ready!')"
```

---

## 🛠️ Development Setup

```bash
# Clone the repository
git clone https://github.com/your-username/ai-privacy-license-detector.git
cd ai-privacy-license-detector

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e .[dev]

# Run tests
cd examples/testing
./quick_test.sh
```

---

## 🚨 Troubleshooting

### **Common Issues**

#### **Issue: "Module not found"**
```bash
# Solution: Install dependencies
pip install requests beautifulsoup4 urllib3
```

#### **Issue: "Permission denied"**
```bash
# Solution: Use virtual environment or --user flag
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

#### **Issue: "SSL certificate verify failed"**
```bash
# Solution: Use insecure_ssl flag (development only)
detector = AIPrivacyLicenseDetector(insecure_ssl=True)
```

#### **Issue: "Connection timeout"**
```bash
# Solution: Increase timeout
detector = AIPrivacyLicenseDetector(timeout=30)
```

### **Platform-Specific Notes**

#### **macOS (Homebrew)**
```bash
# Install Python if needed
brew install python@3.11

# Create virtual environment
python3.11 -m venv venv
```

#### **Windows (PowerShell)**
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\Activate.ps1

# Install dependencies
pip install requests beautifulsoup4 urllib3
```

#### **Linux (Ubuntu/Debian)**
```bash
# Install system dependencies
sudo apt update
sudo apt install python3-venv python3-pip

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
```

---

## 📊 Setup Summary

| Environment | Command | Notes |
|-------------|---------|-------|
| **Development** | `pip install -e .` | Editable install for code changes |
| **Production** | `pip install ai-privacy-license-detector` | Stable release version |
| **Testing** | `./examples/testing/quick_test.sh` | Verify installation works |
| **Docker** | `docker build -t ai-privacy-license .` | Containerized deployment |
| **CI/CD** | Use GitHub Actions example above | Automated testing |

---

## 🎯 Next Steps After Setup

1. ✅ **Verify Installation**: Run `./examples/testing/quick_test.sh`
2. 🧪 **Run Tests**: Execute `./examples/testing/run_tests.sh`
3. 📚 **Read Examples**: Check `examples/example_check.py`
4. 🚀 **Start Using**: Begin with the 2-line integration example
5. 🔧 **Customize**: Adjust timeouts, user agents, and SSL settings

---

## 📚 Related Documentation

- **Main README**: `README.md` - Project overview and features
- **Examples**: `examples/README.md` - Usage examples and testing
- **Testing**: `examples/testing/README.md` - Comprehensive testing guide
- **Publishing**: `PUBLISHING.md` - PyPI build and upload (for maintainers)
- **API Reference**: `ai_privacy_license_detector/detector.py` - Core library code
- **CLI Reference**: `ai_privacy_license_detector/cli.py` - Command-line interface

---

**🚀 Ready to get started? Run `./setup.sh` (macOS/Linux) or `setup.bat` (Windows) to begin!**
