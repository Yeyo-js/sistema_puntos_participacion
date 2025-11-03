"""
Configuración principal de la aplicación
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Directorios base
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = BASE_DIR / "exports"
LOGS_DIR = BASE_DIR / "logs"
ASSETS_DIR = BASE_DIR / "assets"

# Crear directorios si no existen
for directory in [DATA_DIR, EXPORTS_DIR, LOGS_DIR, ASSETS_DIR]:
    directory.mkdir(exist_ok=True)

# Configuración de la aplicación
APP_NAME = os.getenv("APP_NAME", "Sistema de Participación")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Configuración de SQLite (offline)
SQLITE_DB_PATH = DATA_DIR / os.getenv("SQLITE_DB_PATH", "local.db").split("/")[-1]

# Configuración de SQL Server (online)
SQL_SERVER_CONFIG = {
    "host": os.getenv("SQL_SERVER_HOST", "localhost"),
    "port": int(os.getenv("SQL_SERVER_PORT", "1433")),
    "database": os.getenv("SQL_SERVER_DATABASE", "sistema_participacion"),
    "user": os.getenv("SQL_SERVER_USER", "sa"),
    "password": os.getenv("SQL_SERVER_PASSWORD", ""),
}

# Configuración de sincronización
SYNC_INTERVAL = int(os.getenv("SYNC_INTERVAL", "300"))  # 5 minutos por defecto
AUTO_SYNC = os.getenv("AUTO_SYNC", "True").lower() == "true"

# Configuración de UI (CustomTkinter)
UI_THEME = "blue"
UI_MODE = "dark"  # "dark" o "light"
WINDOW_SIZE = "1200x700"
MIN_WINDOW_SIZE = (1000, 600)

# Configuración de logs
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"
LOG_FILE = LOGS_DIR / "app.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Colores de tema (CustomTkinter)
COLORS = {
    "primary": "#1f538d",
    "secondary": "#14375e",
    "success": "#2ecc71",
    "danger": "#e74c3c",
    "warning": "#f39c12",
    "info": "#3498db",
    "light": "#ecf0f1",
    "dark": "#2c3e50",
}