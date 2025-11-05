"""
Sistema de manejo de errores amigable
Convierte errores técnicos en mensajes comprensibles para el usuario
"""
import logging
from functools import wraps
from typing import Callable, Any

logger = logging.getLogger(__name__)


class ErrorHandler:
    """Manejador de errores con mensajes amigables"""
    
    # Mapeo de errores comunes a mensajes amigables
    ERROR_MESSAGES = {
        # Errores de base de datos
        'UNIQUE constraint failed': 'Este registro ya existe en el sistema',
        'IntegrityError': 'Ya existe un registro con esos datos',
        'FOREIGN KEY constraint failed': 'No se puede eliminar porque tiene datos relacionados',
        'NOT NULL constraint failed': 'Falta información obligatoria',
        
        # Errores de conexión
        'Connection refused': 'No se puede conectar a la base de datos',
        'OperationalError': 'Error al acceder a la base de datos',
        'DatabaseError': 'Error en la base de datos',
        
        # Errores de autenticación
        'Invalid credentials': 'Usuario o contraseña incorrectos',
        'User not found': 'Usuario no encontrado',
        'Password mismatch': 'Las contraseñas no coinciden',
        
        # Errores de red
        'ConnectionError': 'Error de conexión. Verifica tu internet',
        'TimeoutError': 'La operación tardó demasiado. Intenta de nuevo',
        
        # Errores de archivo
        'FileNotFoundError': 'Archivo no encontrado',
        'PermissionError': 'No tienes permisos para esta operación',
        'IOError': 'Error al leer/escribir archivo',
        
        # Errores generales
        'ValueError': 'Valor incorrecto en los datos',
        'TypeError': 'Tipo de dato incorrecto',
        'KeyError': 'Falta información necesaria',
    }
    
    @staticmethod
    def get_friendly_message(error: Exception) -> str:
        """
        Convertir excepción técnica a mensaje amigable
        Args:
            error: Excepción capturada
        Returns:
            Mensaje amigable para el usuario
        """
        error_str = str(error)
        error_type = type(error).__name__
        
        # Buscar coincidencias en el mapeo
        for key, message in ErrorHandler.ERROR_MESSAGES.items():
            if key in error_str or key in error_type:
                return message
        
        # Casos especiales con detección más específica
        
        # Error de email duplicado
        if 'email' in error_str.lower() and 'unique' in error_str.lower():
            return 'Este correo electrónico ya está registrado'
        
        # Error de username duplicado
        if 'nombre' in error_str.lower() and 'unique' in error_str.lower():
            return 'Este nombre de usuario ya está registrado'
        
        # Error de lista vacía
        if 'empty' in error_str.lower() or 'no data' in error_str.lower():
            return 'No hay datos para mostrar'
        
        # Si no hay coincidencia, mensaje genérico
        logger.warning(f"Error no mapeado: {error_type} - {error_str}")
        return 'Ocurrió un error inesperado. Por favor, intenta de nuevo'
    
    @staticmethod
    def parse_database_error(error: Exception) -> str:
        """
        Parsear errores específicos de base de datos
        Args:
            error: Excepción de base de datos
        Returns:
            Mensaje amigable específico
        """
        error_str = str(error).lower()
        
        # Detectar tabla y campo del error
        if 'usuarios.email' in error_str:
            return 'Este correo electrónico ya está en uso'
        
        if 'usuarios.nombre' in error_str:
            return 'Este nombre de usuario ya está en uso'
        
        if 'estudiantes' in error_str and 'numero' in error_str:
            return 'Ya existe un estudiante con este número de lista'
        
        if 'clases' in error_str:
            return 'Ya existe una clase con ese nombre'
        
        return ErrorHandler.get_friendly_message(error)


def handle_errors(operation_name: str = "operación"):
    """
    Decorador para manejar errores de forma amigable
    
    Args:
        operation_name: Nombre de la operación para el mensaje
    
    Uso:
        @handle_errors("registro de usuario")
        def register_user(data):
            # código que puede fallar
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> tuple[bool, Any, str]:
            try:
                result = func(*args, **kwargs)
                
                # Si la función ya retorna tupla (success, data, message)
                if isinstance(result, tuple) and len(result) >= 2:
                    return result
                
                # Si retorna solo éxito/datos
                return True, result, "Operación exitosa"
                
            except Exception as e:
                # Log del error técnico (para debugging)
                logger.error(f"Error en {operation_name}: {type(e).__name__} - {str(e)}", exc_info=True)
                
                # Mensaje amigable para el usuario
                friendly_message = ErrorHandler.get_friendly_message(e)
                
                return False, None, friendly_message
        
        return wrapper
    return decorator


def safe_operation(func: Callable) -> Callable:
    """
    Decorador simple para operaciones que solo retornan (success, message)
    
    Uso:
        @safe_operation
        def delete_student(id):
            # código
            return True, "Estudiante eliminado"
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> tuple[bool, str]:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error en {func.__name__}: {str(e)}", exc_info=True)
            friendly_message = ErrorHandler.get_friendly_message(e)
            return False, friendly_message
    
    return wrapper


# Función auxiliar para validar y dar feedback específico
def validate_and_format_error(condition: bool, error_message: str) -> tuple[bool, str]:
    """
    Helper para validaciones con mensajes amigables
    
    Args:
        condition: Si es True, la validación pasó
        error_message: Mensaje a mostrar si falla
    
    Returns:
        (válido, mensaje)
    
    Ejemplo:
        valid, msg = validate_and_format_error(
            len(password) >= 6,
            "La contraseña debe tener al menos 6 caracteres"
        )
        if not valid:
            return False, msg
    """
    if not condition:
        return False, error_message
    return True, ""


# Función para logging de errores con contexto
def log_error_with_context(error: Exception, context: dict = None):
    """
    Log de error con contexto adicional para debugging
    
    Args:
        error: Excepción capturada
        context: Diccionario con información de contexto
    """
    context_str = ""
    if context:
        context_str = " | Contexto: " + ", ".join([f"{k}={v}" for k, v in context.items()])
    
    logger.error(f"Error: {type(error).__name__} - {str(error)}{context_str}", exc_info=True)
