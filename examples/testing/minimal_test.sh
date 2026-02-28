#!/bin/bash

echo "Starting minimal test..."

echo "Step 1: Print header"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           AI Privacy License Detection Tests                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"

echo "Step 2: Test command"
if command -v python3 &> /dev/null; then
    echo "✅ PASS: Python3 available"
else
    echo "❌ FAIL: Python3 missing"
fi

echo "Step 3: Test library import"
if python3 -c "import ai_privacy_license_detector" 2>/dev/null; then
    echo "✅ PASS: Library imported"
else
    echo "❌ FAIL: Library import failed"
fi

echo "Step 4: Test detector"
if python3 -c "from ai_privacy_license_detector import AIPrivacyLicenseDetector; print('OK')" 2>/dev/null; then
    echo "✅ PASS: Detector test"
else
    echo "❌ FAIL: Detector test"
fi

echo "Minimal test completed!"
