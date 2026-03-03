@echo off
chcp 65001 >nul
title Prompt Manager - Setup

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║      ⚙  PROMPT MANAGER - SETUP          ║
echo  ╚══════════════════════════════════════════╝
echo.

:: ── 1. Verificar Python ──────────────────────────────────
echo  [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo  ❌ Python no encontrado en PATH.
    echo  👉 Instala Python 3.11 o 3.12 desde https://python.org
    echo     y marca "Add Python to PATH" durante la instalación.
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYVER=%%i
echo  ✔ %PYVER% detectado

:: ── 2. Eliminar entorno viejo si existe ──────────────────
if exist ".venv" (
    echo.
    echo  [2/5] Eliminando entorno virtual anterior...
    rmdir /s /q .venv
    echo  ✔ Entorno anterior eliminado
) else (
    echo.
    echo  [2/5] No hay entorno previo, continuando...
)

:: ── 3. Crear entorno virtual nuevo ───────────────────────
echo.
echo  [3/5] Creando entorno virtual .venv ...
python -m venv .venv
if errorlevel 1 (
    echo  ❌ Error al crear el entorno virtual.
    pause
    exit /b 1
)
echo  ✔ Entorno .venv creado

:: ── 4. Actualizar pip, setuptools y wheel ────────────────
echo.
echo  [4/5] Actualizando pip, setuptools y wheel dentro del entorno...
call .venv\Scripts\activate.bat

python -m pip install --upgrade pip
if errorlevel 1 (
    echo  ❌ Error al actualizar pip
    pause
    exit /b 1
)
echo  ✔ pip actualizado

python -m pip install --upgrade setuptools wheel
if errorlevel 1 (
    echo  ❌ Error al actualizar setuptools/wheel
    pause
    exit /b 1
)
echo  ✔ setuptools y wheel actualizados

:: ── 5. Instalar dependencias ──────────────────────────────
echo.
echo  [5/5] Instalando dependencias desde requirements.txt ...
if not exist "requirements.txt" (
    echo  ❌ No se encontró requirements.txt
    echo  👉 Asegúrate de ejecutar este script desde la raíz del proyecto
    pause
    exit /b 1
)

pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo  ❌ Error al instalar dependencias.
    echo  👉 Revisa el mensaje de error arriba.
    pause
    exit /b 1
)

:: ── Resumen final ─────────────────────────────────────────
echo.
echo  ╔══════════════════════════════════════════╗
echo  ║         ✅  SETUP COMPLETADO             ║
echo  ╚══════════════════════════════════════════╝
echo.
echo  Ya puedes lanzar la aplicación con:
echo.
echo      start.cmd
echo.
pause
