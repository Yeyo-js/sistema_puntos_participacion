"""
Repositorio Base con operaciones CRUD genéricas
Patrón Repository para abstraer acceso a datos
"""
from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.orm import Session
from src.database.models import Base
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T]):
    """Repositorio genérico con operaciones CRUD"""
    
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session
    
    def get_by_id(self, id: int) -> Optional[T]:
        """Obtener por ID"""
        try:
            return self.session.query(self.model).filter_by(id=id).first()
        except Exception as e:
            logger.error(f"Error al obtener {self.model.__name__} por ID {id}: {e}")
            return None
    
    def get_all(self, active_only: bool = True) -> List[T]:
        """Obtener todos los registros"""
        try:
            query = self.session.query(self.model)
            
            # Si el modelo tiene campo 'activo', filtrar
            if active_only and hasattr(self.model, 'activo'):
                query = query.filter_by(activo=True)
            
            return query.all()
        except Exception as e:
            logger.error(f"Error al obtener todos {self.model.__name__}: {e}")
            return []
    
    def create(self, entity: T) -> T:
        """Crear nuevo registro"""
        try:
            self.session.add(entity)
            self.session.flush()  # Para obtener el ID sin commit
            return entity
        except Exception as e:
            logger.error(f"Error al crear {self.model.__name__}: {e}")
            self.session.rollback()
            raise
    
    def update(self, entity: T) -> T:
        """Actualizar registro"""
        try:
            self.session.merge(entity)
            self.session.flush()
            return entity
        except Exception as e:
            logger.error(f"Error al actualizar {self.model.__name__}: {e}")
            self.session.rollback()
            raise
    
    def delete(self, id: int, soft: bool = True) -> bool:
        """Eliminar registro (soft delete por defecto)"""
        try:
            entity = self.get_by_id(id)
            if not entity:
                return False
            
            if soft and hasattr(entity, 'activo'):
                entity.activo = False
                self.session.flush()
            else:
                self.session.delete(entity)
                self.session.flush()
            
            return True
        except Exception as e:
            logger.error(f"Error al eliminar {self.model.__name__} ID {id}: {e}")
            self.session.rollback()
            raise
    
    def commit(self):
        """Confirmar transacción"""
        try:
            self.session.commit()
        except Exception as e:
            logger.error(f"Error en commit: {e}")
            self.session.rollback()
            raise
    
    def rollback(self):
        """Revertir transacción"""
        self.session.rollback()
