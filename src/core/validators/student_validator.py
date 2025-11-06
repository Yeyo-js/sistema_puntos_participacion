"""
Validador de Estudiantes
Contiene todas las reglas de validación para estudiantes
"""
from src.shared.result import Result


class StudentValidator:
    """Validador para operaciones de estudiantes"""
    
    # Constantes de validación
    MIN_NAME_LENGTH = 3
    MAX_NAME_LENGTH = 100
    MIN_LIST_NUMBER = 1
    MAX_LIST_NUMBER = 999
    
    @staticmethod
    def validate_full_name(nombre: str) -> Result:
        """Validar nombre completo del estudiante"""
        if not nombre or not nombre.strip():
            return Result.failure("El nombre completo es obligatorio")
        
        nombre = nombre.strip()
        
        if len(nombre) < StudentValidator.MIN_NAME_LENGTH:
            return Result.failure(
                f"El nombre debe tener al menos {StudentValidator.MIN_NAME_LENGTH} caracteres"
            )
        
        if len(nombre) > StudentValidator.MAX_NAME_LENGTH:
            return Result.failure(
                f"El nombre es demasiado largo (máximo {StudentValidator.MAX_NAME_LENGTH} caracteres)"
            )
        
        # Validar que contenga al menos 2 palabras (nombre y apellido)
        palabras = nombre.split()
        if len(palabras) < 2:
            return Result.failure("Ingresa el nombre completo (nombre y apellido)")
        
        return Result.success_result(message="Nombre válido")
    
    @staticmethod
    def validate_list_number(numero: int) -> Result:
        """Validar número de lista"""
        if numero < StudentValidator.MIN_LIST_NUMBER:
            return Result.failure(
                f"El número de lista debe ser al menos {StudentValidator.MIN_LIST_NUMBER}"
            )
        
        if numero > StudentValidator.MAX_LIST_NUMBER:
            return Result.failure(
                f"El número de lista es demasiado grande (máximo {StudentValidator.MAX_LIST_NUMBER})"
            )
        
        return Result.success_result(message="Número de lista válido")
    
    @staticmethod
    def validate_student_data(nombre: str, numero_lista: int) -> Result:
        """Validación completa de datos de estudiante"""
        # Validar nombre
        result = StudentValidator.validate_full_name(nombre)
        if result.is_failure:
            return result
        
        # Validar número de lista
        result = StudentValidator.validate_list_number(numero_lista)
        if result.is_failure:
            return result
        
        return Result.success_result(message="Todos los datos son válidos")
