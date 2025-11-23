@echo off
setlocal

rem 1) Buat virtual environment
if not exist .venv (
  python -m venv .venv
)
call .venv\Scripts\activate

rem 2) Upgrade pip dan install deps
python -m pip install --upgrade pip wheel
rem Catatan: torch akan terpasang CPU-only by default.
rem Jika ingin CUDA, install sesuai GPU Anda (lihat komentar di bawah).
pip install -r requirements.txt
pip install pyinstaller

rem 3) Pastikan weight YOLO ada
if not exist yolo11n.pt (
  echo.
  echo [ERROR] File yolo11n.pt tidak ditemukan di folder proyek.
  echo Letakkan yolo11n.pt di sini (satu folder dengan build_windows.bat) lalu jalankan ulang.
  exit /b 1
)

rem 4) Build dengan spec (reproducible)
pyinstaller --noconfirm --clean SmartTrafficCounter.spec

echo.
echo Build selesai. Jalankan:
echo   dist\SmartTrafficCounter\SmartTrafficCounter.exe
echo.

endlocal