"""
Controlador de autenticación de usuarios
"""
import bcrypt
from src.database.sqlite_manager import sqlite_manager
from src.database.models import Usuario
import logging

logger = logging.getLogger(__name__)


class AuthController:
    """Controlador para operaciones de autenticación"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Encriptar contraseña usando bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verificar si una contraseña coincide con el hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception as e:
            logger.error(f"Error al verificar contraseña: {e}")
            return False
    
    @staticmethod
    def login(email: str, password: str) -> tuple[bool, Usuario | None, str]:
        """
        Autenticar usuario
        Retorna: (éxito, usuario, mensaje)
        """
        session = sqlite_manager.get_session()
        
        try:
            # Buscar usuario por email
            usuario = session.query(Usuario).filter_by(email=email).first()
            
            if not usuario:
                return False, None, "Usuario no encontrado"
            
            if not usuario.activo:
                return False, None, "Usuario inactivo"
            
            # Verificar contraseña
            if not AuthController.verify_password(password, usuario.password_hash):
                return False, None, "Contraseña incorrecta"
            
            logger.info(f"Usuario autenticado exitosamente: {email}")
            return True, usuario, "Login exitoso"
        
        except Exception as e:
            logger.error(f"Error durante login: {e}")
            return False, None, f"Error: {str(e)}"
        
        finally:
            sqlite_manager.close_session(session)
    
    @staticmethod
    def register(nombre: str, email: str, password: str, es_admin: bool = False) -> tuple[bool, str]:
        """
        Registrar nuevo usuario
        Retorna: (éxito, mensaje)
        """
        session = sqlite_manager.get_session()
        
        try:
            # Verificar si el email ya existe
            usuario_existente = session.query(Usuario).filter_by(email=email).first()
            if usuario_existente:
                return False, "El email ya está registrado"
            
            # Crear nuevo usuario
            password_hash = AuthController.hash_password(password)
            nuevo_usuario = Usuario(
                nombre=nombre,
                email=email,
                password_hash=password_hash,
                es_admin=es_admin
            )
            
            session.add(nuevo_usuario)
            session.commit()
            
            logger.info(f"Usuario registrado exitosamente: {email}")
            return True, "Usuario registrado exitosamente"
        
        except Exception as e:
            session.rollback()
            logger.error(f"Error durante registro: {e}")
            return False, f"Error: {str(e)}"
        
        finally:
            sqlite_manager.close_session(session)
    
    @staticmethod
    def change_password(usuario_id: int, old_password: str, new_password: str) -> tuple[bool, str]:
        """
        Cambiar contraseña de usuario
        Retorna: (éxito, mensaje)
        """
        session = sqlite_manager.get_session()
        
        try:
            usuario = session.query(Usuario).filter_by(id=usuario_id).first()
            
            if not usuario:
                return False, "Usuario no encontrado"
            
            # Verificar contraseña antigua
            if not AuthController.verify_password(old_password, usuario.password_hash):
                return False, "Contraseña actual incorrecta"
            
            # Actualizar contraseña
            usuario.password_hash = AuthController.hash_password(new_password)
            session.commit()
            
            logger.info(f"Contraseña cambiada para usuario ID: {usuario_id}")
            return True, "Contraseña actualizada exitosamente"
        
        except Exception as e:
            session.rollback()
            logger.error(f"Error al cambiar contraseña: {e}")
            return False, f"Error: {str(e)}"
        
        finally:
            sqlite_manager.close_session(session)
    
    @staticmethod
    def create_default_admin():
        """Crear usuario admin por defecto si no existe"""
        session = sqlite_manager.get_session()
        
        try:
            # Verificar si ya existe un admin
            admin_existente = session.query(Usuario).filter_by(es_admin=True).first()
            
            if not admin_existente:
                # Crear admin por defecto
                password_hash = AuthController.hash_password("admin123")
                admin = Usuario(
                    nombre="Administrador",
                    email="admin@sistema.com",
                    password_hash=password_hash,
                    es_admin=True
                )
                session.add(admin)
                session.commit()
                logger.info("Usuario admin por defecto creado: admin@sistema.com / admin123")
                return True
            
            return False
        
        except Exception as e:
            session.rollback()
            logger.error(f"Error al crear admin por defecto: {e}")
            return False
        
        finally:
            sqlite_manager.close_session(session)


# Instancia global del controlador
auth_controller = AuthController()
