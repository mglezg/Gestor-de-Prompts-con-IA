@echo off
title Prompt Manager

echo.
echo  ==========================================
echo   PROMPT MANAGER - LAUNCHER
echo  ==========================================
echo.

:: Verificar que existe el entorno virtual
if not exist ".venv\Scripts\activate.bat" (
    echo  ERROR: No se encontro el entorno virtual .venv
    echo  Ejecuta primero: setup.cmd
    echo.
    pause
    exit /b 1
)

:: Activar entorno virtual
echo  [OK] Activando entorno virtual...
call ".venv\Scripts\activate.bat"

:: Verificar dependencias instaladas
if not exist ".venv\Scripts\uvicorn.exe" (
    echo  ERROR: Dependencias no instaladas en el entorno virtual.
    echo  Ejecuta setup.cmd para instalarlas.
    echo.
    pause
    exit /b 1
)

:: Verificar que existe run.py
if not exist "run.py" (
    echo  ERROR: No se encontro run.py
    echo  Asegurate de ejecutar este script desde la raiz del proyecto.
    echo.
    pause
    exit /b 1
)

:: Abrir navegador en segundo plano tras breve espera
echo  [OK] Abriendo navegador en http://localhost:8000 ...
start "" cmd /c "ping 127.0.0.1 -n 3 >nul && start http://localhost:8000"

:: Lanzar servidor
echo  [OK] Iniciando servidor...
echo.
echo  ------------------------------------------
echo   URL:      http://localhost:8000
echo   API docs: http://localhost:8000/docs
echo   Detener:  Ctrl+C
echo  ------------------------------------------
echo.

python run.py

echo.
echo  Servidor detenido.
pause
