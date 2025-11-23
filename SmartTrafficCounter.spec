# PyInstaller spec untuk Smart Traffic Counter (Tkinter)
# Mode: onedir (folder dist/SmartTrafficCounter)
# Menyertakan: yolo11n.pt dan seluruh data Ultralytics agar aman

import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Kumpulkan seluruh modul dan data ultralytics (cfg, assets, dll)
hiddenimports = collect_submodules("ultralytics")
datas = collect_data_files("ultralytics")

# Sertakan weight YOLO di root dist (berdampingan dengan exe)
proj_root = Path(".").resolve()
yolo_w = proj_root / "yolo11n.pt"
if yolo_w.exists():
    datas.append((str(yolo_w), "."))

block_cipher = None

a = Analysis(
    ['modern_vehicle_counter.py'],
    pathex=[str(proj_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SmartTrafficCounter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI app (tanpa console). Set True jika ingin log di console.
    icon=None,      # Ganti ke path ico jika punya, mis: 'assets/app.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SmartTrafficCounter'
)