# 📁 Examples Directory Structure

This document provides an overview of the examples directory organization.

## 🗂️ Directory Layout

```
examples/
├── README.md                    # Main examples overview
├── __init__.py                 # Python package initialization
├── example_check.py            # Basic usage examples
└── testing/                    # Complete testing suite
    ├── README.md               # Testing guide and overview
    ├── TESTING.md              # Comprehensive testing documentation
    ├── test_commands.md        # Manual testing commands
    ├── test_local_detection.py # Python test script
    ├── run_tests.sh            # Comprehensive test runner
    ├── quick_test.sh           # Quick test script
    ├── AiPrivacyLicense-1.0.txt # Sample license file
    ├── robots.txt              # Sample robots.txt
    └── test_page.html          # Sample HTML page
```

## 🎯 Purpose of Each Directory

### **`examples/` (Root)**
- **Purpose**: Main examples and testing tools
- **Contents**: Basic usage examples and testing suite
- **Audience**: Developers and users

### **`examples/testing/`**
- **Purpose**: Complete testing infrastructure
- **Contents**: Test files, scripts, and documentation
- **Audience**: Developers, testers, and CI/CD systems

## 📋 File Descriptions

### **Main Examples**
| File | Purpose | Description |
|------|---------|-------------|
| `README.md` | Documentation | Main examples overview and usage guide |
| `example_check.py` | Code Examples | Basic usage patterns and integration examples |
| `__init__.py` | Package | Python package initialization |

### **Testing Suite**
| File | Purpose | Description |
|------|---------|-------------|
| `README.md` | Documentation | Testing guide and quick start |
| `TESTING.md` | Documentation | Comprehensive testing documentation |
| `test_commands.md` | Reference | Manual testing commands and examples |
| `test_local_detection.py` | Script | Python-based testing script |
| `run_tests.sh` | Script | Comprehensive test runner (25+ tests) |
| `quick_test.sh` | Script | Quick test runner (30 seconds) |

### **Test Data**
| File | Purpose | Description |
|------|---------|-------------|
| `AiPrivacyLicense-1.0.txt` | Sample License | Complete AI Privacy License for testing |
| `robots.txt` | Sample Config | robots.txt with AI Privacy License declaration |
| `test_page.html` | Sample HTML | HTML page demonstrating all detection methods |

## 🚀 Usage Patterns

### **For End Users**
```bash
# Run basic examples
python3 examples/example_check.py

# Run interactive test runner
./test.sh
```

### **For Developers**
```bash
# Quick testing
cd examples/testing
./quick_test.sh

# Comprehensive testing
./run_tests.sh

# Custom testing
python3 test_local_detection.py
```

### **For CI/CD**
```bash
# Automated testing
cd examples/testing
./run_tests.sh

# Exit code 0 = success, 1 = failure
```

## 🔧 Customization

### **Adding New Examples**
1. Create new Python files in `examples/`
2. Update `examples/README.md`
3. Add to main project documentation

### **Adding New Tests**
1. Update `test_local_detection.py`
2. Add test data files if needed
3. Update testing documentation

### **Modifying Test Data**
1. Edit sample files in `testing/`
2. Update expected results in test scripts
3. Verify tests still pass

## 📚 Documentation Flow

```
examples/README.md (Overview)
    ↓
examples/testing/README.md (Testing Guide)
    ↓
examples/testing/TESTING.md (Comprehensive Docs)
    ↓
examples/testing/test_commands.md (Manual Commands)
```

## 🎉 Benefits of This Structure

✅ **Organized**: Clear separation of examples and testing  
✅ **Accessible**: Easy to find and use testing tools  
✅ **Maintainable**: Centralized testing infrastructure  
✅ **Documented**: Comprehensive guides for all use cases  
✅ **Flexible**: Easy to add new examples and tests  
✅ **Professional**: Industry-standard project organization  

## 🔄 Maintenance

### **Regular Tasks**
1. **Update examples** when adding new features
2. **Verify tests** still pass after changes
3. **Update documentation** to reflect changes
4. **Clean up** outdated examples and tests

### **Before Releases**
1. **Run full test suite**: `./run_tests.sh`
2. **Verify examples work**: `python3 examples/example_check.py`
3. **Check documentation**: Review all README files
4. **Test installation**: Verify `pip install` works

---

**This structure makes your AI Privacy License Detection Library easy to test, use, and maintain!** 🚀
