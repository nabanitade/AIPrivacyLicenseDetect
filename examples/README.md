# 🎯 Examples Directory

This directory contains practical examples and testing tools for the AI Privacy License Detection Library.

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

## 📁 Directory Structure

```
examples/
├── README.md                    # This file
├── example_check.py            # Basic usage examples
└── testing/                    # Complete testing suite
    ├── README.md               # Testing guide
    ├── run_tests.sh            # Comprehensive test runner
    ├── quick_test.sh           # Quick test script
    ├── test_local_detection.py # Python test script
    ├── test_commands.md        # Manual test commands
    ├── AiPrivacyLicense-1.0.txt # Sample license file
    ├── robots.txt              # Sample robots.txt
    └── test_page.html          # Sample HTML page
```

## 🚀 Quick Start

**📚 [Complete Setup Guide → ../GETTING_STARTED.md](../GETTING_STARTED.md)**

### **Basic Examples**
```bash
# Run basic usage examples
python3 examples/example_check.py
```

### **Testing Your Library**
```bash
# Quick test (30 seconds)
cd examples/testing
./quick_test.sh

# Comprehensive test suite (2-3 minutes)
./run_tests.sh
```

## 📋 What's Included

### **1. Basic Usage Examples (`example_check.py`)**
- Simple 2-line integration
- Batch processing examples
- Custom configuration examples
- Production usage patterns

### **2. Complete Testing Suite (`testing/`)**
- **Test Files**: Sample license, robots.txt, HTML page
- **Test Scripts**: Automated testing with bash and Python
- **Test Commands**: Manual testing instructions
- **Documentation**: Comprehensive testing guide

## 🧪 Testing Your Installation

The testing suite verifies:

✅ **Environment Setup** - Python, dependencies, installation  
✅ **File Detection** - All 5 detection methods working  
✅ **License Parsing** - Correct parsing of all fields  
✅ **CLI Interface** - All commands and options functional  
✅ **Performance** - Detection speed under 1 second  
✅ **Error Handling** - Graceful failure and recovery  

## 🎯 Sample AI Privacy License

The testing suite includes a complete sample AI Privacy License that demonstrates:

- **Do Not Train Flag**: "strict" → `allow_training: false`
- **Commercial Use**: "yes" → `allow_commercial: true`
- **Attribution Required**: "Yes" → `attribution_required: true`
- **Attribution Text**: Custom attribution message
- **Data Owner**: Sample data owner information

## 🔧 Customizing Examples

### **Modify Sample License**
Edit `testing/AiPrivacyLicense-1.0.txt` to test different:
- License parameters
- Field values
- Format variations

### **Add New Test Cases**
Edit `testing/test_local_detection.py` to add:
- New detection method tests
- Edge case scenarios
- Performance benchmarks

### **Create New Examples**
Add new example files to demonstrate:
- Different use cases
- Integration patterns
- Configuration options

## 📚 Documentation

- **`examples/README.md`** - This overview
- **`testing/README.md`** - Complete testing guide
- **`testing/test_commands.md`** - Manual testing commands
- **`testing/TESTING.md`** - Comprehensive testing documentation

## 🚨 Troubleshooting

**📚 [Complete Troubleshooting Guide → ../GETTING_STARTED.md#troubleshooting](../GETTING_STARTED.md#troubleshooting)**

Common issues and solutions are covered in the main setup guide.

### **Quick Fixes**

#### **Permission Denied**
```bash
chmod +x examples/testing/*.sh
```

#### **Getting Help**

1. **Check the testing guide**: `examples/testing/TESTING.md`
2. **Run quick tests**: `examples/testing/quick_test.sh`
3. **Review error messages** in test output
4. **Verify file paths** and permissions

## 🎉 Success Indicators

You'll know everything is working when:

✅ **Examples run** without errors  
✅ **All tests pass** with 100% success rate  
✅ **License detection works** for sample files  
✅ **CLI commands work** without errors  
✅ **Performance is good** (under 1 second detection)  

## 🔄 Continuous Development

For ongoing development:

1. **Run tests** before committing changes
2. **Update examples** when adding new features
3. **Add test cases** for new functionality
4. **Document changes** in relevant README files

---

**Ready to test your AI Privacy License Detection Library?** 🚀

Start with `examples/testing/quick_test.sh` to verify everything is working!
