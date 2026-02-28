#!/bin/bash

# 🚀 Quick Test Script for AI Privacy License Detection Library
# This script runs basic tests quickly to verify core functionality

echo "🚀 Quick Test: AI Privacy License Detection Library"
echo "=================================================="
echo

# Check if library is installed
echo "📦 Checking library installation..."
if python3 -c "import ai_privacy_license_detector" 2>/dev/null; then
    echo "✅ Library is installed"
else
    echo "⚠️  Library not installed, checking virtual environment..."
    # Check if we're in a virtual environment
    if [[ -n "$VIRTUAL_ENV" ]]; then
        echo "✅ Virtual environment detected: $VIRTUAL_ENV"
        echo "⚠️  Please activate the virtual environment first:"
        echo "   source venv/bin/activate"
        exit 1
    else
        echo "⚠️  Please activate the virtual environment first:"
        echo "   source venv/bin/activate"
        exit 1
    fi
fi

echo

# Test 1: Basic import and detection
echo "🔍 Test 1: Basic License Detection"
python3 -c "
from ai_privacy_license_detector import AIPrivacyLicenseDetector
detector = AIPrivacyLicenseDetector(verbose=True)
print('✅ Detector created successfully')
print('   - Timeout:', detector.timeout)
print('   - User Agent:', detector.user_agent)
print('   - Verbose:', detector.verbose)
print('   - Insecure SSL:', detector.insecure_ssl)
"

echo

# Test 2: CLI tool
echo "🖥️  Test 2: CLI Tool"
python3 -m ai_privacy_license_detector.cli --help

echo

# Test 3: Library Structure
echo "⚡ Test 3: Library Structure"
python3 -c "
from ai_privacy_license_detector import AIPrivacyLicenseDetector, LicenseDetectionResult, LicenseRestriction
print('✅ Library structure:')
print('   - AIPrivacyLicenseDetector:', AIPrivacyLicenseDetector)
print('   - LicenseDetectionResult:', LicenseDetectionResult)
print('   - LicenseRestriction:', LicenseRestriction)
"

echo
echo "🎯 Quick test completed!"
echo "Run './run_tests.sh' for comprehensive testing"
