# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent
src_dir = project_root / "src"
resources_dir = project_root / "resources"

# Collect all data files
datas = []

# Add resources directory
if resources_dir.exists():
    datas.append((str(resources_dir), "resources"))

# Add any additional data files
additional_datas = [
    ("README.md", "."),
    ("LICENSE", "."),
]

for src, dst in additional_datas:
    if Path(src).exists():
        datas.append((src, dst))

# Hidden imports (modules that PyInstaller might miss)
hiddenimports = [
    "PyQt5.QtCore",
    "PyQt5.QtGui", 
    "PyQt5.QtWidgets",
    "requests",
    "aiohttp",
    "pandas",
    "openpyxl",
    "json",
    "csv",
    "datetime",
    "pathlib",
    "configparser",
    "logging",
    "asyncio",
    "threading",
    "queue",
    "urllib3",
    "certifi",
    "charset_normalizer",
    "idna",
    "multidict",
    "yarl",
    "frozenlist",
    "aiosignal",
    "async_timeout",
    "typing_extensions",
    "attrs",
    "numpy",
    "pytz",
    "python_dateutil",
    "six",
    "et_xmlfile",
    "defusedxml",
    "openpyxl.workbook",
    "openpyxl.worksheet",
    "openpyxl.styles",
    "openpyxl.utils",
    "openpyxl.cell",
    "openpyxl.comments",
    "openpyxl.drawing",
    "openpyxl.chart",
    "openpyxl.packaging",
    "openpyxl.xml",
]

# Analysis
a = Analysis(
    [str(src_dir / "main.py")],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "matplotlib",
        "scipy",
        "PIL",
        "cv2",
        "sklearn",
        "tensorflow",
        "torch",
        "jupyter",
        "notebook",
        "IPython",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Remove duplicate binaries
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Create executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="GoogleMapsScraper",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI application
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(resources_dir / "icons" / "app_icon.ico") if (resources_dir / "icons" / "app_icon.ico").exists() else None,
    version_file=None,
)

# Optional: Create a directory distribution instead of single file
# Uncomment the following lines to create a directory distribution
# 
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name="GoogleMapsScraper"
# )
