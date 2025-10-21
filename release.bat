@echo off
REM Google Maps Scraper - Release Script
REM This script helps create a new release with proper version tagging

echo ========================================
echo Google Maps Scraper - Release Helper
echo ========================================
echo.

REM Get current version from setup.py
for /f "tokens=2 delims==" %%a in ('findstr /r "version=" setup.py') do set VERSION=%%a
set VERSION=%VERSION:"=%
set VERSION=%VERSION:,=%
set VERSION=%VERSION: =%

echo Current version: %VERSION%
echo.

REM Ask for new version
set /p NEW_VERSION="Enter new version (e.g., 1.0.1) or press Enter to keep current: "
if "%NEW_VERSION%"=="" set NEW_VERSION=%VERSION%

echo.
echo New version: %NEW_VERSION%
echo.

REM Ask for confirmation
set /p CONFIRM="Continue with release v%NEW_VERSION%? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo Release cancelled.
    exit /b 0
)

echo.
echo [1/6] Updating version numbers...

REM Update version in setup.py
powershell -Command "(gc setup.py) -replace 'version=\"[0-9.]+\"', 'version=\"%NEW_VERSION%\"' | Out-File -encoding ASCII setup.py"

REM Update version in installer.iss
powershell -Command "(gc installer.iss) -replace '#define MyAppVersion \"[0-9.]+\"', '#define MyAppVersion \"%NEW_VERSION%\"' | Out-File -encoding ASCII installer.iss"

echo Version numbers updated.
echo.

echo [2/6] Running tests...
python run_tests.py --type unit
if errorlevel 1 (
    echo ERROR: Tests failed! Fix the issues before releasing.
    exit /b 1
)
echo.

echo [3/6] Building application...
python build.py --clean
if errorlevel 1 (
    echo ERROR: Build failed! Fix the issues before releasing.
    exit /b 1
)
echo.

echo [4/6] Committing changes...
git add setup.py installer.iss
git commit -m "Release v%NEW_VERSION%"
if errorlevel 1 (
    echo ERROR: Failed to commit changes!
    exit /b 1
)
echo.

echo [5/6] Creating git tag...
git tag -a v%NEW_VERSION% -m "Release version %NEW_VERSION%"
if errorlevel 1 (
    echo ERROR: Failed to create git tag!
    exit /b 1
)
echo.

echo [6/6] Pushing to GitHub...
git push origin main
git push origin v%NEW_VERSION%
if errorlevel 1 (
    echo ERROR: Failed to push to GitHub!
    exit /b 1
)
echo.

echo ========================================
echo Release v%NEW_VERSION% created successfully!
echo ========================================
echo.
echo Files to upload to GitHub Release:
echo - installer\GoogleMapsScraper_Setup_v%NEW_VERSION%.exe
echo.
echo Next steps:
echo 1. Go to: https://github.com/hoanganh-hue/lazala/releases
echo 2. Click "Draft a new release"
echo 3. Choose tag: v%NEW_VERSION%
echo 4. Upload the installer file
echo 5. Write release notes
echo 6. Publish release
echo.

pause
