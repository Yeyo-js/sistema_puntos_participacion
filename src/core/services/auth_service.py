"""
Servicio de Autenticación
Contiene SOLO lógica de negocio de autenticación
"""
import bcrypt
from datetime import datetime, timedelta
from src.shared.result import Result
from src.core.validators.auth_validator import AuthValidator
from src.infrastructure.database.repositories.user_repository import UserRepository
from src.database.models import Usuario
import logging

logger = logging.getLogger(__name__)


class AuthService:
    """Servicio de lógica de negocio de autenticación"""
    
    # Control de intentos fallidos (en memoria)
    _failed_attempts = {}
    MAX_ATTEMPTS = 3
    BLOCK_TIME_SECONDS = 30
    
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository
        self.validator = AuthValidator()
    
    def login(self, username: str, password: str) -> Result:
        """
        Autenticar usuario
        
        Returns:
            Result con Usuario si éxito, mensaje de error si falla
        """
        try:
            # 1. Validar input básico
            if not username or not password:
                return Result.failure("Usuario y contraseña son obligatorios")
            
            username = username.strip()
            
            # 2. Verificar bloqueo
            is_blocked, seconds_left = self._is_blocked(username)
            if is_blocked:
                return Result.failure(
                    f"Demasiados intentos fallidos. Espera {seconds_left} segundos",
                    error_code="USER_BLOCKED"
                )
            
            # 3. Buscar usuario
            usuario = self.user_repo.get_by_username(username)
            
            if not usuario:
                self._record_failed_attempt(username)
                return Result.failure(
                    "Usuario o contraseña incorrectos",
                    error_code="INVALID_CREDENTIALS"
                )
            
            # 4. Verificar si está activo
            if not usuario.activo:
                return Result.failure(
                    "Usuario inactivo. Contacta al administrador",
                    error_code="USER_INACTIVE"
                )
            
            # 5. Verificar contraseña
            if not self._verify_password(password, usuario.password_hash):
                self._record_failed_attempt(username)
                attempts_left = self.MAX_ATTEMPTS - self._failed_attempts.get(username, {}).get('count', 0)
                return Result.failure(
                    f"Usuario o contraseña incorrectos ({attempts_left} intentos restantes)",
                    error_code="INVALID_CREDENTIALS"
                )
            
            # 6. Login exitoso
            self._reset_failed_attempts(username)
            
            logger.info(f"Login exitoso: {username}")
            return Result.success_result(usuario, "Login exitoso")
        
        except Exception as e:
            logger.error(f"Error en login: {e}")
            return Result.failure("Error durante autenticación")
    
    def register(
        self, 
        nombre: str, 
        username: str, 
        password: str, 
        confirm_password: str,
        es_admin: bool = False
    ) -> Result:
        """Registrar nuevo usuario"""
        try:
            # 1. Validar datos
            validation = self.validator.validate_registration_data(
                nombre, username, password, confirm_password
            )
            
            if validation.is_failure:
                return Result.failure(validation.message)
            
            # 2. Verificar username duplicado
            if self.user_repo.exists_by_username(username):
                return Result.failure(
                    "Este nombre de usuario ya está registrado",
                    error_code="DUPLICATE_USERNAME"
                )
            
            # 3. Generar email único
            email = self._generate_unique_email(username)
            
            # 4. Hash de contraseña
            password_hash = self._hash_password(password)
            
            # 5. Crear usuario
            nuevo_usuario = Usuario(
                nombre=username,
                email=email,
                password_hash=password_hash,
                es_admin=es_admin,
                activo=True
            )
            
            created = self.user_repo.create(nuevo_usuario)
            self.user_repo.commit()
            
            logger.info(f"Usuario registrado: {username}")
            return Result.success_result(created, "Usuario registrado exitosamente")
        
        except Exception as e:
            logger.error(f"Error en registro: {e}")
            self.user_repo.rollback()
            return Result.failure("Error durante el registro")
    
    def verify_pin(self, pin: str, expected_pin: str) -> Result:
        """Verificar PIN"""
        validation = self.validator.validate_pin(pin)
        
        if validation.is_failure:
            return validation
        
        if pin == expected_pin:
            return Result.success_result(True, "PIN correcto")
        
        return Result.failure("PIN incorrecto")
    
    def create_default_admin_if_needed(self) -> bool:
        """Crear admin por defecto si no existe ninguno"""
        try:
            admins = self.user_repo.get_admins()
            
            if not admins:
                password_hash = self._hash_password("admin123")
                self.user_repo.create_default_admin(password_hash)
                self.user_repo.commit()
                logger.info("Admin por defecto creado: admin / admin123")
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error al crear admin: {e}")
            return False
    
    # ========== MÉTODOS PRIVADOS ==========
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """Hashear contraseña con bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def _verify_password(password: str, password_hash: str) -> bool:
        """Verificar contraseña contra hash"""
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'), 
                password_hash.encode('utf-8')
            )
        except Exception as e:
            logger.error(f"Error al verificar password: {e}")
            return False
    
    def _generate_unique_email(self, username: str) -> str:
        """Generar email único basado en username"""
        email = f"{username}@sistema.local"
        contador = 1
        
        while self.user_repo.exists_by_email(email):
            email = f"{username}{contador}@sistema.local"
            contador += 1
        
        return email
    
    def _is_blocked(self, username: str) -> tuple:
        """Verificar si usuario está bloqueado"""
        if username not in self._failed_attempts:
            return False, 0
        
        attempt_data = self._failed_attempts[username]
        
        if attempt_data.get('blocked_until'):
            now = datetime.now()
            blocked_until = attempt_data['blocked_until']
            
            if now < blocked_until:
                seconds_left = int((blocked_until - now).total_seconds())
                return True, seconds_left
            else:
                self._reset_failed_attempts(username)
                return False, 0
        
        return False, 0
    
    def _record_failed_attempt(self, username: str):
        """Registrar intento fallido"""
        if username not in self._failed_attempts:
            self._failed_attempts[username] = {'count': 0, 'blocked_until': None}
        
        self._failed_attempts[username]['count'] += 1
        
        if self._failed_attempts[username]['count'] >= self.MAX_ATTEMPTS:
            block_until = datetime.now() + timedelta(seconds=self.BLOCK_TIME_SECONDS)
            self._failed_attempts[username]['blocked_until'] = block_until
            logger.warning(f"Usuario bloqueado: {username}")
    
    def _reset_failed_attempts(self, username: str):
        """Resetear intentos fallidos"""
        if username in self._failed_attempts:
            self._failed_attempts[username] = {'count': 0, 'blocked_until': None}
