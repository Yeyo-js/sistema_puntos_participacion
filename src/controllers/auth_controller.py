"""
Controlador de autenticación MEJORADO con seguridad reforzada
"""
import bcrypt
from src.database.sqlite_manager import sqlite_manager
from src.database.models import Usuario
from src.utils.session_manager import session_manager
from src.utils.error_handler import ErrorHandler, log_error_with_context
import logging
import re
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class AuthController:
    """Controlador para operaciones de autenticación"""
    
    # Control de intentos fallidos
    failed_attempts = {}
    MAX_ATTEMPTS = 3
    BLOCK_TIME_SECONDS = 30
    
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
    def validate_password_strength(password: str) -> tuple:
        """Validar que la contraseña sea fuerte"""
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        
        if len(password) > 50:
            return False, "La contraseña es demasiado larga (máximo 50 caracteres)"
        
        if not re.search(r'[a-zA-Z]', password):
            return False, "La contraseña debe contener al menos una letra"
        
        if not re.search(r'\d', password):
            return False, "La contraseña debe contener al menos un número"
        
        return True, "Contraseña válida"
    
    @staticmethod
    def validate_username(username: str) -> tuple:
        """Validar formato de nombre de usuario"""
        if len(username) < 3:
            return False, "El usuario debe tener al menos 3 caracteres"
        
        if len(username) > 20:
            return False, "El usuario es demasiado largo (máximo 20 caracteres)"
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "El usuario solo puede contener letras, números y guiones bajos"
        
        return True, "Usuario válido"
    
    @staticmethod
    def validate_pin(pin: str) -> tuple:
        """Validar PIN de 4 dígitos"""
        if not pin or len(pin) != 4:
            return False, "El PIN debe tener 4 dígitos"
        
        if not pin.isdigit():
            return False, "El PIN solo debe contener números"
        
        weak_pins = ['0000', '1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888', '9999', '1234', '4321']
        if pin in weak_pins:
            return False, "PIN demasiado débil, elige otro"
        
        return True, "PIN válido"
    
    @staticmethod
    def is_blocked(username: str) -> tuple:
        """Verificar si un usuario está bloqueado"""
        if username not in AuthController.failed_attempts:
            return False, 0
        
        attempt_data = AuthController.failed_attempts[username]
        
        if attempt_data['blocked_until']:
            now = datetime.now()
            if now < attempt_data['blocked_until']:
                seconds_left = int((attempt_data['blocked_until'] - now).total_seconds())
                return True, seconds_left
            else:
                AuthController.failed_attempts[username] = {'count': 0, 'blocked_until': None}
                return False, 0
        
        return False, 0
    
    @staticmethod
    def record_failed_attempt(username: str):
        """Registrar intento fallido de login"""
        if username not in AuthController.failed_attempts:
            AuthController.failed_attempts[username] = {'count': 0, 'blocked_until': None}
        
        AuthController.failed_attempts[username]['count'] += 1
        
        if AuthController.failed_attempts[username]['count'] >= AuthController.MAX_ATTEMPTS:
            block_until = datetime.now() + timedelta(seconds=AuthController.BLOCK_TIME_SECONDS)
            AuthController.failed_attempts[username]['blocked_until'] = block_until
            logger.warning(f"Usuario bloqueado por {AuthController.BLOCK_TIME_SECONDS}s: {username}")
    
    @staticmethod
    def reset_failed_attempts(username: str):
        """Reiniciar contador de intentos fallidos"""
        if username in AuthController.failed_attempts:
            AuthController.failed_attempts[username] = {'count': 0, 'blocked_until': None}
    
    @staticmethod
    def login(username: str, password: str, remember_me: bool = False) -> tuple:
        """Autenticar usuario con nombre de usuario"""
        blocked, seconds_left = AuthController.is_blocked(username)
        if blocked:
            return False, None, f"⏳ Demasiados intentos fallidos. Espera {seconds_left} segundos"
        
        session = sqlite_manager.get_session()
        
        try:
            usuario = session.query(Usuario).filter(
                (Usuario.nombre == username) | (Usuario.email == username)
            ).first()
            
            if not usuario:
                AuthController.record_failed_attempt(username)
                return False, None, "❌ Usuario o contraseña incorrectos"
            
            if not usuario.activo:
                return False, None, "⚠️ Usuario inactivo"
            
            if not AuthController.verify_password(password, usuario.password_hash):
                AuthController.record_failed_attempt(username)
                attempts_left = AuthController.MAX_ATTEMPTS - AuthController.failed_attempts.get(username, {}).get('count', 0)
                return False, None, f"❌ Usuario o contraseña incorrectos ({attempts_left} intentos restantes)"
            
            AuthController.reset_failed_attempts(username)
            
            if remember_me:
                token = session_manager.generate_token()
                session_manager.save_session(username, token, remember_me=True)
            
            logger.info(f"Usuario autenticado exitosamente: {username}")
            return True, usuario, "✅ Login exitoso"
        
        except Exception as e:
            friendly_message = ErrorHandler.get_friendly_message(e)
            log_error_with_context(e, {'operacion': 'login', 'username': username})
            return False, None, f"❌ {friendly_message}"
        
        finally:
            sqlite_manager.close_session(session)
    
    @staticmethod
    def login_with_pin(pin: str) -> tuple:
        """Autenticar con PIN rápido"""
        try:
            result = session_manager.verify_pin(pin)
            
            if not result:
                return False, None, "❌ PIN incorrecto"
            
            username = result['username']
            
            session = sqlite_manager.get_session()
            usuario = session.query(Usuario).filter(
                (Usuario.nombre == username) | (Usuario.email == username)
            ).first()
            
            if not usuario:
                session_manager.clear_session()
                return False, None, "❌ Usuario no encontrado"
            
            if not usuario.activo:
                return False, None, "⚠️ Usuario inactivo"
            
            sqlite_manager.close_session(session)
            
            logger.info(f"Usuario autenticado con PIN: {username}")
            return True, usuario, "✅ Login exitoso"
            
        except Exception as e:
            friendly_message = ErrorHandler.get_friendly_message(e)
            log_error_with_context(e, {'operacion': 'login_pin'})
            return False, None, f"❌ {friendly_message}"
    
    @staticmethod
    def auto_login() -> tuple:
        """Intentar auto-login con sesión guardada"""
        try:
            session_data = session_manager.load_session()
            
            if not session_data:
                return False, None, "No hay sesión guardada"
            
            username = session_data['username']
            
            session = sqlite_manager.get_session()
            usuario = session.query(Usuario).filter(
                (Usuario.nombre == username) | (Usuario.email == username)
            ).first()
            
            if not usuario:
                session_manager.clear_session()
                return False, None, "Usuario no encontrado"
            
            if not usuario.activo:
                return False, None, "Usuario inactivo"
            
            sqlite_manager.close_session(session)
            
            logger.info(f"Auto-login exitoso: {username}")
            return True, usuario, "✅ Auto-login exitoso"
            
        except Exception as e:
            friendly_message = ErrorHandler.get_friendly_message(e)
            log_error_with_context(e, {'operacion': 'auto_login'})
            return False, None, f"❌ {friendly_message}"
    
    @staticmethod
    def register(nombre: str, username: str, password: str, es_admin: bool = False) -> tuple:
        """Registrar nuevo usuario con nombre de usuario"""
        session = sqlite_manager.get_session()
        
        try:
            valid_user, msg_user = AuthController.validate_username(username)
            if not valid_user:
                return False, f"❌ {msg_user}"
            
            valid_pass, msg_pass = AuthController.validate_password_strength(password)
            if not valid_pass:
                return False, f"❌ {msg_pass}"
            
            usuario_existente = session.query(Usuario).filter_by(nombre=username).first()
            
            if usuario_existente:
                return False, "❌ Este nombre de usuario ya está registrado"
            
            import random
            email = f"{username}@sistema.local"
            
            contador = 1
            while session.query(Usuario).filter_by(email=email).first():
                email = f"{username}{contador}@sistema.local"
                contador += 1
            
            password_hash = AuthController.hash_password(password)
            nuevo_usuario = Usuario(
                nombre=username,
                email=email,
                password_hash=password_hash,
                es_admin=es_admin
            )
            
            session.add(nuevo_usuario)
            session.commit()
            
            logger.info(f"Usuario registrado exitosamente: {username}")
            return True, "✅ Usuario registrado exitosamente"
        
        except Exception as e:
            session.rollback()
            friendly_message = ErrorHandler.get_friendly_message(e)
            log_error_with_context(e, {'operacion': 'registro', 'username': username})
            return False, f"❌ {friendly_message}"
        
        finally:
            sqlite_manager.close_session(session)
    
    @staticmethod
    def setup_pin(username: str, pin: str) -> tuple:
        """Configurar PIN para acceso rápido"""
        valid, msg = AuthController.validate_pin(pin)
        if not valid:
            return False, f"❌ {msg}"
        
        success = session_manager.update_pin(pin)
        
        if success:
            logger.info(f"PIN configurado para: {username}")
            return True, "✅ PIN configurado exitosamente"
        else:
            return False, "❌ Error al configurar PIN"
    
    @staticmethod
    def logout():
        """Cerrar sesión"""
        session_manager.clear_session()
        logger.info("Sesión cerrada")
    
    @staticmethod
    def create_default_admin():
        """Crear usuario admin por defecto si no existe"""
        session = sqlite_manager.get_session()
        
        try:
            admin_existente = session.query(Usuario).filter_by(es_admin=True).first()
            
            if not admin_existente:
                password_hash = AuthController.hash_password("admin123")
                admin = Usuario(
                    nombre="admin",
                    email="admin@sistema.com",
                    password_hash=password_hash,
                    es_admin=True
                )
                session.add(admin)
                session.commit()
                logger.info("Usuario admin por defecto creado: admin / admin123")
                return True
            
            return False
        
        except Exception as e:
            session.rollback()
            logger.error(f"Error al crear admin por defecto: {e}")
            return False
        
        finally:
            sqlite_manager.close_session(session)


auth_controller = AuthController()
