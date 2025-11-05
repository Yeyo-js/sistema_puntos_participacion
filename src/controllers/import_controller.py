"""
Controlador de Importación de Estudiantes desde Excel
Maneja la lógica de importación masiva desde archivos Excel
"""
import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ImportController:
    """Controlador para importación de estudiantes desde Excel"""
    
    @staticmethod
    def validate_excel_file(file_path):
        """
        Validar que el archivo Excel tenga el formato correcto
        Args:
            file_path: Ruta del archivo Excel
        Returns:
            tuple (bool, str, DataFrame): (válido, mensaje, datos)
        """
        try:
            # Verificar extensión
            ext = Path(file_path).suffix.lower()
            if ext not in ['.xlsx', '.xls', '.xlsm']:
                return False, "El archivo debe ser Excel (.xlsx, .xls)", None
            
            # Leer archivo
            df = pd.read_excel(file_path)
            
            # Validar que no esté vacío
            if df.empty:
                return False, "El archivo está vacío", None
            
            # Validar columnas requeridas
            required_columns = ['numero', 'nombre']
            df.columns = df.columns.str.lower().str.strip()
            
            missing_columns = []
            for col in required_columns:
                if col not in df.columns:
                    missing_columns.append(col)
            
            if missing_columns:
                return False, f"Faltan columnas: {', '.join(missing_columns)}", None
            
            # Limpiar datos
            df = df[['numero', 'nombre']].copy()
            df = df.dropna(subset=['numero', 'nombre'])
            
            # Convertir número a entero
            try:
                df['numero'] = df['numero'].astype(int)
            except:
                return False, "La columna 'numero' debe contener solo números", None
            
            # Validar que haya datos después de limpiar
            if df.empty:
                return False, "No hay datos válidos en el archivo", None
            
            logger.info(f"Archivo validado: {len(df)} registros encontrados")
            return True, f"Archivo válido: {len(df)} estudiantes encontrados", df
            
        except Exception as e:
            logger.error(f"Error al validar archivo: {e}")
            return False, f"Error al leer archivo: {str(e)}", None
    
    @staticmethod
    def import_students(df, student_controller, clase_id=None):
        """
        Importar estudiantes desde DataFrame
        Args:
            df: DataFrame con datos de estudiantes
            student_controller: Instancia de StudentController
            clase_id: ID de la clase (opcional)
        Returns:
            dict con resultados de importación
        """
        try:
            # Si no hay clase, crear una por defecto
            if clase_id is None:
                clase_id = student_controller.create_sample_section()
            
            resultados = {
                'total': len(df),
                'exitosos': 0,
                'duplicados': 0,
                'errores': 0,
                'detalles': []
            }
            
            for index, row in df.iterrows():
                numero = int(row['numero'])
                nombre = str(row['nombre']).strip()
                
                # Intentar crear estudiante
                result = student_controller.create_student(
                    full_name=nombre,
                    list_number=numero,
                    section_id=clase_id
                )
                
                if result['success']:
                    resultados['exitosos'] += 1
                    resultados['detalles'].append({
                        'numero': numero,
                        'nombre': nombre,
                        'estado': 'exitoso',
                        'mensaje': 'Importado correctamente'
                    })
                else:
                    # Detectar si es duplicado
                    if 'Ya existe' in result['message']:
                        resultados['duplicados'] += 1
                        resultados['detalles'].append({
                            'numero': numero,
                            'nombre': nombre,
                            'estado': 'duplicado',
                            'mensaje': 'Ya existe en la base de datos'
                        })
                    else:
                        resultados['errores'] += 1
                        resultados['detalles'].append({
                            'numero': numero,
                            'nombre': nombre,
                            'estado': 'error',
                            'mensaje': result['message']
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
    def create_template_excel(output_path):
        """
        Crear archivo Excel de ejemplo/plantilla
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
            
            # Guardar archivo
            df.to_excel(output_path, index=False, sheet_name='Estudiantes')
            
            logger.info(f"Plantilla Excel creada: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error al crear plantilla: {e}")
            return False
