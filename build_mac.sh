#!/bin/bash
# Genera VeoWatermarkRemover.app en la carpeta dist/
# Requisito: pip3 install pyinstaller

set -e
echo "Instalando PyInstaller..."
pip3 install pyinstaller

echo "Construyendo .app..."
python3 -m PyInstaller --windowed --name "VeoWatermarkRemover" remove_watermark_gui.py

echo ""
echo "Listo! El archivo está en: dist/VeoWatermarkRemover.app"
echo "Cópialo a /Applications o compártelo como ZIP."
