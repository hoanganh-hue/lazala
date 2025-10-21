@echo off
REM Google Maps Scraper - Windows Build Script
REM This script automates the entire build process for Windows

echo ========================================
echo Google Maps Scraper - Build Script
echo ========================================
echo.

REM Check if running on Windows
if not "%OS%"=="Windows_NT" (
    echo ERROR: This script must run on Windows!
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.10 or higher.
    echo Download from: https://www.python.org/downloads/
    exit /b 1
)

echo [1/6] Checking Python version...
python --version
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [2/6] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        exit /b 1
    )
) else (
    echo [2/6] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    exit /b 1
)
echo.

REM Install dependencies
echo [4/6] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    exit /b 1
)
echo.

REM Run tests (optional)
set /p run_tests="Run tests before building? (y/n): "
if /i "%run_tests%"=="y" (
    echo [5/6] Running tests...
    python run_tests.py --type unit
    if errorlevel 1 (
        echo WARNING: Some tests failed!
        set /p continue="Continue with build? (y/n): "
        if /i not "%continue%"=="y" (
            echo Build cancelled.
            exit /b 1
        )
    )
) else (
    echo [5/6] Skipping tests...
)
echo.

REM Build application
echo [6/6] Building application...
python build.py --clean
if errorlevel 1 (
    echo ERROR: Build failed!
    exit /b 1
)
echo.

echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Executable: dist\GoogleMapsScraper.exe
echo Installer: installer\GoogleMapsScraper_Setup_v1.0.0.exe
echo.
echo Next steps:
echo 1. Test the executable: dist\GoogleMapsScraper.exe
echo 2. Test the installer: installer\GoogleMapsScraper_Setup_v1.0.0.exe
echo 3. Upload installer to GitHub Releases
echo.

pause
