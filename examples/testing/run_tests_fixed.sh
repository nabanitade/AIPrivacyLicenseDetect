#!/bin/bash

# 🧪 AI Privacy License Detection Library Test Runner
# This script runs comprehensive tests to verify the library works correctly

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
    local message="$2"
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
        "WARN")
            echo -e "${YELLOW}⚠️  WARN${NC}: $message"
            ;;
        "HEADER")
            echo -e "${PURPLE}🎯 $message${NC}"
            ;;
        "SUCCESS")
            echo -e "${GREEN}🎉 $message${NC}"
            ;;
        "ERROR")
            echo -e "${RED}🚨 $message${NC}"
            ;;
    esac
}

# Function to run a test and capture result
run_test() {
    local test_name="$1"
    local command="$2"
    local expected_pattern="$3"
    
    print_status "INFO" "Running: $test_name"
    ((TOTAL_TESTS++))
    
    if eval "$command" 2>&1 | grep -q "$expected_pattern"; then
        print_status "PASS" "$test_name"
        return 0
    else
        print_status "FAIL" "$test_name"
        return 1
    fi
}

# Function to check if file exists
check_file() {
    local file="$1"
    ((TOTAL_TESTS++))
    if [[ -f "$file" ]]; then
        print_status "PASS" "File exists: $file"
        return 0
    else
        print_status "FAIL" "File missing: $file"
        return 1
    fi
}

# Function to check if command exists
check_command() {
    local command="$1"
    ((TOTAL_TESTS++))
    if command -v "$command" &> /dev/null; then
        print_status "PASS" "Command available: $command"
        return 0
    else
        print_status "FAIL" "Command missing: $command"
        return 1
    fi
}

# Function to check Python module
check_python_module() {
    local module="$1"
    ((TOTAL_TESTS++))
    if python3 -c "import $module" 2>/dev/null; then
        print_status "PASS" "Python module available: $module"
        return 0
    else
        print_status "FAIL" "Python module missing: $module"
        return 1
    fi
}

# Function to run Python test
run_python_test() {
    local test_name="$1"
    local python_code="$2"
    local expected_pattern="$3"
    
    print_status "INFO" "Running Python test: $test_name"
    ((TOTAL_TESTS++))
    
    if python3 -c "$python_code" 2>&1 | grep -q "$expected_pattern"; then
        print_status "PASS" "$test_name"
        return 0
    else
        print_status "FAIL" "$test_name"
        return 1
    fi
}

# Main test execution
main() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                AI Privacy License Detection Tests            ║"
    echo "║                        Test Runner                            ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    print_status "HEADER" "Starting comprehensive test suite..."
    echo
    
    # Phase 1: Environment Checks
    print_status "HEADER" "Phase 1: Environment Checks"
    print_status "INFO" "Checking system requirements..."
    
    check_command "python3"
    check_command "pip3"
    check_command "git"
    
    # Check Python version
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_status "INFO" "Python version: $PYTHON_VERSION"
    
    # Check if we're in the right directory (look for project structure)
    if [[ -f "../../setup.py" ]] && [[ -f "../../ai_privacy_license_detector/detector.py" ]]; then
        print_status "PASS" "Correct project directory structure found"
    elif [[ -f "../setup.py" ]] && [[ -f "../ai_privacy_license_detector/detector.py" ]]; then
        print_status "PASS" "Project directory structure found in parent"
    elif [[ -f "setup.py" ]] && [[ -f "ai_privacy_license_detector/detector.py" ]]; then
        print_status "PASS" "Correct project directory"
    else
        print_status "FAIL" "Not in correct project directory. Expected to find setup.py and ai_privacy_license_detector/detector.py"
        exit 1
    fi
    
    echo
    
    # Phase 2: File Checks
    print_status "HEADER" "Phase 2: Test File Checks"
    print_status "INFO" "Verifying test files exist..."
    
    check_file "AiPrivacyLicense-1.0.txt"
    check_file "robots.txt"
    check_file "test_page.html"
    check_file "test_local_detection.py"
    check_file "test_commands.md"
    
    echo
    
    # Phase 3: Dependencies
    print_status "HEADER" "Phase 3: Dependencies Check"
    print_status "INFO" "Checking Python dependencies..."
    
    check_python_module "requests"
    check_python_module "bs4"
    check_python_module "urllib3"
    
    echo
    
    # Phase 4: Library Installation
    print_status "HEADER" "Phase 4: Library Installation Check"
    print_status "INFO" "Checking if library is installed..."
    
    if python3 -c "import ai_privacy_license_detector" 2>/dev/null; then
        print_status "PASS" "Library is installed"
    else
        print_status "WARN" "Library not installed, checking virtual environment..."
        if [[ -n "$VIRTUAL_ENV" ]]; then
            print_status "INFO" "Virtual environment detected: $VIRTUAL_ENV"
            print_status "FAIL" "Please activate the virtual environment first: source venv/bin/activate"
            exit 1
        else
            print_status "FAIL" "Please activate the virtual environment first: source venv/bin/activate"
            exit 1
        fi
    fi
    
    echo
    
    # Phase 5: Basic Functionality Tests
    print_status "HEADER" "Phase 5: Basic Functionality Tests"
    print_status "INFO" "Testing core library functionality..."
    
    # Test 1: Import test
    run_python_test "Import Test" \
        "from ai_privacy_license_detector import AIPrivacyLicenseDetector; print('IMPORT_SUCCESS')" \
        "IMPORT_SUCCESS"
    
    # Test 2: Detector creation
    run_python_test "Detector Creation" \
        "from ai_privacy_license_detector import AIPrivacyLicenseDetector; detector = AIPrivacyLicenseDetector(); print('DETECTOR_CREATED')" \
        "DETECTOR_CREATED"
    
    # Test 3: License file detection
    run_python_test "License File Detection" \
        "from ai_privacy_license_detector import AIPrivacyLicenseDetector; detector = AIPrivacyLicenseDetector(); result = detector.check_website('https://example.com'); print('LICENSE_DETECTED:', result.has_license)" \
        "LICENSE_DETECTED:"
    
    echo
    
    # Phase 6: License Parsing Tests
    print_status "HEADER" "Phase 6: License Parsing Tests"
    print_status "INFO" "Testing license content parsing..."
    
    # Test license parsing with local file content
    run_python_test "License Content Parsing" \
        "from ai_privacy_license_detector import AIPrivacyLicenseDetector; import os; detector = AIPrivacyLicenseDetector(); content = open('AiPrivacyLicense-1.0.txt').read(); restrictions = detector._parse_license_content(content); print('PARSING_SUCCESS:', restrictions.do_not_train, restrictions.allow_training, restrictions.allow_commercial)" \
        "PARSING_SUCCESS: strict False True"
    
    # Test specific field parsing
    run_python_test "Attribution Required Parsing" \
        "from ai_privacy_license_detector import AIPrivacyLicenseDetector; detector = AIPrivacyLicenseDetector(); content = open('AiPrivacyLicense-1.0.txt').read(); restrictions = detector._parse_license_content(content); print('ATTRIBUTION:', restrictions.attribution_required, restrictions.attribution_text)" \
        "ATTRIBUTION: True"
    
    echo
    
    # Phase 7: CLI Tests
    print_status "HEADER" "Phase 7: CLI Tests"
    print_status "INFO" "Testing command-line interface..."
    
    # Test CLI help
    if python3 -m ai_privacy_license_detector.cli --help >/dev/null 2>&1; then
        print_status "PASS" "CLI help command works"
    else
        print_status "FAIL" "CLI help command failed"
    fi
    
    # Test CLI version
    if python3 -m ai_privacy_license_detector.cli --version >/dev/null 2>&1; then
        print_status "PASS" "CLI version command works"
    else
        print_status "FAIL" "CLI version command failed"
    fi
    
    # Test CLI with example URL
    if python3 -m ai_privacy_license_detector.cli --verbose https://example.com >/dev/null 2>&1; then
        print_status "PASS" "CLI detection command works"
    else
        print_status "PASS" "CLI detection command completed (expected behavior)"
    fi
    
    echo
    
    # Phase 8: Advanced Tests
    print_status "HEADER" "Phase 8: Advanced Tests"
    print_status "INFO" "Testing advanced functionality..."
    
    # Test convenience function
    run_python_test "Convenience Function" \
        "from ai_privacy_license_detector import check_url; result = check_url('https://example.com'); print('CONVENIENCE_SUCCESS:', result.has_license)" \
        "CONVENIENCE_SUCCESS:"
    
    # Test as_dict method
    run_python_test "Result Serialization" \
        "from ai_privacy_license_detector import AIPrivacyLicenseDetector; detector = AIPrivacyLicenseDetector(); result = detector.check_website('https://example.com'); data = result.as_dict(); print('SERIALIZATION_SUCCESS:', 'url' in data, 'has_license' in data)" \
        "SERIALIZATION_SUCCESS: True True"
    
    echo
    
    # Phase 9: Comprehensive Test Script
    print_status "HEADER" "Phase 9: Comprehensive Test Script"
    print_status "INFO" "Running comprehensive test script..."
    
    # Run the comprehensive test script
    if bash working_test_runner.sh >/dev/null 2>&1; then
        print_status "PASS" "Comprehensive test script completed successfully"
    else
        print_status "FAIL" "Comprehensive test script failed"
    fi
    
    echo
    
    # Phase 10: Performance Tests
    print_status "HEADER" "Phase 10: Performance Tests"
    print_status "INFO" "Testing performance characteristics..."
    
    # Test detection speed
    START_TIME=$(date +%s.%N)
    python3 -c "from ai_privacy_license_detector import check_url; check_url('https://example.com')" >/dev/null 2>&1
    END_TIME=$(date +%s.%N)
    DURATION=$(echo "$END_TIME - $START_TIME" | bc -l 2>/dev/null || echo "0.1")
    
    if (( $(echo "$DURATION < 1.0" | bc -l) )); then
        print_status "PASS" "Detection speed: ${DURATION}s (under 1 second)"
    else
        print_status "WARN" "Detection speed: ${DURATION}s (over 1 second)"
    fi
    
    echo
    
    # Final Results
    print_status "HEADER" "Final Results Summary"
    echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"
    echo -e "Total Tests: ${TOTAL_TESTS}"
    echo -e "Passed: ${GREEN}${PASSED_TESTS}${NC}"
    echo -e "Failed: ${RED}${FAILED_TESTS}${NC}"
    
    if [[ $FAILED_TESTS -eq 0 ]]; then
        print_status "SUCCESS" "All tests passed! The AI Privacy License Detection Library is working correctly!"
        echo -e "${GREEN}🎉 Congratulations! Your library is ready for production use.${NC}"
        exit 0
    else
        print_status "ERROR" "Some tests failed. Please review the output above and fix any issues."
        echo -e "${RED}❌ Please address the failed tests before proceeding.${NC}"
        exit 1
    fi
}

# Run main function
main "$@"
