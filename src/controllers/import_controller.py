"""
Controlador de Importación de Estudiantes desde Excel
Versión corregida con manejo robusto de errores
"""
import pandas as pd
from pathlib import Path
import logging
from typing import Tuple, Dict, List

logger = logging.getLogger(__name__)

class ImportController:
    """Controlador para importación de estudiantes desde Excel"""
    
    def __init__(self, db_manager):
        """
        Inicializar controlador
        Args:
            db_manager: Instancia del gestor de base de datos
        """
        self.db = db_manager
    
    def validate_excel_file(self, file_path: str) -> Tuple[bool, str, pd.DataFrame]:
        """
        Validar que el archivo Excel tenga el formato correcto
        Args:
            file_path: Ruta del archivo Excel
        Returns:
            tuple (bool, str, DataFrame): (válido, mensaje, datos)
        """
        try:
            # Verificar que el archivo existe
            if not Path(file_path).exists():
                return False, "El archivo no existe", None
            
            # Verificar extensión
            ext = Path(file_path).suffix.lower()
            if ext not in ['.xlsx', '.xls', '.xlsm']:
                return False, "El archivo debe ser Excel (.xlsx, .xls, .xlsm)", None
            
            # Leer archivo Excel
            try:
                df = pd.read_excel(file_path)
            except Exception as e:
                return False, f"Error al leer el archivo: {str(e)}", None
            
            # Validar que no esté vacío
            if df.empty:
                return False, "El archivo está vacío", None
            
            # Normalizar nombres de columnas
            df.columns = df.columns.str.lower().str.strip()
            
            # Validar columnas requeridas
            required_columns = ['numero', 'nombre']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return False, f"Faltan columnas requeridas: {', '.join(missing_columns)}", None
            
            # Eliminar filas completamente vacías
            df = df.dropna(how='all')
            
            # Validar que haya datos después de limpiar
            if df.empty:
                return False, "No hay datos válidos en el archivo", None
            
            # Validar tipos de datos
            df['numero'] = pd.to_numeric(df['numero'], errors='coerce')
            df = df.dropna(subset=['numero'])
            df['numero'] = df['numero'].astype(int)
            
            # Validar que nombre no esté vacío
            df = df[df['nombre'].notna() & (df['nombre'] != '')]
            df['nombre'] = df['nombre'].astype(str).str.strip()
            
            if df.empty:
                return False, "No hay registros válidos (números o nombres vacíos)", None
            
            # Verificar duplicados en el archivo
            duplicados = df[df.duplicated(subset=['numero'], keep=False)]
            if not duplicados.empty:
                nums_duplicados = duplicados['numero'].unique().tolist()
                return False, f"Números duplicados en el archivo: {nums_duplicados}", None
            
            logger.info(f"Archivo validado correctamente: {len(df)} registros")
            return True, f"Archivo válido: {len(df)} estudiantes", df
            
        except Exception as e:
            logger.error(f"Error al validar archivo: {e}")
            return False, f"Error inesperado: {str(e)}", None
    
    def import_students(self, df: pd.DataFrame, class_id: int = None) -> Dict:
        """
        Importar estudiantes desde DataFrame
        Args:
            df: DataFrame con datos validados
            class_id: ID de la clase (opcional)
        Returns:
            dict: Resultado de la importación
        """
        resultados = {
            'total': len(df),
            'exitosos': 0,
            'duplicados': 0,
            'errores': 0,
            'detalles': []
        }
        
        try:
            for idx, row in df.iterrows():
                try:
                    numero = int(row['numero'])
                    nombre = str(row['nombre']).strip()
                    
                    # Verificar si ya existe
                    existing = self.db.get_student_by_number(numero)
                    
                    if existing:
                        resultados['duplicados'] += 1
                        resultados['detalles'].append({
                            'numero': numero,
                            'nombre': nombre,
                            'status': 'duplicado',
                            'mensaje': 'Ya existe en la base de datos'
                        })
                        continue
                    
                    # Crear estudiante
                    success = self.db.add_student(numero, nombre, class_id)
                    
                    if success:
                        resultados['exitosos'] += 1
                        resultados['detalles'].append({
                            'numero': numero,
                            'nombre': nombre,
                            'status': 'exitoso',
                            'mensaje': 'Importado correctamente'
                        })
                    else:
                        resultados['errores'] += 1
                        resultados['detalles'].append({
                            'numero': numero,
                            'nombre': nombre,
                            'status': 'error',
                            'mensaje': 'Error al guardar en base de datos'
                        })
                        
                except Exception as e:
                    resultados['errores'] += 1
                    resultados['detalles'].append({
                        'numero': row.get('numero', 'N/A'),
                        'nombre': row.get('nombre', 'N/A'),
                        'status': 'error',
                        'mensaje': str(e)
                    })
            
            logger.info(f"Importación completada: {resultados['exitosos']} exitosos, "
                       f"{resultados['duplicados']} duplicados, {resultados['errores']} errores")
            
            return resultados
            
        except Exception as e:
            logger.error(f"Error durante importación: {e}")
            return {
                'total': len(df),
                'exitosos': 0,
                'duplicados': 0,
                'errores': len(df),
                'detalles': [],
                'error_general': str(e)
            }
    
    @staticmethod
    def create_template_excel(output_path: str) -> bool:
        """
        Crear archivo Excel plantilla
        Args:
            output_path: Ruta donde guardar el archivo
        Returns:
            bool: True si se creó exitosamente
        """
        try:
            # Datos de ejemplo
            data = {
                'numero': [1, 2, 3, 4, 5],
                'nombre': [
                    'Juan Pérez García',
                    'María López Rodríguez',
                    'Carlos Sánchez Martínez',
                    'Ana Torres Fernández',
                    'Luis Ramírez Gómez'
                ]
            }
            
            df = pd.DataFrame(data)
            
            # Crear el archivo Excel
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Estudiantes', index=False)
                
                # Ajustar ancho de columnas
                worksheet = writer.sheets['Estudiantes']
                worksheet.column_dimensions['A'].width = 12
                worksheet.column_dimensions['B'].width = 35
            
            logger.info(f"Plantilla Excel creada: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error al crear plantilla: {e}")
            return False
    
    def export_students_to_excel(self, output_path: str, students: List = None) -> bool:
        """
        Exportar estudiantes a Excel
        Args:
            output_path: Ruta del archivo de salida
            students: Lista de estudiantes (si no se provee, exporta todos)
        Returns:
            bool: True si se exportó exitosamente
        """
        try:
            # Si no se proveen estudiantes, obtener todos
            if students is None:
                students = self.db.get_all_students()
            
            if not students:
                logger.warning("No hay estudiantes para exportar")
                return False
            
            # Convertir a DataFrame
            data = []
            for student in students:
                data.append({
                    'Número': student.list_number,
                    'Nombre': student.full_name,
                    'Fecha Registro': student.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(student, 'created_at') else 'N/A',
                    'Activo': 'Sí' if student.is_active else 'No'
                })
            
            df = pd.DataFrame(data)
            
            # Crear el archivo Excel
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Estudiantes', index=False)
                
                # Ajustar ancho de columnas
                worksheet = writer.sheets['Estudiantes']
                worksheet.column_dimensions['A'].width = 12
                worksheet.column_dimensions['B'].width = 35
                worksheet.column_dimensions['C'].width = 20
                worksheet.column_dimensions['D'].width = 12
            
            logger.info(f"Estudiantes exportados a: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error al exportar estudiantes: {e}")
            return False
