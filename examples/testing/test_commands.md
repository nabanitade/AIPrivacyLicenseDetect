# 🧪 Testing AI Privacy License Detection Library

## 🚀 Quick Test Commands

### **1. Test License File Detection**
```bash
# Check if the library can find and parse your license file
python3 -c "
from ai_privacy_license_detector import AIPrivacyLicenseDetector
detector = AIPrivacyLicenseDetector(verbose=True)
result = detector.check_website('.')
print('Has License:', result.has_license)
print('License Type:', result.license_type)
print('Detection Methods:', result.detection_methods)
if result.restrictions:
    print('Do Not Train:', result.restrictions.do_not_train)
    print('Allow Training:', result.restrictions.allow_training)
    print('Commercial Use:', result.restrictions.allow_commercial)
    print('Attribution Required:', result.restrictions.attribution_required)
"
```

### **2. Test CLI Tool**
```bash
# Test the command-line interface
python3 -m ai_privacy_license_detector.cli --verbose --summary .

# Test with JSON output
python3 -m ai_privacy_license_detector.cli --verbose --ndjson .

# Test with compact output
python3 -m ai_privacy_license_detector.cli --verbose --compact .
```

### **3. Test Convenience Function**
```bash
# Test the simple check_url function
python3 -c "
from ai_privacy_license_detector import check_url
result = check_url('.', verbose=True)
print('Result:', result.as_dict())
"
```

### **4. Test License Parsing**
```bash
# Test just the license content parsing
python3 -c "
from ai_privacy_license_detector import AIPrivacyLicenseDetector
detector = AIPrivacyLicenseDetector()
with open('AiPrivacyLicense-1.0.txt', 'r') as f:
    content = f.read()
restrictions = detector._parse_license_content(content)
print('Do Not Train:', restrictions.do_not_train)
print('Allow Training:', restrictions.allow_training)
print('Commercial Use:', restrictions.allow_commercial)
print('Attribution Required:', restrictions.attribution_required)
print('Attribution Text:', restrictions.attribution_text)
print('Data Owner:', restrictions.data_owner)
"
```

### **5. Run Full Test Suite**
```bash
# Run the comprehensive test script
python3 test_local_detection.py
```

## 🎯 Expected Results

When you run these tests, you should see:

✅ **License Detection**: The library finds your `AiPrivacyLicense-1.0.txt` file  
✅ **robots.txt Parsing**: Detects the `ai-privacy-license-link:` declaration  
✅ **HTML Parsing**: Finds meta tags, link tags, and JSON-LD  
✅ **License Parsing**: Correctly parses all fields:
- `do_not_train`: "strict"
- `allow_training`: False (because "strict" means no training)
- `allow_commercial`: True (because "yes")
- `attribution_required`: True (because "Yes")
- `attribution_text`: "This data is provided by Test Data Owner for testing purposes"
- `data_owner`: "Test Data Owner"

## 🔍 What Each Test Does

### **License File Detection**
- Tests if the library can find your `AiPrivacyLicense-1.0.txt` file
- Verifies the file is readable and parseable

### **robots.txt Detection**
- Tests if the library reads your `robots.txt` file
- Checks if it finds the `ai-privacy-license-link:` declaration
- Verifies it can fetch and parse the license file

### **HTML Detection**
- Tests meta tag detection: `<meta name="ai-privacy-license-link">`
- Tests link tag detection: `<link rel="license">`
- Tests JSON-LD detection: structured data in `<script>` tags

### **License Parsing**
- Tests the core parsing logic
- Verifies all fields are extracted correctly
- Ensures boolean values are interpreted properly

### **CLI Testing**
- Tests the command-line interface
- Verifies all CLI options work
- Tests output formatting (JSON, NDJSON, compact)

## 🚨 Troubleshooting

If tests fail:

1. **Install the library**: `pip install -e .`
2. **Check file paths**: Make sure all test files exist
3. **Check permissions**: Ensure files are readable
4. **Check dependencies**: Make sure `requests` and `beautifulsoup4` are installed

## 🎉 Success Indicators

You'll know it's working when you see:
- ✅ All detection methods succeed
- ✅ License content is parsed correctly
- ✅ CLI commands work without errors
- ✅ All expected fields have correct values
