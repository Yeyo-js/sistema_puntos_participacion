"""
Repositorio para operaciones de Estudiantes
Extiende BaseRepository con métodos específicos
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from src.database.models import Alumno
from src.infrastructure.database.repositories.base_repository import BaseRepository
import logging

logger = logging.getLogger(__name__)


class StudentRepository(BaseRepository[Alumno]):
    """Repositorio especializado para Estudiantes"""
    
    def __init__(self, session: Session):
        super().__init__(Alumno, session)
    
    def get_by_list_number(self, list_number: int, clase_id: int) -> Optional[Alumno]:
        """Obtener estudiante por número de lista en una clase"""
        try:
            return self.session.query(Alumno).filter_by(
                numero_lista=list_number,
                clase_id=clase_id,
                activo=True
            ).first()
        except Exception as e:
            logger.error(f"Error al buscar estudiante por número {list_number}: {e}")
            return None
    
    def search_by_name(self, search_term: str, clase_id: int = None) -> List[Alumno]:
        """Buscar estudiantes por nombre"""
        try:
            query = self.session.query(Alumno).filter(
                Alumno.activo == True,
                Alumno.nombre.ilike(f'%{search_term}%')
            )
            
            if clase_id:
                query = query.filter_by(clase_id=clase_id)
            
            return query.order_by(Alumno.numero_lista).all()
        except Exception as e:
            logger.error(f"Error al buscar estudiantes: {e}")
            return []
    
    def get_by_section(self, clase_id: int) -> List[Alumno]:
        """Obtener todos los estudiantes de una sección"""
        try:
            return self.session.query(Alumno).filter_by(
                clase_id=clase_id,
                activo=True
            ).order_by(Alumno.numero_lista).all()
        except Exception as e:
            logger.error(f"Error al obtener estudiantes de la sección: {e}")
            return []
    
    def exists_by_list_number(self, list_number: int, clase_id: int, exclude_id: int = None) -> bool:
        """Verificar si ya existe un estudiante con ese número de lista"""
        try:
            query = self.session.query(Alumno).filter_by(
                numero_lista=list_number,
                clase_id=clase_id,
                activo=True
            )
            
            if exclude_id:
                query = query.filter(Alumno.id != exclude_id)
            
            return query.first() is not None
        except Exception as e:
            logger.error(f"Error al verificar número de lista: {e}")
            return False
    
    def get_next_list_number(self, clase_id: int) -> int:
        """Obtener el siguiente número de lista disponible"""
        try:
            from sqlalchemy import func
            max_number = self.session.query(
                func.max(Alumno.numero_lista)
            ).filter_by(clase_id=clase_id, activo=True).scalar()
            
            return (max_number or 0) + 1
        except Exception as e:
            logger.error(f"Error al obtener siguiente número de lista: {e}")
            return 1
    
    def bulk_create(self, students: List[Alumno]) -> int:
        """Crear múltiples estudiantes en una transacción"""
        try:
            self.session.bulk_save_objects(students)
            self.session.flush()
            return len(students)
        except Exception as e:
            logger.error(f"Error en bulk create: {e}")
            self.session.rollback()
            raise
    
    def count_by_section(self, clase_id: int) -> int:
        """Contar estudiantes activos en una sección"""
        try:
            return self.session.query(Alumno).filter_by(
                clase_id=clase_id,
                activo=True
            ).count()
        except Exception as e:
            logger.error(f"Error al contar estudiantes: {e}")
            return 0
