"""
Repositorio de Usuarios
Maneja SOLO el acceso a datos de usuarios
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from src.database.models import Usuario
from src.infrastructure.database.repositories.base_repository import BaseRepository
import logging

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository[Usuario]):
    """Repositorio especializado para Usuarios"""
    
    def __init__(self, session: Session):
        super().__init__(Usuario, session)
    
    def get_by_username(self, username: str) -> Optional[Usuario]:
        """Obtener usuario por nombre de usuario"""
        try:
            return self.session.query(Usuario).filter(
                (Usuario.nombre == username) | (Usuario.email == username)
            ).first()
        except Exception as e:
            logger.error(f"Error al buscar usuario {username}: {e}")
            return None
    
    def get_by_email(self, email: str) -> Optional[Usuario]:
        """Obtener usuario por email"""
        try:
            return self.session.query(Usuario).filter_by(email=email).first()
        except Exception as e:
            logger.error(f"Error al buscar email {email}: {e}")
            return None
    
    def exists_by_username(self, username: str) -> bool:
        """Verificar si existe un username"""
        return self.get_by_username(username) is not None
    
    def exists_by_email(self, email: str) -> bool:
        """Verificar si existe un email"""
        return self.get_by_email(email) is not None
    
    def get_admins(self) -> List[Usuario]:
        """Obtener todos los administradores"""
        try:
            return self.session.query(Usuario).filter_by(
                es_admin=True,
                activo=True
            ).all()
        except Exception as e:
            logger.error(f"Error al obtener admins: {e}")
            return []
    
    def create_default_admin(self, password_hash: str) -> Usuario:
        """Crear usuario admin por defecto"""
        try:
            admin = Usuario(
                nombre="admin",
                email="admin@sistema.com",
                password_hash=password_hash,
                es_admin=True,
                activo=True
            )
            return self.create(admin)
        except Exception as e:
            logger.error(f"Error al crear admin: {e}")
            raise
