"""
Excepciones personalizadas de la aplicación
"""


class AppException(Exception):
    """Excepción base de la aplicación"""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ValidationError(AppException):
    """Error de validación de datos"""
    pass


class AuthenticationError(AppException):
    """Error de autenticación"""
    pass


class PermissionError(AppException):
    """Error de permisos"""
    pass


class ResourceNotFoundError(AppException):
    """Recurso no encontrado"""
    pass


class DuplicateResourceError(AppException):
    """Recurso duplicado"""
    pass


class DatabaseError(AppException):
    """Error de base de datos"""
    pass
