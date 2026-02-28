@echo off
REM 🚀 AI Privacy License Detector Setup Script for Windows
REM This script sets up the Python environment and installs all dependencies

echo 🚀 AI Privacy License Detector Setup Script
echo ==================================================
echo.

REM Check if Python is available
echo 📋 Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found
    echo Please install Python 3.8 or higher and try again
    pause
    exit /b 1
)

python --version
echo ✅ Python found

REM Check if pip is available
echo 📦 Checking pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip not found
    echo Please install pip and try again
    pause
    exit /b 1
)

echo ✅ pip found

REM Create virtual environment
echo 🔧 Creating virtual environment...
if exist "venv" (
    echo ⚠️  Virtual environment already exists
    echo Using existing virtual environment...
) else (
    echo Creating new virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat
echo ✅ Virtual environment activated

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip
echo ✅ pip upgraded

REM Install dependencies
echo 📦 Installing Python dependencies...
pip install requests beautifulsoup4 urllib3
echo ✅ Dependencies installed

REM Install the library
echo 📦 Installing AI Privacy License Detector...
pip install -e .
echo ✅ Library installed

REM Test installation
echo 🧪 Testing installation...
python -c "import ai_privacy_license_detector; print('✅ Library import successful')" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Library import test failed
    pause
    exit /b 1
)
echo ✅ Library import test passed

REM Test CLI
echo 🧪 Testing CLI...
python -m ai_privacy_license_detector.cli --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ CLI test failed
    pause
    exit /b 1
)
echo ✅ CLI test passed

echo.
echo 🎉 Setup completed successfully!
echo.
echo 📋 Next Steps:
echo 1. Activate virtual environment: venv\Scripts\activate.bat
echo 2. Run quick test: cd examples\testing ^&^& quick_test.sh
echo 3. Start using the library: python examples\example_check.py
echo.
echo 📚 Documentation:
echo - Main README: README.md
echo - Examples: examples\README.md
echo - Testing: examples\testing\README.md
echo.
echo 🚀 Your AI Privacy License Detector is ready to use!
pause
