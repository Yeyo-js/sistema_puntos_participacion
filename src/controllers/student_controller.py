"""
Controlador de Estudiantes
Maneja toda la lógica de negocio para el CRUD de estudiantes
"""
from src.database.sqlite_manager import SQLiteManager
from src.database.models import Alumno, Clase
from sqlalchemy import or_
import logging

logger = logging.getLogger(__name__)

class StudentController:
    """Controlador para gestión de estudiantes"""
    
    def __init__(self):
        self.db_manager = SQLiteManager()
    
    def get_all_students(self, clase_id=None):
        """Obtener todos los estudiantes"""
        try:
            session = self.db_manager.get_session()
            
            query = session.query(Alumno).filter_by(activo=True)
            
            if clase_id:
                query = query.filter_by(clase_id=clase_id)
            
            students = query.order_by(Alumno.numero_lista).all()
            
            result = []
            for student in students:
                result.append({
                    'id': student.id,
                    'list_number': student.numero_lista,
                    'full_name': student.nombre,
                    'section_id': student.clase_id,
                    'section_name': student.clase.nombre if student.clase else 'Sin clase',
                    'is_active': student.activo
                })
            
            session.close()
            logger.info(f"Se obtuvieron {len(result)} estudiantes")
            return result
            
        except Exception as e:
            logger.error(f"Error al obtener estudiantes: {e}")
            return []
    
    def get_student_by_id(self, student_id):
        """Obtener un estudiante por ID"""
        try:
            session = self.db_manager.get_session()
            
            student = session.query(Alumno).filter_by(id=student_id).first()
            
            if student:
                result = {
                    'id': student.id,
                    'list_number': student.numero_lista,
                    'full_name': student.nombre,
                    'section_id': student.clase_id,
                    'is_active': student.activo
                }
                session.close()
                return result
            
            session.close()
            return None
            
        except Exception as e:
            logger.error(f"Error al obtener estudiante {student_id}: {e}")
            return None
    
    def create_student(self, full_name, list_number, section_id=None):
        """Crear un nuevo estudiante"""
        try:
            session = self.db_manager.get_session()
            
            # Si no hay clase, crear una de ejemplo
            if section_id is None:
                section_id = self.get_or_create_default_class(session)
            
            # Validar número de lista duplicado
            existing = session.query(Alumno).filter_by(
                clase_id=section_id,
                numero_lista=list_number,
                activo=True
            ).first()
            
            if existing:
                session.close()
                return {
                    'success': False,
                    'message': f'Ya existe un estudiante con el número de lista {list_number} en esta clase'
                }
            
            # Crear nuevo estudiante
            new_student = Alumno(
                nombre=full_name.strip(),
                numero_lista=list_number,
                clase_id=section_id,
                activo=True
            )
            
            session.add(new_student)
            session.commit()
            
            student_id = new_student.id
            session.close()
            
            logger.info(f"Estudiante creado: {full_name} (ID: {student_id})")
            
            return {
                'success': True,
                'message': 'Estudiante creado exitosamente',
                'student_id': student_id
            }
            
        except Exception as e:
            logger.error(f"Error al crear estudiante: {e}")
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    def update_student(self, student_id, full_name=None, list_number=None, section_id=None):
        """Actualizar un estudiante existente"""
        try:
            session = self.db_manager.get_session()
            
            student = session.query(Alumno).filter_by(id=student_id).first()
            
            if not student:
                session.close()
                return {
                    'success': False,
                    'message': 'Estudiante no encontrado'
                }
            
            # Validar número de lista si se está cambiando
            if list_number and list_number != student.numero_lista:
                existing = session.query(Alumno).filter_by(
                    clase_id=student.clase_id,
                    numero_lista=list_number,
                    activo=True
                ).filter(Alumno.id != student_id).first()
                
                if existing:
                    session.close()
                    return {
                        'success': False,
                        'message': f'Ya existe un estudiante con el número de lista {list_number}'
                    }
            
            # Actualizar campos
            if full_name:
                student.nombre = full_name.strip()
            if list_number:
                student.numero_lista = list_number
            
            session.commit()
            session.close()
            
            logger.info(f"Estudiante actualizado: ID {student_id}")
            
            return {
                'success': True,
                'message': 'Estudiante actualizado exitosamente'
            }
            
        except Exception as e:
            logger.error(f"Error al actualizar estudiante {student_id}: {e}")
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    def delete_student(self, student_id):
        """Eliminar un estudiante (soft delete)"""
        try:
            session = self.db_manager.get_session()
            
            student = session.query(Alumno).filter_by(id=student_id).first()
            
            if not student:
                session.close()
                return {
                    'success': False,
                    'message': 'Estudiante no encontrado'
                }
            
            # Soft delete
            student.activo = False
            
            session.commit()
            session.close()
            
            logger.info(f"Estudiante eliminado: ID {student_id}")
            
            return {
                'success': True,
                'message': 'Estudiante eliminado exitosamente'
            }
            
        except Exception as e:
            logger.error(f"Error al eliminar estudiante {student_id}: {e}")
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    def search_students(self, search_term):
        """Buscar estudiantes por nombre o número de lista"""
        try:
            session = self.db_manager.get_session()
            
            # Buscar por nombre
            students = session.query(Alumno).filter(
                Alumno.activo == True,
                Alumno.nombre.ilike(f'%{search_term}%')
            ).order_by(Alumno.numero_lista).all()
            
            result = []
            for student in students:
                result.append({
                    'id': student.id,
                    'list_number': student.numero_lista,
                    'full_name': student.nombre,
                    'section_id': student.clase_id,
                    'section_name': student.clase.nombre if student.clase else 'Sin clase',
                    'is_active': student.activo
                })
            
            session.close()
            logger.info(f"Búsqueda '{search_term}': {len(result)} resultados")
            return result
            
        except Exception as e:
            logger.error(f"Error al buscar estudiantes: {e}")
            return []
    
    def get_or_create_default_class(self, session):
        """Obtener o crear clase por defecto"""
        try:
            # Buscar clase existente
            clase = session.query(Clase).first()
            
            if clase:
                return clase.id
            
            # Crear clase de ejemplo
            from src.database.models import Usuario, Seccion, Nivel, Institucion
            
            # Crear usuario de ejemplo si no existe
            usuario = session.query(Usuario).first()
            if not usuario:
                usuario = Usuario(
                    nombre="Profesor de Ejemplo",
                    email="profesor@ejemplo.com",
                    password_hash="hash_temporal",
                    es_admin=False
                )
                session.add(usuario)
                session.flush()
            
            # Crear institución si no existe
            institucion = session.query(Institucion).first()
            if not institucion:
                institucion = Institucion(
                    nombre="Institución de Ejemplo",
                    tipo="colegio"
                )
                session.add(institucion)
                session.flush()
            
            # Crear nivel si no existe
            nivel = session.query(Nivel).first()
            if not nivel:
                nivel = Nivel(
                    institucion_id=institucion.id,
                    nombre="Primer Grado",
                    orden=1
                )
                session.add(nivel)
                session.flush()
            
            # Crear sección si no existe
            seccion = session.query(Seccion).first()
            if not seccion:
                seccion = Seccion(
                    nivel_id=nivel.id,
                    nombre="Sección A"
                )
                session.add(seccion)
                session.flush()
            
            # Crear clase
            nueva_clase = Clase(
                profesor_id=usuario.id,
                seccion_id=seccion.id,
                nombre="Clase General",
                anio_academico=2025,
                activa=True
            )
            session.add(nueva_clase)
            session.flush()
            
            logger.info(f"Clase de ejemplo creada: ID {nueva_clase.id}")
            return nueva_clase.id
            
        except Exception as e:
            logger.error(f"Error al crear clase de ejemplo: {e}")
            session.rollback()
            return None
    
    def create_sample_section(self):
        """Compatibilidad con código anterior"""
        session = self.db_manager.get_session()
        try:
            clase_id = self.get_or_create_default_class(session)
            session.commit()
            session.close()
            return clase_id
        except Exception as e:
            session.rollback()
            session.close()
            logger.error(f"Error: {e}")
            return None