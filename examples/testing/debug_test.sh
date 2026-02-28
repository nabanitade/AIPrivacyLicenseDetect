#!/bin/bash

set -e

echo "🔍 Debug Test: Finding where run_tests.sh hangs..."

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "PASS")
            echo "✅ PASS: $message"
            ;;
        "FAIL")
            echo "❌ FAIL: $message"
            ;;
        "INFO")
            echo "ℹ️  INFO: $message"
            ;;
    esac
}

echo "Phase 1: Environment Checks"
command -v python3 && print_status "PASS" "python3 available" || print_status "FAIL" "python3 missing"
command -v pip3 && print_status "PASS" "pip3 available" || print_status "FAIL" "pip3 missing"

echo "Phase 2: Directory Check"
if [[ -f "../../setup.py" ]] && [[ -f "../../ai_privacy_license_detector/detector.py" ]]; then
    print_status "PASS" "Correct project directory structure found"
elif [[ -f "../setup.py" ]] && [[ -f "../ai_privacy_license_detector/detector.py" ]]; then
    print_status "PASS" "Project directory structure found in parent"
elif [[ -f "setup.py" ]] && [[ -f "ai_privacy_license_detector/detector.py" ]]; then
    print_status "PASS" "Correct project directory"
else
    print_status "FAIL" "Not in correct project directory"
    exit 1
fi

echo "Phase 3: File Checks"
[[ -f "AiPrivacyLicense-1.0.txt" ]] && print_status "PASS" "License file exists" || print_status "FAIL" "License file missing"

echo "Phase 4: Library Import"
python3 -c "import ai_privacy_license_detector" 2>/dev/null && print_status "PASS" "Library imported" || print_status "FAIL" "Library import failed"

echo "Phase 5: Basic Tests"
python3 -c "from ai_privacy_license_detector import AIPrivacyLicenseDetector; print('Import: OK')" && print_status "PASS" "Import test" || print_status "FAIL" "Import test"

python3 -c "from ai_privacy_license_detector import AIPrivacyLicenseDetector; detector = AIPrivacyLicenseDetector(); print('Detector: OK')" && print_status "PASS" "Detector creation" || print_status "FAIL" "Detector creation"

echo "Phase 6: License Parsing"
python3 -c "
from ai_privacy_license_detector import AIPrivacyLicenseDetector
detector = AIPrivacyLicenseDetector()
content = open('AiPrivacyLicense-1.0.txt').read()
restrictions = detector._parse_license_content(content)
print('PARSING_SUCCESS:', restrictions.do_not_train, restrictions.allow_training, restrictions.allow_commercial)
" && print_status "PASS" "License parsing test" || print_status "FAIL" "License parsing test"

echo "🎉 Debug test completed!"
