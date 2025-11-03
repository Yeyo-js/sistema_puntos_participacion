"""
Controlador de Estudiantes
Maneja toda la lógica de negocio para el CRUD de estudiantes
"""
from src.database.sqlite_manager import SQLiteManager
from src.database.models import Alumno as Student, Seccion as Section
from sqlalchemy import or_
import logging

logger = logging.getLogger(__name__)

class StudentController:
    """Controlador para gestión de estudiantes"""
    
    def __init__(self):
        self.db_manager = SQLiteManager()
    
    def get_all_students(self, section_id=None):
        """
        Obtener todos los estudiantes
        Args:
            section_id: Filtrar por sección (opcional)
        Returns:
            Lista de estudiantes
        """
        try:
            session = self.db_manager.get_session()
            
            query = session.query(Student).filter_by(is_active=True)
            
            if section_id:
                query = query.filter_by(section_id=section_id)
            
            students = query.order_by(Student.list_number).all()
            
            # Convertir a diccionarios para facilitar el uso en UI
            result = []
            for student in students:
                result.append({
                    'id': student.id,
                    'list_number': student.list_number,
                    'full_name': student.full_name,
                    'section_id': student.section_id,
                    'section_name': student.section.name if student.section else 'Sin sección',
                    'is_active': student.is_active
                })
            
            session.close()
            logger.info(f"Se obtuvieron {len(result)} estudiantes")
            return result
            
        except Exception as e:
            logger.error(f"Error al obtener estudiantes: {e}")
            return []
    
    def get_student_by_id(self, student_id):
        """
        Obtener un estudiante por ID
        Args:
            student_id: ID del estudiante
        Returns:
            Diccionario con datos del estudiante o None
        """
        try:
            session = self.db_manager.get_session()
            
            student = session.query(Student).filter_by(id=student_id).first()
            
            if student:
                result = {
                    'id': student.id,
                    'list_number': student.list_number,
                    'full_name': student.full_name,
                    'section_id': student.section_id,
                    'is_active': student.is_active
                }
                session.close()
                return result
            
            session.close()
            return None
            
        except Exception as e:
            logger.error(f"Error al obtener estudiante {student_id}: {e}")
            return None
    
    def create_student(self, full_name, list_number, section_id=None):
        """
        Crear un nuevo estudiante
        Args:
            full_name: Nombre completo
            list_number: Número de lista
            section_id: ID de la sección (opcional)
        Returns:
            dict con 'success' y 'message'
        """
        try:
            session = self.db_manager.get_session()
            
            # Validar que no exista otro estudiante con el mismo número de lista en la sección
            if section_id:
                existing = session.query(Student).filter_by(
                    section_id=section_id,
                    list_number=list_number,
                    is_active=True
                ).first()
                
                if existing:
                    session.close()
                    return {
                        'success': False,
                        'message': f'Ya existe un estudiante con el número de lista {list_number} en esta sección'
                    }
            
            # Crear nuevo estudiante
            new_student = Student(
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
                'message': f'Error al crear estudiante: {str(e)}'
            }
    
    def update_student(self, student_id, full_name=None, list_number=None, section_id=None):
        """
        Actualizar un estudiante existente
        Args:
            student_id: ID del estudiante
            full_name: Nuevo nombre (opcional)
            list_number: Nuevo número de lista (opcional)
            section_id: Nueva sección (opcional)
        Returns:
            dict con 'success' y 'message'
        """
        try:
            session = self.db_manager.get_session()
            
            student = session.query(Student).filter_by(id=student_id).first()
            
            if not student:
                session.close()
                return {
                    'success': False,
                    'message': 'Estudiante no encontrado'
                }
            
            # Validar número de lista si se está cambiando
            if list_number and list_number != student.list_number:
                if section_id or student.section_id:
                    check_section = section_id if section_id else student.section_id
                    existing = session.query(Student).filter_by(
                        section_id=check_section,
                        list_number=list_number,
                        is_active=True
                    ).filter(Student.id != student_id).first()
                    
                    if existing:
                        session.close()
                        return {
                            'success': False,
                            'message': f'Ya existe un estudiante con el número de lista {list_number} en esta sección'
                        }
            
            # Actualizar campos
            if full_name:
                student.full_name = full_name.strip()
            if list_number:
                student.list_number = list_number
            if section_id is not None:
                student.section_id = section_id
            
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
                'message': f'Error al actualizar estudiante: {str(e)}'
            }
    
    def delete_student(self, student_id):
        """
        Eliminar un estudiante (soft delete)
        Args:
            student_id: ID del estudiante
        Returns:
            dict con 'success' y 'message'
        """
        try:
            session = self.db_manager.get_session()
            
            student = session.query(Student).filter_by(id=student_id).first()
            
            if not student:
                session.close()
                return {
                    'success': False,
                    'message': 'Estudiante no encontrado'
                }
            
            # Soft delete: marcar como inactivo
            student.is_active = False
            
            session.commit()
            session.close()
            
            logger.info(f"Estudiante eliminado (soft delete): ID {student_id}")
            
            return {
                'success': True,
                'message': 'Estudiante eliminado exitosamente'
            }
            
        except Exception as e:
            logger.error(f"Error al eliminar estudiante {student_id}: {e}")
            return {
                'success': False,
                'message': f'Error al eliminar estudiante: {str(e)}'
            }
    
    def search_students(self, search_term):
        """
        Buscar estudiantes por nombre o número de lista
        Args:
            search_term: Término de búsqueda
        Returns:
            Lista de estudiantes que coinciden
        """
        try:
            session = self.db_manager.get_session()
            
            # Buscar por nombre o número de lista
            students = session.query(Student).filter(
                Student.is_active == True,
                or_(
                    Student.full_name.ilike(f'%{search_term}%'),
                    Student.list_number.cast(db.String).ilike(f'%{search_term}%')
                )
            ).order_by(Student.list_number).all()
            
            result = []
            for student in students:
                result.append({
                    'id': student.id,
                    'list_number': student.list_number,
                    'full_name': student.full_name,
                    'section_id': student.section_id,
                    'section_name': student.section.name if student.section else 'Sin sección',
                    'is_active': student.is_active
                })
            
            session.close()
            logger.info(f"Búsqueda '{search_term}': {len(result)} resultados")
            return result
            
        except Exception as e:
            logger.error(f"Error al buscar estudiantes: {e}")
            return []
    
    def get_all_sections(self):
        """
        Obtener todas las secciones disponibles
        Returns:
            Lista de secciones
        """
        try:
            session = self.db_manager.get_session()
            
            sections = session.query(Section).all()
            
            result = []
            for section in sections:
                result.append({
                    'id': section.id,
                    'name': section.name,
                    'grade': section.grade.name if section.grade else 'Sin grado',
                    'year': section.year
                })
            
            session.close()
            return result
            
        except Exception as e:
            logger.error(f"Error al obtener secciones: {e}")
            return []
    
    def create_sample_section(self):
        """
        Crear una sección de ejemplo si no existe ninguna
        Returns:
            ID de la sección creada o existente
        """
        try:
            session = self.db_manager.get_session()
            
            # Verificar si ya existe una sección
            existing = session.query(Section).first()
            if existing:
                session.close()
                return existing.id
            
            # Crear sección de ejemplo
            from src.database.models import Grade, Institution, Cycle
            
            # Crear institución de ejemplo
            institution = Institution(
                name="Institución de Ejemplo",
                institution_type="colegio"
            )
            session.add(institution)
            session.commit()
            
            # Crear grado de ejemplo
            grade = Grade(
                institution_id=institution.id,
                name="1° Secundaria",
                level=1
            )
            session.add(grade)
            session.commit()
            
            # Crear sección de ejemplo
            section = Section(
                grade_id=grade.id,
                name="Sección A",
                year=2025
            )
            session.add(section)
            session.commit()
            
            section_id = section.id
            session.close()
            
            logger.info(f"Sección de ejemplo creada: ID {section_id}")
            return section_id
            
        except Exception as e:
            logger.error(f"Error al crear sección de ejemplo: {e}")
            return None
