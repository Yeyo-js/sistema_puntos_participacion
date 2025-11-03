@echo off
cls
echo ========================================
echo INSTALADOR AUTOMATICO
echo Sistema de Participacion Estudiantil
echo ========================================
echo.

REM Verificar Python
echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado.
    echo.
    echo Descarga Python desde: https://www.python.org/downloads/
    echo Durante la instalacion, marca "Add Python to PATH"
    echo.
    pause
    exit /b 1
)
echo [OK] Python encontrado
echo.

REM Crear entorno virtual
echo [2/4] Creando entorno virtual...
if exist "venv\" (
    echo [INFO] El entorno virtual ya existe, omitiendo...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual creado
)
echo.

REM Activar entorno virtual
echo [3/4] Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] No se pudo activar el entorno virtual
    pause
    exit /b 1
)
echo [OK] Entorno virtual activado
echo.

REM Instalar dependencias
echo [4/4] Instalando dependencias...
echo Esta operacion puede tardar 2-5 minutos...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo.
echo [OK] Dependencias instaladas correctamente
echo.

echo ========================================
echo INSTALACION COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo Para ejecutar la aplicacion:
echo 1. Doble clic en run.bat
echo    O
echo 2. En terminal: python src/main.py
echo.
echo Credenciales de login:
echo   Email: admin@sistema.com
echo   Password: admin123
echo.
pause
