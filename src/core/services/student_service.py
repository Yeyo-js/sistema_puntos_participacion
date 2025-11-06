"""
Servicio de Estudiantes
Contiene SOLO lógica de negocio de estudiantes
"""
from src.shared.result import Result
from src.core.validators.student_validator import StudentValidator
from src.infrastructure.database.repositories.student_repository import StudentRepository
from src.database.models import Alumno
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class StudentService:
    """Servicio de lógica de negocio de estudiantes"""
    
    def __init__(self, student_repository: StudentRepository):
        self.student_repo = student_repository
        self.validator = StudentValidator()
    
    def get_all_students(self, clase_id: int = None) -> Result:
        """
        Obtener todos los estudiantes
        
        Returns:
            Result con lista de estudiantes
        """
        try:
            if clase_id:
                students = self.student_repo.get_by_section(clase_id)
            else:
                students = self.student_repo.get_all(active_only=True)
            
            # Convertir a diccionarios
            result_data = []
            for student in students:
                result_data.append({
                    'id': student.id,
                    'list_number': student.numero_lista,
                    'full_name': student.nombre,
                    'section_id': student.clase_id,
                    'section_name': student.clase.nombre if student.clase else 'Sin clase',
                    'is_active': student.activo
                })
            
            logger.info(f"Se obtuvieron {len(result_data)} estudiantes")
            return Result.success_result(result_data, f"Se encontraron {len(result_data)} estudiantes")
        
        except Exception as e:
            logger.error(f"Error al obtener estudiantes: {e}")
            return Result.failure("Error al obtener estudiantes")
    
    def get_student_by_id(self, student_id: int) -> Result:
        """Obtener un estudiante por ID"""
        try:
            student = self.student_repo.get_by_id(student_id)
            
            if not student:
                return Result.failure("Estudiante no encontrado")
            
            result_data = {
                'id': student.id,
                'list_number': student.numero_lista,
                'full_name': student.nombre,
                'section_id': student.clase_id,
                'is_active': student.activo
            }
            
            return Result.success_result(result_data)
        
        except Exception as e:
            logger.error(f"Error al obtener estudiante: {e}")
            return Result.failure("Error al obtener estudiante")
    
    def create_student(self, full_name: str, list_number: int, section_id: int) -> Result:
        """
        Crear un nuevo estudiante
        
        Returns:
            Result con ID del estudiante creado
        """
        try:
            # Validar datos
            validation = self.validator.validate_student_data(full_name, list_number)
            if validation.is_failure:
                return validation
            
            # Verificar número de lista duplicado
            if self.student_repo.exists_by_list_number(list_number, section_id):
                return Result.failure(
                    f"Ya existe un estudiante con el número de lista {list_number}",
                    error_code="DUPLICATE_LIST_NUMBER"
                )
            
            # Crear estudiante
            nuevo_estudiante = Alumno(
                nombre=full_name.strip(),
                numero_lista=list_number,
                clase_id=section_id,
                activo=True
            )
            
            created = self.student_repo.create(nuevo_estudiante)
            self.student_repo.commit()
            
            logger.info(f"Estudiante creado: {full_name} (ID: {created.id})")
            
            return Result.success_result(
                {'id': created.id},
                "Estudiante creado exitosamente"
            )
        
        except Exception as e:
            logger.error(f"Error al crear estudiante: {e}")
            self.student_repo.rollback()
            return Result.failure("Error al crear estudiante")
    
    def update_student(
        self, 
        student_id: int, 
        full_name: str = None, 
        list_number: int = None
    ) -> Result:
        """Actualizar un estudiante"""
        try:
            student = self.student_repo.get_by_id(student_id)
            
            if not student:
                return Result.failure("Estudiante no encontrado")
            
            # Validar nuevo nombre si se proporciona
            if full_name:
                validation = self.validator.validate_full_name(full_name)
                if validation.is_failure:
                    return validation
                student.nombre = full_name.strip()
            
            # Validar y verificar nuevo número de lista si se proporciona
            if list_number and list_number != student.numero_lista:
                validation = self.validator.validate_list_number(list_number)
                if validation.is_failure:
                    return validation
                
                if self.student_repo.exists_by_list_number(
                    list_number, 
                    student.clase_id, 
                    exclude_id=student_id
                ):
                    return Result.failure(
                        f"Ya existe un estudiante con el número de lista {list_number}"
                    )
                
                student.numero_lista = list_number
            
            self.student_repo.update(student)
            self.student_repo.commit()
            
            logger.info(f"Estudiante actualizado: ID {student_id}")
            return Result.success_result(message="Estudiante actualizado exitosamente")
        
        except Exception as e:
            logger.error(f"Error al actualizar estudiante: {e}")
            self.student_repo.rollback()
            return Result.failure("Error al actualizar estudiante")
    
    def delete_student(self, student_id: int) -> Result:
        """Eliminar un estudiante (soft delete)"""
        try:
            success = self.student_repo.delete(student_id, soft=True)
            
            if not success:
                return Result.failure("Estudiante no encontrado")
            
            self.student_repo.commit()
            
            logger.info(f"Estudiante eliminado: ID {student_id}")
            return Result.success_result(message="Estudiante eliminado exitosamente")
        
        except Exception as e:
            logger.error(f"Error al eliminar estudiante: {e}")
            self.student_repo.rollback()
            return Result.failure("Error al eliminar estudiante")
    
    def search_students(self, search_term: str, clase_id: int = None) -> Result:
        """Buscar estudiantes por nombre"""
        try:
            students = self.student_repo.search_by_name(search_term, clase_id)
            
            result_data = []
            for student in students:
                result_data.append({
                    'id': student.id,
                    'list_number': student.numero_lista,
                    'full_name': student.nombre,
                    'section_id': student.clase_id,
                    'section_name': student.clase.nombre if student.clase else 'Sin clase',
                    'is_active': student.activo
                })
            
            logger.info(f"Búsqueda '{search_term}': {len(result_data)} resultados")
            return Result.success_result(result_data)
        
        except Exception as e:
            logger.error(f"Error al buscar estudiantes: {e}")
            return Result.failure("Error al buscar estudiantes")
    
    def get_next_list_number(self, clase_id: int) -> Result:
        """Obtener el siguiente número de lista disponible"""
        try:
            next_number = self.student_repo.get_next_list_number(clase_id)
            return Result.success_result(next_number)
        except Exception as e:
            logger.error(f"Error al obtener siguiente número: {e}")
            return Result.failure("Error al obtener siguiente número de lista")
