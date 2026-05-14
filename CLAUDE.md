# Instrucciones para Claude — Veo Watermark Remover

Este documento está escrito para que Claude lo lea y pueda instalar y usar el programa de forma autónoma en cualquier computador, guiando al usuario paso a paso.

---

## ¿Qué hace este programa?

Elimina el logo **"Veo"** (marca de agua de Veo AI) de la esquina inferior derecha de videos generados con esa plataforma. Usa FFmpeg con el filtro `delogo` para reconstruir el área del logo con el contenido circundante.

- **Resolución de video soportada:** 2560×1440
- **Posición del logo:** esquina inferior derecha
- **Coordenadas verificadas:** x=2190, y=1308, w=355, h=118
- **Formato de entrada/salida:** MP4

---

## Lo que Claude debe hacer al leer este documento

Al recibir instrucciones del usuario para usar este programa, Claude debe:

1. Detectar el sistema operativo del usuario
2. Verificar si FFmpeg está instalado
3. Instalar FFmpeg si hace falta
4. Ejecutar el programa con el archivo de video indicado
5. Confirmar que el resultado se guardó correctamente

---

## Paso 1 — Detectar el sistema operativo

- **Mac:** preguntar si usan Terminal y si tienen Homebrew
- **Windows:** usar PowerShell o Command Prompt

Para verificar si FFmpeg está instalado, ejecutar:
```
ffmpeg -version
```
Si el comando no se reconoce, hay que instalarlo.

---

## Paso 2 — Instalar FFmpeg (si no está instalado)

### En Mac
```bash
# Opción 1: Con Homebrew (recomendado)
brew install ffmpeg

# Opción 2: Si no tienen Homebrew, instalarlo primero
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install ffmpeg
```

### En Windows
```powershell
# Opción 1: Con winget (Windows 11 / Windows 10 actualizado)
winget install ffmpeg

# Opción 2: Con Chocolatey
choco install ffmpeg

# Opción 3: Manual
# Ir a https://ffmpeg.org/download.html → Windows builds
# Descargar, descomprimir y agregar la carpeta /bin al PATH del sistema
```

Después de instalar, verificar con:
```
ffmpeg -version
```

---

## Paso 3 — Clonar o descargar el repositorio

```bash
git clone https://github.com/pleonoliva31/veo-watermark-remover.git
cd veo-watermark-remover
```

O descargar el ZIP desde GitHub → Code → Download ZIP, y descomprimir.

---

## Paso 4 — Usar el programa

### Opción A — Interfaz gráfica (recomendado para usuarios no técnicos)

Abre una ventana donde el usuario elige el video de entrada y el destino con explorador de archivos:

**Mac / Linux:**
```bash
python3 remove_watermark_gui.py
```

**Windows:**
```cmd
python remove_watermark_gui.py
```

### Opción B — Línea de comandos

**Mac o Linux:**
```bash
python3 remove_watermark.py "ruta/al/video.mp4"
```

Ejemplo:
```bash
python3 remove_watermark.py "/Users/pablo/Downloads/mi_video.mp4"
```

**Windows (opción 1 — Python):**
```cmd
python remove_watermark.py "C:\Users\pablo\Downloads\mi_video.mp4"
```

**Windows (opción 2 — doble clic o cmd):**
Arrastrar el archivo .mp4 sobre `remove_watermark.bat`, o ejecutar:
```cmd
remove_watermark.bat "C:\Users\pablo\Downloads\mi_video.mp4"
```

---

## Paso 5 — Resultado

El video procesado se guarda automáticamente en la misma carpeta del video original, con el sufijo `_sin_marca`:

```
mi_video.mp4           ← original (no se modifica)
mi_video_sin_marca.mp4 ← resultado sin marca de agua
```

---

## Comandos directos con FFmpeg (sin Python)

Si el usuario prefiere usar FFmpeg directamente:

```bash
ffmpeg -y \
  -i "video_original.mp4" \
  -vf "delogo=x=2190:y=1308:w=355:h=118:show=0" \
  -c:v libx264 -preset fast -crf 18 \
  -c:a copy \
  "video_sin_marca.mp4"
```

---

## Tiempos de procesamiento estimados

| Duración del video | Tiempo estimado (Mac M1/M2) | Tiempo estimado (Windows i7) |
|---|---|---|
| 1 minuto | ~1 min | ~2-3 min |
| 5 minutos | ~5 min | ~10-15 min |
| 17 minutos | ~12 min | ~25-35 min |

---

## Errores comunes y soluciones

| Error | Causa | Solución |
|---|---|---|
| `ffmpeg: command not found` | FFmpeg no instalado | Instalar con brew o winget |
| `No such file or directory` | Ruta del video incorrecta | Verificar la ruta exacta del archivo |
| `Invalid argument` (delogo) | Coordenadas fuera del borde del video | Reducir w o h para no sobrepasar los límites |
| Video de salida con artefactos | Área de delogo muy pequeña | Ajustar coordenadas para cubrir todo el logo |

---

## Notas técnicas

- El filtro `delogo` de FFmpeg reconstruye la zona tapada usando los píxeles circundantes. No es perfecto pero es invisible en la mayoría de los casos.
- Se usa `-crf 18` (calidad alta) con `-preset fast` para equilibrar velocidad y calidad.
- El audio se copia sin recodificar (`-c:a copy`) para no perder calidad.
- Si el video tiene una resolución distinta a 2560×1440, las coordenadas deben ajustarse proporcionalmente.

---

## Estructura del repositorio

```
veo-watermark-remover/
├── CLAUDE.md                  ← Este archivo (instrucciones para Claude)
├── README.md                  ← Instrucciones para humanos
├── remove_watermark_gui.py    ← Interfaz gráfica (recomendado)
├── remove_watermark.py        ← Script de línea de comandos (Mac + Windows)
└── remove_watermark.bat       ← Script para Windows (doble clic)
```
