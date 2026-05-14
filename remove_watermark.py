#!/usr/bin/env python3
"""
Veo Watermark Remover
---------------------
Elimina el logo "Veo" de la esquina inferior derecha de videos generados con Veo AI.
Compatible con Mac y Windows.

Uso:
    python3 remove_watermark.py "mi_video.mp4"
    python3 remove_watermark.py "mi_video.mp4" "mi_video_sin_marca.mp4"

Requisito: FFmpeg instalado en el sistema.
"""

import subprocess
import sys
import os
from pathlib import Path


# Coordenadas del logo Veo en videos 2560x1440
# Verificadas manualmente — esquina inferior derecha
DELOGO_FILTER = "delogo=x=2190:y=1308:w=355:h=118:show=0"


def check_ffmpeg():
    """Verifica que FFmpeg esté instalado."""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return True
    except FileNotFoundError:
        pass
    return False


def remove_watermark(input_path: str, output_path: str = None):
    """
    Elimina el logo Veo del video.

    Args:
        input_path: Ruta al video de entrada (.mp4)
        output_path: Ruta del video de salida (opcional)
    """
    if not check_ffmpeg():
        print("ERROR: FFmpeg no está instalado.")
        print("  Mac:     brew install ffmpeg")
        print("  Windows: winget install ffmpeg")
        sys.exit(1)

    input_file = Path(input_path)

    if not input_file.exists():
        print(f"ERROR: No se encontró el archivo: {input_path}")
        sys.exit(1)

    if output_path is None:
        output_path = str(input_file.parent / f"{input_file.stem}_sin_marca{input_file.suffix}")

    print("==========================================")
    print("  Veo Watermark Remover")
    print("==========================================")
    print(f"  Entrada:  {input_file.name}")
    print(f"  Salida:   {output_path}")
    print("  Esto puede tardar varios minutos...")
    print("==========================================\n")

    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_file),
        "-vf", DELOGO_FILTER,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "copy",
        output_path
    ]

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print(f"\n  Listo! Video guardado en:\n  {output_path}")
    else:
        print("\n  Error al procesar el video.")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:   python3 remove_watermark.py <video.mp4>")
        print("Ejemplo: python3 remove_watermark.py 'mi_video.mp4'")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    remove_watermark(input_file, output_file)
