#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "PASS")
            echo -e "${GREEN}✅ PASS${NC}: $message"
            ((PASSED_TESTS++))
            ;;
        "FAIL")
            echo -e "${RED}❌ FAIL${NC}: $message"
            ((FAILED_TESTS++))
            ;;
        "INFO")
            echo -e "${BLUE}ℹ️  INFO${NC}: $message"
            ;;
        "HEADER")
            echo -e "${PURPLE}🎯 $message${NC}"
            ;;
    esac
    ((TOTAL_TESTS++))
}

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           AI Privacy License Detection Tests (Simple)        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

print_status "HEADER" "Starting simplified test suite..."
echo

# Phase 1: Environment Checks
print_status "HEADER" "Phase 1: Environment Checks"

if command -v python3 &> /dev/null; then
    print_status "PASS" "Python3 available"
else
    print_status "FAIL" "Python3 missing"
fi

if command -v pip3 &> /dev/null; then
    print_status "PASS" "Pip3 available"
else
    print_status "FAIL" "Pip3 missing"
fi

# Phase 2: Library Import
print_status "HEADER" "Phase 2: Library Import"

if python3 -c "import ai_privacy_license_detector" 2>/dev/null; then
    print_status "PASS" "Library imported successfully"
else
    print_status "FAIL" "Library import failed"
    exit 1
fi

# Phase 3: Basic Functionality
print_status "HEADER" "Phase 3: Basic Functionality"

# Test detector creation
if python3 -c "from ai_privacy_license_detector import AIPrivacyLicenseDetector; detector = AIPrivacyLicenseDetector(); print('OK')" 2>/dev/null | grep -q "OK"; then
    print_status "PASS" "Detector creation"
else
    print_status "FAIL" "Detector creation"
fi

# Test license parsing
if python3 -c "
from ai_privacy_license_detector import AIPrivacyLicenseDetector
detector = AIPrivacyLicenseDetector()
content = open('AiPrivacyLicense-1.0.txt').read()
restrictions = detector._parse_license_content(content)
print('PARSING_SUCCESS:', restrictions.do_not_train, restrictions.allow_training, restrictions.allow_commercial)
" 2>/dev/null | grep -q "PARSING_SUCCESS: strict False True"; then
    print_status "PASS" "License content parsing"
else
    print_status "FAIL" "License content parsing"
fi

# Phase 4: CLI Tests
print_status "HEADER" "Phase 4: CLI Tests"

# Test CLI help
if python3 -m ai_privacy_license_detector.cli --help >/dev/null 2>&1; then
    print_status "PASS" "CLI help command"
else
    print_status "FAIL" "CLI help command"
fi

# Test CLI version
if python3 -m ai_privacy_license_detector.cli --version >/dev/null 2>&1; then
    print_status "PASS" "CLI version command"
else
    print_status "FAIL" "CLI version command"
fi

# Final Results
echo
print_status "HEADER" "Test Results Summary"
echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"
echo -e "Total Tests: ${TOTAL_TESTS}"
echo -e "Passed: ${GREEN}${PASSED_TESTS}${NC}"
echo -e "Failed: ${RED}${FAILED_TESTS}${NC}"

if [[ $FAILED_TESTS -eq 0 ]]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    echo -e "${GREEN}The AI Privacy License Detection Library is working correctly!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed.${NC}"
    exit 1
fi
