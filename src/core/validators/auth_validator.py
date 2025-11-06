"""
Validador de Autenticación
Contiene todas las reglas de validación para auth
"""
import re
from src.shared.result import Result


class AuthValidator:
    """Validador para operaciones de autenticación"""
    
    # Constantes de validación
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 20
    MIN_PASSWORD_LENGTH = 6
    MAX_PASSWORD_LENGTH = 50
    PIN_LENGTH = 4
    
    # Patrón para username
    USERNAME_PATTERN = r'^[a-zA-Z0-9_]+$'
    
    # PINs débiles prohibidos
    WEAK_PINS = [
        '0000', '1111', '2222', '3333', '4444', 
        '5555', '6666', '7777', '8888', '9999', 
        '1234', '4321', '0123', '9876'
    ]
    
    @staticmethod
    def validate_username(username: str) -> Result:
        """Validar formato de nombre de usuario"""
        if not username or not username.strip():
            return Result.failure("El nombre de usuario es obligatorio")
        
        username = username.strip()
        
        if len(username) < AuthValidator.MIN_USERNAME_LENGTH:
            return Result.failure(
                f"El usuario debe tener al menos {AuthValidator.MIN_USERNAME_LENGTH} caracteres"
            )
        
        if len(username) > AuthValidator.MAX_USERNAME_LENGTH:
            return Result.failure(
                f"El usuario es demasiado largo (máximo {AuthValidator.MAX_USERNAME_LENGTH} caracteres)"
            )
        
        if not re.match(AuthValidator.USERNAME_PATTERN, username):
            return Result.failure(
                "El usuario solo puede contener letras, números y guiones bajos"
            )
        
        return Result.success_result(message="Usuario válido")
    
    @staticmethod
    def validate_password(password: str) -> Result:
        """Validar fortaleza de contraseña"""
        if not password:
            return Result.failure("La contraseña es obligatoria")
        
        if len(password) < AuthValidator.MIN_PASSWORD_LENGTH:
            return Result.failure(
                f"La contraseña debe tener al menos {AuthValidator.MIN_PASSWORD_LENGTH} caracteres"
            )
        
        if len(password) > AuthValidator.MAX_PASSWORD_LENGTH:
            return Result.failure(
                f"La contraseña es demasiado larga (máximo {AuthValidator.MAX_PASSWORD_LENGTH} caracteres)"
            )
        
        # Debe contener al menos una letra
        if not re.search(r'[a-zA-Z]', password):
            return Result.failure("La contraseña debe contener al menos una letra")
        
        # Debe contener al menos un número
        if not re.search(r'\d', password):
            return Result.failure("La contraseña debe contener al menos un número")
        
        return Result.success_result(message="Contraseña válida")
    
    @staticmethod
    def validate_pin(pin: str) -> Result:
        """Validar PIN de 4 dígitos"""
        if not pin:
            return Result.failure("El PIN es obligatorio")
        
        if len(pin) != AuthValidator.PIN_LENGTH:
            return Result.failure(f"El PIN debe tener {AuthValidator.PIN_LENGTH} dígitos")
        
        if not pin.isdigit():
            return Result.failure("El PIN solo debe contener números")
        
        if pin in AuthValidator.WEAK_PINS:
            return Result.failure("PIN demasiado débil, elige otro")
        
        return Result.success_result(message="PIN válido")
    
    @staticmethod
    def validate_full_name(nombre: str) -> Result:
        """Validar nombre completo"""
        if not nombre or not nombre.strip():
            return Result.failure("El nombre completo es obligatorio")
        
        nombre = nombre.strip()
        
        if len(nombre) < 3:
            return Result.failure("El nombre es demasiado corto")
        
        if len(nombre) > 100:
            return Result.failure("El nombre es demasiado largo")
        
        return Result.success_result(message="Nombre válido")
    
    @staticmethod
    def validate_passwords_match(password: str, confirm_password: str) -> Result:
        """Validar que las contraseñas coincidan"""
        if password != confirm_password:
            return Result.failure("Las contraseñas no coinciden")
        
        return Result.success_result(message="Las contraseñas coinciden")
    
    @staticmethod
    def validate_registration_data(
        nombre: str, 
        username: str, 
        password: str, 
        confirm_password: str
    ) -> Result:
        """Validación completa de datos de registro"""
        # Validar nombre
        result = AuthValidator.validate_full_name(nombre)
        if result.is_failure:
            return result
        
        # Validar username
        result = AuthValidator.validate_username(username)
        if result.is_failure:
            return result
        
        # Validar contraseña
        result = AuthValidator.validate_password(password)
        if result.is_failure:
            return result
        
        # Validar que coincidan
        result = AuthValidator.validate_passwords_match(password, confirm_password)
        if result.is_failure:
            return result
        
        return Result.success_result(message="Todos los datos son válidos")
