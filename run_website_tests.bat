@echo off
REM 🧪 Comprehensive Website Testing Suite for Windows
REM This script runs all the different types of website tests

echo 🧪 AI Privacy License Detector - Website Testing Suite
echo ================================================================
echo.

REM Check if we're in the right directory
if not exist "test_website.py" (
    echo ❌ Error: Please run this script from the project root directory
    echo    (where test_website.py is located)
    pause
    exit /b 1
)

REM Check if virtual environment is activated
if "%VIRTUAL_ENV%"=="" (
    echo ⚠️  Warning: Virtual environment not detected
    echo    Consider running: venv\Scripts\activate.bat
    echo.
)

:menu
echo 📋 Available Tests:
echo 1.  Single website test (like we did manually)
echo 2.  Batch test multiple websites
echo 3.  Interactive testing session
echo 4.  Run all tests
echo 5.  Exit
echo.

set /p "choice=Choose an option (1-5): "

if "%choice%"=="1" goto single_test
if "%choice%"=="2" goto batch_test
if "%choice%"=="3" goto interactive_test
if "%choice%"=="4" goto all_tests
if "%choice%"=="5" goto exit
echo ❌ Invalid option. Please choose 1-5.
goto menu

:single_test
echo.
set /p "url=Enter URL to test: "
if not "%url%"=="" (
    echo.
    echo 🔍 Running: Single Website Test
    echo    Testing: %url%
    echo.
    python test_website.py --verbose --all-methods "%url%"
    if %errorlevel% equ 0 (
        echo ✅ Single Website Test completed successfully
    ) else (
        echo ❌ Single Website Test failed
    )
) else (
    echo ❌ No URL provided
)
echo.
pause
goto menu

:batch_test
echo.
echo 📁 Available URL files:
dir *.txt | findstr /i "url"
echo.
set /p "url_file=Enter URL file name (or press Enter for sample_urls.txt): "
if "%url_file%"=="" set "url_file=sample_urls.txt"

if exist "%url_file%" (
    echo.
    echo 🔍 Running: Batch Website Test
    echo    Testing websites from: %url_file%
    echo.
    python test_multiple_websites.py --from-file "%url_file%" --summary-only
    if %errorlevel% equ 0 (
        echo ✅ Batch Website Test completed successfully
    ) else (
        echo ❌ Batch Website Test failed
    )
) else (
    echo ❌ File not found: %url_file%
)
echo.
pause
goto menu

:interactive_test
echo.
echo 🎮 Starting Interactive Test
echo    This will open an interactive session where you can test websites
echo    Type 'help' for commands, 'quit' to exit
echo.
pause
python interactive_test.py
goto menu

:all_tests
echo.
echo 🚀 Running All Tests
echo =====================
echo.

echo 🔍 Running: Single Website Test
echo    Tests the website we tested manually with all detection methods
echo.
python test_website.py --verbose --all-methods "https://keen-flan-b72fc1.netlify.app/"
if %errorlevel% equ 0 (
    echo ✅ Single Website Test completed successfully
) else (
    echo ❌ Single Website Test failed
)

echo.
echo ---
echo.

echo 🔍 Running: Batch Website Test
echo    Tests multiple websites from the sample URLs file
echo.
python test_multiple_websites.py --from-file "sample_urls.txt" --summary-only
if %errorlevel% equ 0 (
    echo ✅ Batch Website Test completed successfully
) else (
    echo ❌ Batch Website Test failed
)

echo.
echo ---
echo.

echo 🔍 Running: CLI Tool Test
echo    Tests that the CLI tool is working
echo.
python -m ai_privacy_license_detector.cli --version
if %errorlevel% equ 0 (
    echo ✅ CLI Tool Test completed successfully
) else (
    echo ❌ CLI Tool Test failed
)

echo.
echo 🎉 All tests completed!
pause
goto menu

:exit
echo 👋 Goodbye!
pause
exit /b 0
