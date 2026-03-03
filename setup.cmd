@echo off
title Prompt Manager - Setup

echo.
echo  ==========================================
echo   PROMPT MANAGER - SETUP
echo  ==========================================
echo.

:: ── 1. Verificar Python ──────────────────────────────────
echo  [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python no encontrado en PATH.
    echo  Instala Python 3.11 o 3.12 desde https://python.org
    echo  y marca "Add Python to PATH" durante la instalacion.
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo  [OK] %PYVER% detectado

:: Advertir si es Python 3.13 o superior
for /f "tokens=2 delims=." %%v in ('python -c "import sys; print(sys.version_info.minor)"') do set PYMINOR=%%v
python -c "import sys; exit(0 if sys.version_info < (3,13) else 1)" >nul 2>&1
if errorlevel 1 (
    echo.
    echo  AVISO: Tienes Python 3.13 o superior.
    echo  Se recomienda Python 3.11 o 3.12 para evitar errores de compilacion.
    echo  Continuar de todas formas? Pulsa cualquier tecla o cierra esta ventana.
    echo.
    pause
)

:: ── 2. Eliminar entorno viejo si existe ──────────────────
echo.
if exist ".venv" (
    echo  [2/5] Eliminando entorno virtual anterior...
    rmdir /s /q ".venv"
    echo  [OK] Entorno anterior eliminado
) else (
    echo  [2/5] Sin entorno previo, continuando...
)

:: ── 3. Crear entorno virtual nuevo ───────────────────────
echo.
echo  [3/5] Creando entorno virtual .venv ...
python -m venv .venv
if errorlevel 1 (
    echo  ERROR: No se pudo crear el entorno virtual.
    pause
    exit /b 1
)
echo  [OK] Entorno .venv creado

:: ── 4. Actualizar pip, setuptools y wheel ────────────────
echo.
echo  [4/5] Actualizando pip, setuptools y wheel...
call ".venv\Scripts\activate.bat"

".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 (
    echo  ERROR: No se pudo actualizar pip.
    pause
    exit /b 1
)
echo  [OK] pip actualizado

".venv\Scripts\python.exe" -m pip install --upgrade setuptools wheel
if errorlevel 1 (
    echo  ERROR: No se pudo actualizar setuptools/wheel.
    pause
    exit /b 1
)
echo  [OK] setuptools y wheel actualizados

:: ── 5. Instalar dependencias ──────────────────────────────
echo.
echo  [5/5] Instalando dependencias desde requirements.txt ...
if not exist "requirements.txt" (
    echo  ERROR: No se encontro requirements.txt
    echo  Asegurate de ejecutar este script desde la raiz del proyecto.
    pause
    exit /b 1
)

".venv\Scripts\pip.exe" install -r requirements.txt
if errorlevel 1 (
    echo.
    echo  ERROR: Fallo la instalacion de dependencias.
    echo  Revisa el mensaje de error arriba.
    pause
    exit /b 1
)

:: ── Resumen final ─────────────────────────────────────────
echo.
echo  ==========================================
echo   SETUP COMPLETADO CORRECTAMENTE
echo  ==========================================
echo.
echo  Ahora puedes lanzar la aplicacion con:
echo.
echo      start.cmd
echo.
pause
