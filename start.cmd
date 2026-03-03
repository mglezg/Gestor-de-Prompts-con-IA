@echo off
chcp 65001 >nul
title Prompt Manager

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║       🚀 PROMPT MANAGER - LAUNCHER       ║
echo  ╚══════════════════════════════════════════╝
echo.

:: Verificar que existe el entorno virtual
if not exist ".venv\Scripts\activate.bat" (
    echo  ❌ No se encontró el entorno virtual .venv
    echo  👉 Ejecuta primero: setup.cmd
    echo.
    pause
    exit /b 1
)

:: Activar entorno virtual
echo  ✔ Activando entorno virtual...
call .venv\Scripts\activate.bat

:: Verificar que existe run.py
if not exist "run.py" (
    echo  ❌ No se encontró run.py en este directorio
    echo  👉 Asegúrate de ejecutar este script desde la raíz del proyecto
    echo.
    pause
    exit /b 1
)

:: Esperar un momento y abrir el navegador en segundo plano
echo  ✔ Abriendo navegador en http://localhost:8000 ...
ping 127.0.0.1 -n 3 >nul
start "" "http://localhost:8000"

:: Lanzar el servidor
echo  ✔ Iniciando servidor...
echo.
echo  ─────────────────────────────────────────────
echo   URL:      http://localhost:8000
echo   API docs: http://localhost:8000/docs
echo   Detener:  Ctrl+C
echo  ─────────────────────────────────────────────
echo.

python run.py

echo.
echo  Servidor detenido.
pause
