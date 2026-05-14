@echo off
REM Genera VeoWatermarkRemover.exe en la carpeta dist\
REM Requisito: pip install pyinstaller

echo Instalando PyInstaller...
pip install pyinstaller

echo Construyendo .exe...
python -m PyInstaller --windowed --onefile --name "VeoWatermarkRemover" remove_watermark_gui.py

echo.
echo Listo! El archivo esta en: dist\VeoWatermarkRemover.exe
pause
