@echo off
REM Script to create a GitHub release for Google Maps Scraper
REM This will trigger GitHub Actions to build and upload the installer

setlocal enabledelayedexpansion

set VERSION=1.0.0
set TAG=v%VERSION%
set RELEASE_NAME=Google Maps Scraper v%VERSION%

echo ================================================
echo   Google Maps Scraper - Release Creator
echo ================================================
echo.
echo Version: %VERSION%
echo Tag: %TAG%
echo.

REM Check if tag exists
git rev-parse %TAG% >nul 2>&1
if %errorlevel% equ 0 (
    echo Error: Tag %TAG% already exists!
    echo.
    echo To recreate the tag, first delete it:
    echo   git tag -d %TAG%
    echo   git push origin :refs/tags/%TAG%
    echo.
    exit /b 1
)

REM Show current branch
for /f "tokens=*" %%i in ('git branch --show-current') do set CURRENT_BRANCH=%%i
echo Current branch: %CURRENT_BRANCH%
echo.

REM Confirm action
set /p CONFIRM="Do you want to create tag %TAG% and trigger the release? (Y/N) "
if /i not "%CONFIRM%"=="Y" (
    echo Cancelled.
    exit /b 0
)

echo.
echo Creating tag %TAG%...
git tag -a "%TAG%" -m "%RELEASE_NAME%"

echo Pushing tag to GitHub...
git push origin "%TAG%"

echo.
echo Success!
echo.
echo Next steps:
echo 1. Check GitHub Actions build: https://github.com/hoanganh-hue/lazala/actions
echo 2. Wait 5-10 minutes for build to complete
echo 3. Check release: https://github.com/hoanganh-hue/lazala/releases/tag/%TAG%
echo.
echo The installer will be automatically uploaded to:
echo https://github.com/hoanganh-hue/lazala/releases/download/%TAG%/GoogleMapsScraper_Setup_v%VERSION%.exe
echo.
pause
