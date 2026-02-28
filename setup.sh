#!/bin/bash

# 🚀 AI Privacy License Detector Setup Script
# This script sets up the Python environment and installs all dependencies

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 AI Privacy License Detector Setup Script${NC}"
echo "=================================================="
echo

# Check if Python 3.8+ is available
echo -e "${BLUE}📋 Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    echo -e "${GREEN}✅ Python found: $PYTHON_VERSION${NC}"
    
    # Check if version is 3.8 or higher
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
        echo -e "${GREEN}✅ Python version 3.8+ confirmed${NC}"
    else
        echo -e "${RED}❌ Python version must be 3.8 or higher${NC}"
        echo "Current version: $PYTHON_VERSION"
        exit 1
    fi
else
    echo -e "${RED}❌ Python 3 not found${NC}"
    echo "Please install Python 3.8 or higher and try again"
    exit 1
fi

# Check if pip is available
echo -e "${BLUE}📦 Checking pip...${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✅ pip3 found${NC}"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    echo -e "${GREEN}✅ pip found${NC}"
    PIP_CMD="pip"
else
    echo -e "${RED}❌ pip not found${NC}"
    echo "Please install pip and try again"
    exit 1
fi

# Create virtual environment
echo -e "${BLUE}🔧 Creating virtual environment...${NC}"
if [[ -d "venv" ]]; then
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
    echo "Using existing virtual environment..."
else
    echo "Creating new virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

if [[ ! -d "venv" ]]; then
    echo "Creating new virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Upgrade pip
echo -e "${BLUE}📦 Upgrading pip...${NC}"
$PIP_CMD install --upgrade pip
echo -e "${GREEN}✅ pip upgraded${NC}"

# Install dependencies
echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
$PIP_CMD install requests beautifulsoup4 urllib3
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Install the library
echo -e "${BLUE}📦 Installing AI Privacy License Detector...${NC}"
$PIP_CMD install -e .
echo -e "${GREEN}✅ Library installed${NC}"

# Test installation
echo -e "${BLUE}🧪 Testing installation...${NC}"
if python3 -c "import ai_privacy_license_detector; print('✅ Library import successful')" 2>/dev/null; then
    echo -e "${GREEN}✅ Library import test passed${NC}"
else
    echo -e "${RED}❌ Library import test failed${NC}"
    exit 1
fi

# Test CLI
echo -e "${BLUE}🧪 Testing CLI...${NC}"
if python3 -m ai_privacy_license_detector.cli --version >/dev/null 2>&1; then
    echo -e "${GREEN}✅ CLI test passed${NC}"
else
    echo -e "${RED}❌ CLI test failed${NC}"
    exit 1
fi

# Make test scripts executable
echo -e "${BLUE}🔧 Making test scripts executable...${NC}"
if [[ -d "examples/testing" ]]; then
    chmod +x examples/testing/*.sh
    echo -e "${GREEN}✅ Test scripts made executable${NC}"
else
    echo -e "${YELLOW}⚠️  examples/testing directory not found${NC}"
fi

echo
echo -e "${GREEN}🎉 Setup completed successfully!${NC}"
echo
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "1. Activate virtual environment: ${GREEN}source venv/bin/activate${NC}"
echo "2. Run quick test: ${GREEN}cd examples/testing && ./quick_test.sh${NC}"
echo "3. Run comprehensive test: ${GREEN}./run_tests.sh${NC}"
echo "4. Start using the library: ${GREEN}python3 examples/example_check.py${NC}"
echo
echo -e "${BLUE}📚 Documentation:${NC}"
echo "- Main README: ${GREEN}README.md${NC}"
echo "- Examples: ${GREEN}examples/README.md${NC}"
echo "- Testing: ${GREEN}examples/testing/README.md${NC}"
echo
echo -e "${GREEN}🚀 Your AI Privacy License Detector is ready to use!${NC}"
