"""
Sistema de logging para la aplicación
"""
import logging
import sys
from src.config.settings import LOG_LEVEL, LOG_FILE, LOG_FORMAT

# Colores para la consola
try:
    from colorlog import ColoredFormatter
    USE_COLOR = True
except ImportError:
    USE_COLOR = False


def setup_logging():
    """Configurar el sistema de logging"""
    
    # Crear logger raíz
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Limpiar handlers existentes
    root_logger.handlers.clear()
    
    # Handler para archivo
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    
    if USE_COLOR:
        console_formatter = ColoredFormatter(
            '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
    else:
        console_formatter = logging.Formatter(LOG_FORMAT)
    
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # Reducir verbosidad de SQLAlchemy
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    
    logging.info("Sistema de logging iniciado correctamente")


def get_logger(name):
    """Obtener un logger con un nombre específico"""
    return logging.getLogger(name)
