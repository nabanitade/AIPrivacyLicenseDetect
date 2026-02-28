#!/bin/bash

# 🧪 Comprehensive Website Testing Suite
# This script runs all the different types of website tests

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 AI Privacy License Detector - Website Testing Suite${NC}"
echo "================================================================"
echo

# Check if we're in the right directory
if [[ ! -f "test_website.py" ]]; then
    echo -e "${RED}❌ Error: Please run this script from the project root directory${NC}"
    echo "   (where test_website.py is located)"
    exit 1
fi

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}⚠️  Warning: Virtual environment not detected${NC}"
    echo "   Consider running: source venv/bin/activate"
    echo
fi

# Function to run a test
run_test() {
    local test_name="$1"
    local command="$2"
    local description="$3"
    
    echo -e "${BLUE}🔍 Running: ${test_name}${NC}"
    echo "   ${description}"
    echo "   Command: ${command}"
    echo
    
    if eval "$command"; then
        echo -e "${GREEN}✅ ${test_name} completed successfully${NC}"
    else
        echo -e "${RED}❌ ${test_name} failed${NC}"
        return 1
    fi
    
    echo
    echo "---"
    echo
}

# Function to run interactive test
run_interactive_test() {
    echo -e "${BLUE}🎮 Starting Interactive Test${NC}"
    echo "   This will open an interactive session where you can test websites"
    echo "   Type 'help' for commands, 'quit' to exit"
    echo
    
    read -p "Press Enter to continue, or Ctrl+C to skip..."
    
    python3 interactive_test.py
}

# Main test menu
show_menu() {
    echo -e "${BLUE}📋 Available Tests:${NC}"
    echo "1.  Single website test (like we did manually)"
    echo "2.  Batch test multiple websites"
    echo "3.  Interactive testing session"
    echo "4.  Run all tests"
    echo "5.  Exit"
    echo
}

# Run all tests
run_all_tests() {
    echo -e "${BLUE}🚀 Running All Tests${NC}"
    echo "====================="
    echo
    
    # Test 1: Single website
    run_test "Single Website Test" \
        "python3 test_website.py --verbose --all-methods https://keen-flan-b72fc1.netlify.app/" \
        "Tests the website we tested manually with all detection methods"
    
    # Test 2: Batch test
    run_test "Batch Website Test" \
        "python3 test_multiple_websites.py --from-file sample_urls.txt --summary-only" \
        "Tests multiple websites from the sample URLs file"
    
    # Test 3: CLI test
    run_test "CLI Tool Test" \
        "python3 -m ai_privacy_license_detector.cli --version" \
        "Tests that the CLI tool is working"
    
    echo -e "${GREEN}🎉 All tests completed!${NC}"
}

# Main loop
while true; do
    show_menu
    read -p "Choose an option (1-5): " choice
    
    case $choice in
        1)
            echo
            read -p "Enter URL to test: " url
            if [[ -n "$url" ]]; then
                run_test "Single Website Test" \
                    "python3 test_website.py --verbose --all-methods \"$url\"" \
                    "Testing: $url"
            else
                echo -e "${RED}❌ No URL provided${NC}"
            fi
            ;;
        2)
            echo
            echo -e "${BLUE}📁 Available URL files:${NC}"
            ls -la *.txt | grep -E "(url|URL)" || echo "   No URL files found"
            echo
            read -p "Enter URL file name (or press Enter for sample_urls.txt): " url_file
            url_file=${url_file:-sample_urls.txt}
            
            if [[ -f "$url_file" ]]; then
                run_test "Batch Website Test" \
                    "python3 test_multiple_websites.py --from-file \"$url_file\" --summary-only" \
                    "Testing websites from: $url_file"
            else
                echo -e "${RED}❌ File not found: $url_file${NC}"
            fi
            ;;
        3)
            echo
            run_interactive_test
            ;;
        4)
            echo
            run_all_tests
            ;;
        5)
            echo -e "${GREEN}👋 Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Invalid option. Please choose 1-5.${NC}"
            ;;
    esac
    
    echo
    read -p "Press Enter to continue..."
    echo
done
