"""
Punto de entrada principal de la aplicación
Sistema de Participación Estudiantil
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.utils.logger import setup_logging
from src.presentation.controllers.auth_controller_v2 import auth_controller_v2
from src.ui.login_window import LoginWindow
import logging

# Configurar logging
setup_logging()
logger = logging.getLogger(__name__)


def main():
    """Función principal de la aplicación"""
    try:
        logger.info("=" * 70)
        logger.info("Iniciando Sistema de Participación Estudiantil")
        logger.info("=" * 70)
        
        # usar auth_controller_v2
        auth_controller_v2.create_default_admin()
        
        # Iniciar ventana de login
        app = LoginWindow()
        app.mainloop()
        
        logger.info("Aplicación cerrada correctamente")
        
    except Exception as e:
        logger.critical(f"Error crítico en la aplicación: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()