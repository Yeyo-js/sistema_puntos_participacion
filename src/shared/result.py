"""
Patrón Result para manejo consistente de operaciones
Reemplaza las tuplas (bool, data, message)
"""
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar('T')


@dataclass
class Result(Generic[T]):
    """
    Resultado de una operación
    
    Ejemplo de uso:
        # Éxito
        return Result.success_result(data, "Operación exitosa")
        
        # Error
        return Result.failure("Mensaje de error")
    """
    success: bool
    data: Optional[T] = None
    message: str = ""
    error_code: Optional[str] = None
    
    @classmethod
    def success_result(cls, data: T = None, message: str = "Operación exitosa") -> 'Result[T]':
        """Crear resultado exitoso"""
        return cls(success=True, data=data, message=message)
    
    @classmethod
    def failure(cls, message: str, error_code: str = None) -> 'Result[T]':
        """Crear resultado fallido"""
        return cls(success=False, message=message, error_code=error_code)
    
    @property
    def is_success(self) -> bool:
        """Alias para success"""
        return self.success
    
    @property
    def is_failure(self) -> bool:
        """Verificar si falló"""
        return not self.success
    
    def unwrap(self) -> T:
        """
        Obtener data o lanzar excepción
        Úsalo solo cuando estés 100% seguro del éxito
        """
        if not self.success:
            raise ValueError(f"Intentando unwrap de Result fallido: {self.message}")
        return self.data
    
    def unwrap_or(self, default: T) -> T:
        """Obtener data o valor por defecto"""
        return self.data if self.success else default
