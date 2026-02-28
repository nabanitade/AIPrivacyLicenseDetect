# 🧪 Testing Websites with AI Privacy License Detector

**Complete guide to testing any website for AI Privacy License detection using our comprehensive test suite.**

---

## 🚀 Quick Start

### **CLI Tool (Fastest & Most Powerful)**
```bash
# Test single website
ai-license https://example.com

# Test multiple websites with summary
ai-license --ndjson --summary https://site1.com https://site2.com

# Test from file
cat urls.txt | ai-license --ndjson --summary -
```

### **Test Suite Runner (Interactive Menu)**
```bash
# macOS/Linux
./run_website_tests.sh

# Windows
run_website_tests.bat
```

This opens an interactive menu where you can choose what to test!

---

## 📁 Test Files Overview

| File | Purpose | Platform |
|------|---------|----------|
| **`ai-license`** | **CLI tool (recommended)** | All |
| **`test_website.py`** | Test single website with all methods | All |
| **`test_multiple_websites.py`** | Batch test multiple websites | All |
| **`interactive_test.py`** | Interactive testing session | All |
| **`run_website_tests.sh`** | Test suite runner | macOS/Linux |
| **`run_website_tests.bat`** | Test suite runner | Windows |
| **`sample_urls.txt`** | Sample URLs for testing | All |

---

## 🖥️ CLI Tool (Recommended)

**The `ai-license` command is the fastest and most powerful way to test websites!**

### **Basic Usage**
```bash
# Test single website
ai-license https://example.com

# Test multiple websites
ai-license https://site1.com https://site2.com

# Check version
ai-license --version

# Get help
ai-license --help
```

### **Output Options**
```bash
# Pretty JSON (default)
ai-license https://example.com

# Compact JSON
ai-license --compact https://example.com

# NDJSON (one JSON per line)
ai-license --ndjson https://example.com

# With summary statistics
ai-license --summary https://example.com
```

### **Batch Processing**
```bash
# Multiple URLs
ai-license --ndjson --summary https://site1.com https://site2.com

# From file via stdin
cat urls.txt | ai-license --ndjson --summary -

# Echo URLs
echo "https://example.com" | ai-license -
```

### **Performance & Control**
```bash
# Concurrency (up to 50 parallel requests)
ai-license --concurrency 10 https://site1.com https://site2.com

# Custom timeout
ai-license --timeout 30 https://example.com

# Custom user agent
ai-license --user-agent "MyBot/1.0" https://example.com
```

### **Error Handling**
```bash
# Fail fast on errors
ai-license --fail-fast-error https://example.com

# Require licenses (exit code 2 if none found)
ai-license --require https://example.com

# Fail fast on missing licenses
ai-license --require --fail-fast-require https://example.com
```

### **CLI vs Python Scripts**
| Feature | CLI Tool | Python Scripts |
|---------|----------|----------------|
| **Ease of Use** | 🚀 One command | 🐍 Need to run Python |
| **Batch Processing** | ✅ Built-in | ✅ Custom scripts |
| **Output Formats** | ✅ Multiple options | ✅ Customizable |
| **Performance** | ✅ Concurrency | ✅ Single-threaded |
| **Integration** | ✅ Shell scripts | ✅ Python code |
| **Customization** | ✅ Command flags | ✅ Full Python control |

---

## 🔍 Individual Test Scripts

### **1. Single Website Test (`test_website.py`)**

**Purpose**: Test a single website with comprehensive analysis

**Usage**:
```bash
# Basic test
python3 test_website.py https://example.com

# Verbose test (includes CLI test)
python3 test_website.py --verbose https://example.com

# Test all individual detection methods
python3 test_website.py --all-methods https://example.com

# Full comprehensive test
python3 test_website.py --verbose --all-methods https://example.com
```

**What it tests**:
- ✅ Full website check
- 🔬 Individual detection methods (HTTP headers, robots.txt, HTML, license files)
- 🖥️ CLI equivalent test
- ⏱️ Performance timing
- 📊 Detailed results

**Example Output**:
```
🔍 Testing website: https://example.com
⏰ Started at: 2025-08-22 11:15:00
------------------------------------------------------------

✅ Detector initialized successfully

📋 Test 1: Full Website Check
------------------------------
✅ Website check completed in 0.85 seconds
   Has License: False
   License URL: None
   License Type: None
   Detection Methods: []
   Error: None
   Timestamp: 2025-08-22T11:15:01.165040+00:00
   No restrictions detected
```

### **2. Batch Website Test (`test_multiple_websites.py`)**

**Purpose**: Test multiple websites efficiently

**Usage**:
```bash
# Test URLs from file
python3 test_multiple_websites.py --from-file urls.txt

# Test specific URLs
python3 test_multiple_websites.py --urls https://site1.com https://site2.com

# Save results to JSON
python3 test_multiple_websites.py --from-file urls.txt --output results.json

# Summary only (no detailed results)
python3 test_multiple_websites.py --from-file urls.txt --summary-only
```

**What it provides**:
- 📊 Summary statistics
- 🔍 Detailed results for each site
- 💾 JSON export capability
- ⏱️ Performance metrics
- 🚫 Error handling

**Example Output**:
```
📊 Test Results Summary
==================================================
🌐 Total websites tested: 5
✅ Successful tests: 5
❌ Failed tests: 0
🛡️  Licenses found: 1
🚫 No licenses: 4
⏱️  Average test time: 0.92s
```

### **3. Interactive Test (`interactive_test.py`)**

**Purpose**: Interactive testing session for exploration

**Usage**:
```bash
python3 interactive_test.py
```

**Available Commands**:
- `test <url>` - Test a single website
- `methods <url>` - Test individual detection methods
- `cli <url>` - Test CLI equivalent
- `compare <url1> <url2>` - Compare two websites
- `help` - Show available commands
- `clear` - Clear the screen
- `quit` - Exit the program

**Example Session**:
```
🎮 > test https://example.com

🔍 Testing: https://example.com
----------------------------------------
✅ Completed in 0.85 seconds
🛡️  Has License: False
🔗 License URL: None
📋 License Type: None
🔍 Detection Methods: []
🚫 No restrictions detected

🎮 > methods https://example.com

🔬 Testing individual methods for: https://example.com
--------------------------------------------------
   Testing HTTP Headers...
      ✅ Completed in 0.12s
      Result: {'found': False}

   Testing robots.txt...
      ✅ Completed in 0.23s
      Result: {'found': False}
```

---

## 🎯 Test Suite Runner

### **macOS/Linux (`run_website_tests.sh`)**
```bash
chmod +x run_website_tests.sh
./run_website_tests.sh
```

### **Windows (`run_website_tests.bat`)**
```cmd
run_website_tests.bat
```

**Menu Options**:
1. **Single website test** - Test one website like we did manually
2. **Batch test multiple websites** - Test from URL file
3. **Interactive testing session** - Open interactive mode
4. **Run all tests** - Execute comprehensive test suite
5. **Exit** - Close the program

---

## 📝 Sample URLs File

**File**: `sample_urls.txt`

**Format**: One URL per line, comments start with `#`

**Content**:
```
# Test sites (no licenses expected)
https://keen-flan-b72fc1.netlify.app/
https://example.com
https://httpbin.org

# AI and tech sites (might have licenses)
https://openai.com
https://anthropic.com
https://perplexity.ai

# News and content sites
https://techcrunch.com
https://wired.com
https://arstechnica.com
```

**Create your own**:
```bash
# Create a custom URL file
echo "https://your-site.com" > my_urls.txt
echo "https://another-site.com" >> my_urls.txt

# Test with your file
python3 test_multiple_websites.py --from-file my_urls.txt
```

---

## 🧪 Testing Scenarios

### **Scenario 1: CLI Tool (Fastest)**
```bash
# Single website
ai-license https://example.com

# With summary
ai-license --summary https://example.com

# Verbose output
ai-license --verbose https://example.com
```

### **Scenario 2: Python Scripts (Detailed Analysis)**
```bash
python3 test_website.py https://example.com
```

### **Scenario 2: Comprehensive Analysis**
```bash
python3 test_website.py --verbose --all-methods https://example.com
```

### **Scenario 3: CLI Batch Testing (Recommended)**
```bash
# Multiple URLs
ai-license --ndjson --summary https://site1.com https://site2.com

# From file
cat sample_urls.txt | ai-license --ndjson --summary -

# High performance
ai-license --concurrency 8 --ndjson --summary $(cat sample_urls.txt | grep -v '^#')
```

### **Scenario 4: Python Scripts Batch Testing**
```bash
python3 test_multiple_websites.py --from-file sample_urls.txt --output results.json
```

### **Scenario 5: Interactive Exploration**
```bash
python3 interactive_test.py
```

### **Scenario 6: Full Test Suite**
```bash
./run_website_tests.sh  # macOS/Linux
run_website_tests.bat   # Windows
```

---

## 🔧 Customization

### **Modify Test Parameters**
Edit the test scripts to change:
- Timeout values
- User agent strings
- Detection method order
- Output formatting

### **Add New Detection Methods**
Extend the scripts to test:
- Custom HTTP headers
- Additional file paths
- New parsing logic

### **Integration with CI/CD**
Use the scripts in automated testing:
```yaml
# GitHub Actions example
- name: Test websites
  run: |
    # CLI tool (recommended for CI/CD)
    ai-license --ndjson --summary https://site1.com https://site2.com > results.json
    
    # Python scripts (for detailed analysis)
    python3 test_multiple_websites.py --from-file test_urls.txt --output results.json
    python3 test_website.py --verbose https://example.com
```

---

## 📊 Expected Results

### **Website with AI Privacy License**:
```
🛡️  Has License: True
🔗 License URL: https://example.com/ai-privacy-license
📋 License Type: AI-Privacy-License-1.0
🔍 Detection Methods: ['http_headers', 'robots_txt']
🎯 Allow Training: False
💼 Allow Commercial: True
📝 Attribution Required: True
```

### **Website without AI Privacy License**:
```
🛡️  Has License: False
🔗 License URL: None
📋 License Type: None
🔍 Detection Methods: []
🚫 No restrictions detected
```

### **Website with Errors**:
```
❌ Website check failed: Connection timeout
   Error: Connection timeout after 10 seconds
```

---

## 🚨 Troubleshooting

### **Common Issues**:

**Issue**: "Module not found"
```bash
# Solution: Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate.bat # Windows
```

**Issue**: "Permission denied" on scripts
```bash
# Solution: Make scripts executable
chmod +x run_website_tests.sh
chmod +x test_website.py
```

**Issue**: "URL validation failed"
```bash
# Solution: Ensure URLs start with http:// or https://
python3 test_website.py https://example.com  # ✅ Correct
python3 test_website.py example.com          # ❌ Wrong
```

### **Getting Help**:
1. **Check the interactive help**: Run `interactive_test.py` and type `help`
2. **Review error messages**: Most errors include helpful information
3. **Check file permissions**: Ensure scripts are executable
4. **Verify virtual environment**: Make sure dependencies are installed

---

## 🎉 Success Indicators

You'll know everything is working when:

✅ **All test scripts run** without errors  
✅ **Website detection works** for various sites  
✅ **Individual methods function** correctly  
✅ **CLI integration works** seamlessly  
✅ **Batch processing handles** multiple URLs  
✅ **Interactive mode responds** to commands  

---

## 🚀 Ready to Test?

**Start with the CLI tool (fastest)**:
```bash
# Single website
ai-license https://your-website.com

# Multiple websites
ai-license --ndjson --summary https://site1.com https://site2.com

# From file
cat sample_urls.txt | ai-license --ndjson --summary -
```

**Or use the test suite runner**:
```bash
# macOS/Linux
./run_website_tests.sh

# Windows
run_website_tests.bat
```

**Or use Python scripts for detailed analysis**:
```bash
python3 test_website.py --verbose --all-methods https://your-website.com
```

**Happy testing!** 🧪✨
