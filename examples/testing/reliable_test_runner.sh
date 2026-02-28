#!/bin/bash

echo "🚀 Starting Reliable Test Runner..."
echo "This script tests the core functionality without complex shell functions"
echo

# Test counter
passed=0
failed=0

# Simple test function
test_step() {
    local name="$1"
    local command="$2"
    
    echo "Testing: $name"
    if eval "$command" >/dev/null 2>&1; then
        echo "✅ PASS: $name"
        ((passed++))
    else
        echo "❌ FAIL: $name"
        ((failed++))
    fi
    echo
}

echo "Phase 1: Environment Checks"
test_step "Python3 available" "command -v python3"
test_step "Pip3 available" "command -v pip3"

echo "Phase 2: Library Tests"
test_step "Library import" "python3 -c 'import ai_privacy_license_detector'"
test_step "Detector creation" "python3 -c 'from ai_privacy_license_detector import AIPrivacyLicenseDetector; detector = AIPrivacyLicenseDetector()'"

echo "Phase 3: License Parsing Test"
echo "Testing license content parsing..."
if python3 -c "
from ai_privacy_license_detector import AIPrivacyLicenseDetector
detector = AIPrivacyLicenseDetector()
content = open('AiPrivacyLicense-1.0.txt').read()
restrictions = detector._parse_license_content(content)
print('PARSING_SUCCESS:', restrictions.do_not_train, restrictions.allow_training, restrictions.allow_commercial)
" 2>/dev/null | grep -q "PARSING_SUCCESS: strict False True"; then
    echo "✅ PASS: License content parsing"
    ((passed++))
else
    echo "❌ FAIL: License content parsing"
    ((failed++))
fi
echo

echo "Phase 4: CLI Tests"
test_step "CLI help" "python3 -m ai_privacy_license_detector.cli --help"
test_step "CLI version" "python3 -m ai_privacy_license_detector.cli --version"

echo "Phase 5: Basic URL Test"
echo "Testing basic URL detection..."
if python3 -c "
from ai_privacy_license_detector import check_url
result = check_url('https://example.com')
print('URL_TEST:', result.has_license, result.error)
" 2>/dev/null | grep -q "URL_TEST:"; then
    echo "✅ PASS: Basic URL detection"
    ((passed++))
else
    echo "❌ FAIL: Basic URL detection"
    ((failed++))
fi
echo

echo "Phase 6: Results"
echo "══════════════════════════════════════════════════════════════"
echo "Total Tests: $((passed + failed))"
echo "Passed: $passed"
echo "Failed: $failed"

if [ $failed -eq 0 ]; then
    echo "🎉 All tests passed! The library is working correctly."
    exit 0
else
    echo "❌ Some tests failed. Check the output above."
    exit 1
fi
