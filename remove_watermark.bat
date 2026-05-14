@echo off
REM Veo Watermark Remover - Windows
REM Uso: remove_watermark.bat "mi_video.mp4"

SET INPUT=%~1
IF "%INPUT%"=="" (
    echo Uso: remove_watermark.bat "mi_video.mp4"
    pause
    exit /b 1
)

SET OUTPUT=%~dpn1_sin_marca%~x1

echo ==========================================
echo   Veo Watermark Remover
echo ==========================================
echo   Entrada:  %INPUT%
echo   Salida:   %OUTPUT%
echo   Esto puede tardar varios minutos...
echo ==========================================

ffmpeg -y -i "%INPUT%" -vf "delogo=x=2190:y=1308:w=355:h=118:show=0" -c:v libx264 -preset fast -crf 18 -c:a copy "%OUTPUT%"

IF %ERRORLEVEL% EQU 0 (
    echo.
    echo   Listo! Video guardado en: %OUTPUT%
) ELSE (
    echo.
    echo   Error. Asegurate de que FFmpeg este instalado.
    echo   Instalar: winget install ffmpeg
)

pause
