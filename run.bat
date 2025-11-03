@echo off
echo ========================================
echo Sistema de Participacion Estudiantil
echo ========================================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\" (
    echo [ERROR] No se encontro el entorno virtual.
    echo Por favor ejecuta: python -m venv venv
    echo.
    pause
    exit /b 1
)

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Ejecutar la aplicacion
echo Iniciando aplicacion...
echo.
python src/main.py

REM Si hay error
if errorlevel 1 (
    echo.
    echo [ERROR] Hubo un problema al ejecutar la aplicacion.
    echo Verifica que hayas instalado las dependencias: pip install -r requirements.txt
    pause
)
