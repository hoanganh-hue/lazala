#!/usr/bin/env python3
"""
Build script for Google Maps Scraper Desktop App
"""

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path


def clean_build():
    """Clean build directories"""
    print("🧹 Cleaning build directories...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"  Removed {dir_name}/")
    
    # Clean .pyc files
    for pyc_file in Path(".").rglob("*.pyc"):
        pyc_file.unlink()
    
    for pycache_dir in Path(".").rglob("__pycache__"):
        shutil.rmtree(pycache_dir)
    
    print("✅ Clean completed")


def install_dependencies():
    """Install dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    
    return True


def run_tests():
    """Run tests before building"""
    print("🧪 Running tests...")
    
    try:
        result = subprocess.run([
            sys.executable, "run_tests.py", "--type", "unit", "--verbose"
        ], check=True)
        print("✅ All tests passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed: {e}")
        return False


def build_executable():
    """Build executable using PyInstaller"""
    print("🔨 Building executable...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "PyInstaller", "build.spec"
        ], check=True)
        print("✅ Executable built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False


def create_installer():
    """Create installer using Inno Setup"""
    print("📦 Creating installer...")
    
    # Check if Inno Setup is available
    inno_compiler = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    if not Path(inno_compiler).exists():
        print("⚠️  Inno Setup not found. Skipping installer creation.")
        print("   Please install Inno Setup to create installer.")
        return True
    
    # Create installer script
    installer_script = """
[Setup]
AppName=Google Maps Scraper
AppVersion=1.0.0
AppPublisher=Google Maps Scraper Team
AppPublisherURL=https://github.com/yourusername/google-maps-scraper-app
AppSupportURL=https://github.com/yourusername/google-maps-scraper-app/issues
AppUpdatesURL=https://github.com/yourusername/google-maps-scraper-app/releases
DefaultDirName={autopf}\\GoogleMapsScraper
DefaultGroupName=Google Maps Scraper
AllowNoIcons=yes
LicenseFile=LICENSE
InfoBeforeFile=README.md
OutputDir=installer
OutputBaseFilename=GoogleMapsScraper_Setup_v1.0.0
SetupIconFile=resources\\icons\\app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "vietnamese"; MessagesFile: "compiler:Languages\\Vietnamese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
Source: "dist\\GoogleMapsScraper.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "docs\\*"; DestDir: "{app}\\docs"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\\Google Maps Scraper"; Filename: "{app}\\GoogleMapsScraper.exe"
Name: "{group}\\{cm:UninstallProgram,Google Maps Scraper}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\Google Maps Scraper"; Filename: "{app}\\GoogleMapsScraper.exe"; Tasks: desktopicon
Name: "{userappdata}\\Microsoft\\Internet Explorer\\Quick Launch\\Google Maps Scraper"; Filename: "{app}\\GoogleMapsScraper.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\\GoogleMapsScraper.exe"; Description: "{cm:LaunchProgram,Google Maps Scraper}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\\logs"
Type: filesandordirs; Name: "{app}\\cache"
"""
    
    # Write installer script
    installer_file = Path("installer.iss")
    with open(installer_file, 'w', encoding='utf-8') as f:
        f.write(installer_script)
    
    try:
        subprocess.run([inno_compiler, str(installer_file)], check=True)
        print("✅ Installer created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Installer creation failed: {e}")
        return False
    finally:
        # Clean up installer script
        if installer_file.exists():
            installer_file.unlink()


def main():
    """Main build function"""
    parser = argparse.ArgumentParser(description="Build Google Maps Scraper Desktop App")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean build directories before building"
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip running tests before building"
    )
    parser.add_argument(
        "--skip-installer",
        action="store_true",
        help="Skip creating installer"
    )
    parser.add_argument(
        "--dependencies",
        action="store_true",
        help="Install dependencies before building"
    )
    
    args = parser.parse_args()
    
    print("🚀 Google Maps Scraper - Build Script")
    print("=" * 50)
    
    # Clean if requested
    if args.clean:
        clean_build()
    
    # Install dependencies if requested
    if args.dependencies:
        if not install_dependencies():
            sys.exit(1)
    
    # Run tests unless skipped
    if not args.skip_tests:
        if not run_tests():
            print("❌ Build aborted due to test failures")
            sys.exit(1)
    
    # Build executable
    if not build_executable():
        print("❌ Build failed")
        sys.exit(1)
    
    # Create installer unless skipped
    if not args.skip_installer:
        create_installer()
    
    print("\n🎉 Build completed successfully!")
    print("📁 Executable location: dist/GoogleMapsScraper.exe")
    
    if not args.skip_installer:
        print("📦 Installer location: installer/GoogleMapsScraper_Setup_v1.0.0.exe")


if __name__ == "__main__":
    main()
