# Veo Watermark Remover

Elimina el logo **"Veo"** de la esquina inferior derecha de videos generados con [Veo AI](https://deepmind.google/technologies/veo/).

---

## Requisitos

- [FFmpeg](https://ffmpeg.org/) instalado en tu sistema
- Python 3 (incluido en Mac y en la mayoría de sistemas)

---

## Instalación rápida

### 1. Clonar el repositorio
```bash
git clone https://github.com/pleonoliva31/veo-watermark-remover.git
cd veo-watermark-remover
```

### 2. Instalar FFmpeg

**Mac:**
```bash
brew install ffmpeg
```

**Windows:**
```powershell
winget install ffmpeg
```

---

## Uso

### Interfaz gráfica (recomendado)

Abre una ventana donde puedes elegir el video y el destino con un explorador de archivos:

```bash
python3 remove_watermark_gui.py
```

En Windows:
```cmd
python remove_watermark_gui.py
```

### Línea de comandos

**Mac / Linux:**
```bash
python3 remove_watermark.py "mi_video.mp4"
```

**Windows:**
```cmd
python remove_watermark.py "mi_video.mp4"
```
O arrastra el archivo `.mp4` sobre `remove_watermark.bat`.

---

## ¿Usando Claude?

Si tienes Claude Desktop o Claude en Cowork, simplemente dile:

> "Lee el archivo CLAUDE.md de este repo y ayúdame a instalar y usar el programa"

Claude leerá la documentación y te guiará automáticamente en todo el proceso.

---

## Detalles técnicos

- Resolución soportada: **2560×1440**
- Filtro: `delogo` de FFmpeg
- Coordenadas del logo: `x=2190, y=1308, w=355, h=118`
- Calidad de salida: CRF 18 (alta calidad), preset fast

---

## Licencia

MIT
