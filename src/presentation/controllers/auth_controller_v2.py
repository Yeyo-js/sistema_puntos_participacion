"""
Controller de Autenticación V2 - REFACTORIZADO
Solo orquesta entre UI y servicios - NO tiene lógica de negocio
"""
from src.core.services.auth_service import AuthService
from src.infrastructure.database.repositories.user_repository import UserRepository
from src.database.sqlite_manager import sqlite_manager
from src.shared.result import Result
import logging

logger = logging.getLogger(__name__)


class AuthControllerV2:
    """
    Controller V2 que orquesta autenticación
    - NO tiene lógica de negocio
    - Solo coordina entre UI y servicios
    """
    
    def __init__(self):
        self._auth_service = None
        self._session = None
    
    @property
    def auth_service(self) -> AuthService:
        """Lazy loading del servicio"""
        if self._auth_service is None:
            self._session = sqlite_manager.get_session()
            user_repo = UserRepository(self._session)
            self._auth_service = AuthService(user_repo)
        return self._auth_service
    
    def login(self, username: str, password: str) -> Result:
        """
        Manejar login desde UI
        
        Uso:
            result = auth_controller_v2.login(username, password)
            
            if result.is_success:
                usuario = result.data
                # Abrir ventana principal
            else:
                # Mostrar error: result.message
        """
        return self.auth_service.login(username, password)
    
    def register(
        self, 
        nombre: str, 
        username: str, 
        password: str, 
        confirm_password: str
    ) -> Result:
        """
        Manejar registro desde UI
        
        Uso:
            result = auth_controller_v2.register(nombre, user, pass, confirm)
            
            if result.is_success:
                # Mostrar éxito
            else:
                # Mostrar error: result.message
        """
        return self.auth_service.register(
            nombre, username, password, confirm_password
        )
    
    def verify_pin(self, pin: str, expected_pin: str) -> Result:
        """Verificar PIN desde UI"""
        return self.auth_service.verify_pin(pin, expected_pin)
    
    def create_default_admin(self) -> bool:
        """Crear admin por defecto (llamar al inicio)"""
        return self.auth_service.create_default_admin_if_needed()


# Instancia global
auth_controller_v2 = AuthControllerV2()
