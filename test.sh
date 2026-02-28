#!/bin/bash

# 🧪 AI Privacy License Detection Library Test Runner
# This script runs tests from the examples/testing directory

echo "🧪 AI Privacy License Detection Library Test Runner"
echo "=================================================="
echo

# Check if we're in the right directory
if [[ ! -f "setup.py" ]] || [[ ! -d "ai_privacy_license_detector" ]]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo "   You should see setup.py and ai_privacy_license_detector/ folder"
    exit 1
fi

# Check if examples/testing directory exists
if [[ ! -d "examples/testing" ]]; then
    echo "❌ Error: examples/testing directory not found"
    echo "   Please ensure the examples directory is properly set up"
    exit 1
fi

echo "✅ Project directory verified"
echo "✅ Examples directory found"

# Check if virtual environment exists
if [[ -d "venv" ]]; then
    echo "✅ Virtual environment found"
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found"
    echo "   Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Installing dependencies..."
    pip install requests beautifulsoup4 urllib3
    echo "📦 Installing library..."
    pip install -e .
    echo "✅ Virtual environment ready"
fi

echo

# Change to testing directory and run tests
cd examples/testing

echo "🚀 Running tests from examples/testing directory..."
echo

# Check if test scripts exist and are executable
if [[ ! -x "quick_test.sh" ]]; then
    echo "⚠️  Making test scripts executable..."
    chmod +x *.sh
fi

echo "Choose your test option:"
echo "1) Quick test (30 seconds) - recommended for first run"
echo "2) Comprehensive test suite (2-3 minutes)"
echo "3) View testing documentation"
echo "4) Exit"
echo

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo
        echo "🚀 Running quick test..."
        ./quick_test.sh
        ;;
    2)
        echo
        echo "🚀 Running comprehensive test suite..."
        ./run_tests.sh
        ;;
    3)
        echo
        echo "📚 Testing Documentation:"
        echo "========================="
        echo
        echo "📖 README.md - Testing guide and overview"
        echo "📋 TESTING.md - Comprehensive testing documentation"
        echo "🔧 test_commands.md - Manual testing commands"
        echo "🐍 test_local_detection.py - Python test script"
        echo
        echo "To run tests manually:"
        echo "  ./quick_test.sh     # Quick test (30 seconds)"
        echo "  ./run_tests.sh      # Full test suite (2-3 minutes)"
        echo
        echo "For more information, see:"
        echo "  examples/testing/README.md"
        echo "  examples/testing/TESTING.md"
        ;;
    4)
        echo "👋 Exiting..."
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo
echo "🎯 Test completed!"
echo "For more testing options, see: examples/testing/"
