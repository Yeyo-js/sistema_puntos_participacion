"""
Controller de Estudiantes V2 - REFACTORIZADO
Solo orquesta entre UI y servicios
"""
from src.core.services.student_service import StudentService
from src.infrastructure.database.repositories.student_repository import StudentRepository
from src.database.sqlite_manager import sqlite_manager
from src.shared.result import Result
import logging

logger = logging.getLogger(__name__)


class StudentControllerV2:
    """
    Controller V2 que orquesta gestión de estudiantes
    - NO tiene lógica de negocio
    - Solo coordina entre UI y servicios
    """
    
    def __init__(self):
        self._student_service = None
        self._session = None
    
    @property
    def student_service(self) -> StudentService:
        """Lazy loading del servicio"""
        if self._student_service is None:
            self._session = sqlite_manager.get_session()
            student_repo = StudentRepository(self._session)
            self._student_service = StudentService(student_repo)
        return self._student_service
    
    def get_all_students(self, clase_id: int = None) -> Result:
        """
        Obtener todos los estudiantes
        
        Uso:
            result = student_controller_v2.get_all_students()
            if result.is_success:
                students = result.data  # Lista de diccionarios
        """
        return self.student_service.get_all_students(clase_id)
    
    def get_student_by_id(self, student_id: int) -> Result:
        """Obtener un estudiante por ID"""
        return self.student_service.get_student_by_id(student_id)
    
    def create_student(self, full_name: str, list_number: int, section_id: int) -> Result:
        """
        Crear un nuevo estudiante
        
        Uso:
            result = student_controller_v2.create_student("Juan Pérez", 1, section_id)
            if result.is_success:
                student_id = result.data['id']
        """
        return self.student_service.create_student(full_name, list_number, section_id)
    
    def update_student(
        self, 
        student_id: int, 
        full_name: str = None, 
        list_number: int = None
    ) -> Result:
        """Actualizar un estudiante"""
        return self.student_service.update_student(student_id, full_name, list_number)
    
    def delete_student(self, student_id: int) -> Result:
        """Eliminar un estudiante"""
        return self.student_service.delete_student(student_id)
    
    def search_students(self, search_term: str, clase_id: int = None) -> Result:
        """Buscar estudiantes por nombre"""
        return self.student_service.search_students(search_term, clase_id)
    
    def get_next_list_number(self, clase_id: int) -> Result:
        """Obtener el siguiente número de lista disponible"""
        return self.student_service.get_next_list_number(clase_id)
    
    # ========== MÉTODO DE COMPATIBILIDAD ==========
    
    def create_sample_section(self) -> int:
        """
        Crear o obtener clase de ejemplo (compatibilidad con código viejo)
        Este método mantiene la compatibilidad con el código existente
        """
        from src.database.models import Usuario, Clase, Seccion, Nivel, Institucion
        
        session = sqlite_manager.get_session()
        
        try:
            # Buscar clase existente
            clase = session.query(Clase).first()
            
            if clase:
                return clase.id
            
            # Crear estructura si no existe
            usuario = session.query(Usuario).first()
            if not usuario:
                # Usar el admin creado por auth
                usuario = session.query(Usuario).filter_by(es_admin=True).first()
            
            institucion = session.query(Institucion).first()
            if not institucion:
                institucion = Institucion(
                    nombre="Institución de Ejemplo",
                    tipo="colegio"
                )
                session.add(institucion)
                session.flush()
            
            nivel = session.query(Nivel).first()
            if not nivel:
                nivel = Nivel(
                    institucion_id=institucion.id,
                    nombre="Primer Grado",
                    orden=1
                )
                session.add(nivel)
                session.flush()
            
            seccion = session.query(Seccion).first()
            if not seccion:
                seccion = Seccion(
                    nivel_id=nivel.id,
                    nombre="Sección A"
                )
                session.add(seccion)
                session.flush()
            
            nueva_clase = Clase(
                profesor_id=usuario.id,
                seccion_id=seccion.id,
                nombre="Clase General",
                anio_academico=2025,
                activa=True
            )
            session.add(nueva_clase)
            session.commit()
            
            logger.info(f"Clase de ejemplo creada: ID {nueva_clase.id}")
            return nueva_clase.id
        
        except Exception as e:
            logger.error(f"Error al crear clase de ejemplo: {e}")
            session.rollback()
            return None
        finally:
            session.close()


# Instancia global
student_controller_v2 = StudentControllerV2()
