@echo off
title Prompt Manager - Setup

echo.
echo  ==========================================
echo   PROMPT MANAGER - SETUP
echo  ==========================================
echo.

:: ── 1. Verificar Python ──────────────────────────────────
echo  [1/5] Verificando Python...

:: Comprobar si Python 3.12 ya esta instalado en el sistema
python --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo  [OK] %%i encontrado en PATH
    goto :check_version
)

:: No esta en PATH, buscar instalador .exe en la carpeta del proyecto
echo  Python no encontrado en PATH. Buscando instalador local...

set INSTALLER=
for %%f in ("%~dp0python-*.exe") do set INSTALLER=%%f

if not "%INSTALLER%"=="" (
    echo  [OK] Instalador encontrado: %INSTALLER%
    echo  Instalando Python 3.12 en modo silencioso...
    "%INSTALLER%" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
    if errorlevel 1 (
        echo  ERROR: Fallo la instalacion de Python.
        echo  Intenta ejecutar el instalador manualmente: %INSTALLER%
        pause
        exit /b 1
    )
    echo  [OK] Python instalado correctamente
    :: Recargar PATH para que python sea accesible
    call refreshenv >nul 2>&1
    goto :check_version
)

:: No hay instalador local -> abrir web oficial y salir
echo.
echo  ERROR: No se encontro Python ni un instalador en la carpeta del proyecto.
echo.
echo  Abriendo la pagina oficial de descarga de Python 3.12...
start "" "https://www.python.org/downloads/release/python-31210/"
echo.
echo  Instrucciones:
echo    1. Descarga el archivo "Windows installer (64-bit)"
echo    2. Coloca el .exe en la misma carpeta que este setup.cmd
echo    3. Vuelve a ejecutar setup.cmd  (lo instalara automaticamente)
echo.
pause
exit /b 1

:check_version
:: Advertir si la version es 3.13 o superior
python -c "import sys; exit(0 if sys.version_info < (3,13) else 1)" >nul 2>&1
if errorlevel 1 (
    echo.
    echo  AVISO: La version de Python detectada es 3.13 o superior.
    echo  Se recomienda Python 3.12 para evitar errores de compilacion.
    echo  Puedes descargar Python 3.12 desde:
    echo    https://www.python.org/downloads/release/python-31210/
    echo.
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