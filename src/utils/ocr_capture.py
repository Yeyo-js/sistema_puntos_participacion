"""
Sistema de captura de lista de alumnos mediante foto
Este módulo permite al profesor tomar una foto de su lista y extraer los nombres automáticamente
"""
import cv2
import pytesseract
from PIL import Image
import re
import logging

logger = logging.getLogger(__name__)

class ListaCaptureOCR:
    """Clase para capturar y procesar listas de alumnos desde imágenes"""
    
    def __init__(self):
        # Configurar ruta de Tesseract (ajustar según instalación)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    def capturar_desde_camara(self):
        """Capturar imagen desde la cámara web"""
        logger.info("Iniciando captura desde cámara...")
        
        # Abrir cámara
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            logger.error("No se pudo abrir la cámara")
            return None
        
        # Configurar resolución
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        logger.info("Cámara lista. Presiona ESPACIO para capturar, ESC para cancelar")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Mostrar preview
            cv2.putText(frame, "Presiona ESPACIO para capturar", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "ESC para cancelar", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Capturar Lista de Alumnos', frame)
            
            key = cv2.waitKey(1)
            
            # ESPACIO para capturar
            if key == 32:
                logger.info("Foto capturada")
                cap.release()
                cv2.destroyAllWindows()
                return frame
            
            # ESC para cancelar
            elif key == 27:
                logger.info("Captura cancelada")
                cap.release()
                cv2.destroyAllWindows()
                return None
        
        cap.release()
        cv2.destroyAllWindows()
        return None
    
    def procesar_desde_archivo(self, ruta_imagen: str):
        """Procesar imagen desde archivo"""
        try:
            imagen = cv2.imread(ruta_imagen)
            if imagen is None:
                logger.error(f"No se pudo cargar la imagen: {ruta_imagen}")
                return None
            return imagen
        except Exception as e:
            logger.error(f"Error al cargar imagen: {e}")
            return None
    
    def preprocesar_imagen(self, imagen):
        """Preprocesar imagen para mejorar OCR"""
        # Convertir a escala de grises
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        
        # Aplicar umbral para mejorar contraste
        _, umbral = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Eliminar ruido
        denoised = cv2.fastNlMeansDenoising(umbral, None, 10, 7, 21)
        
        return denoised
    
    def extraer_texto(self, imagen):
        """Extraer texto de la imagen usando OCR"""
        try:
            # Preprocesar
            imagen_procesada = self.preprocesar_imagen(imagen)
            
            # Convertir a PIL Image
            pil_image = Image.fromarray(imagen_procesada)
            
            # Configuración de Tesseract para español
            config_tesseract = '--psm 6 -l spa'  # psm 6 = bloque uniforme de texto
            
            # Extraer texto
            texto = pytesseract.image_to_string(pil_image, config=config_tesseract)
            
            logger.info("Texto extraído exitosamente")
            return texto
            
        except Exception as e:
            logger.error(f"Error al extraer texto: {e}")
            return ""
    
    def parsear_nombres(self, texto: str):
        """Parsear el texto extraído para obtener lista de nombres"""
        lineas = texto.strip().split('\n')
        nombres = []
        
        # Patrones comunes en listas
        # Ejemplo: "1. Juan Pérez" o "1 - Juan Pérez" o "01 Juan Pérez"
        patron_lista = r'^\s*\d+[\.\-\)]*\s*(.+)$'
        
        for linea in lineas:
            linea = linea.strip()
            
            # Ignorar líneas vacías
            if not linea:
                continue
            
            # Intentar extraer nombre con patrón de lista numerada
            match = re.match(patron_lista, linea)
            if match:
                nombre = match.group(1).strip()
                # Limpiar caracteres extraños
                nombre = re.sub(r'[^\w\sáéíóúñÁÉÍÓÚÑ]', '', nombre)
                if len(nombre) > 3:  # Filtrar nombres muy cortos
                    nombres.append(nombre)
            else:
                # Si no tiene número, verificar si parece un nombre
                # (contiene al menos 2 palabras con letras)
                palabras = linea.split()
                if len(palabras) >= 2 and all(any(c.isalpha() for c in p) for p in palabras):
                    nombre = ' '.join(palabras)
                    nombre = re.sub(r'[^\w\sáéíóúñÁÉÍÓÚÑ]', '', nombre)
                    if len(nombre) > 3:
                        nombres.append(nombre)
        
        logger.info(f"Se extrajeron {len(nombres)} nombres")
        return nombres
    
    def capturar_y_procesar(self, desde_camara=True, ruta_archivo=None):
        """
        Método principal: captura y procesa la lista
        
        Args:
            desde_camara: Si True, captura desde cámara. Si False, usa archivo.
            ruta_archivo: Ruta del archivo si desde_camara=False
        
        Returns:
            Lista de nombres extraídos
        """
        # Capturar imagen
        if desde_camara:
            imagen = self.capturar_desde_camara()
        else:
            if not ruta_archivo:
                logger.error("Debe proporcionar una ruta de archivo")
                return []
            imagen = self.procesar_desde_archivo(ruta_archivo)
        
        if imagen is None:
            logger.error("No se pudo obtener la imagen")
            return []
        
        # Extraer texto
        texto = self.extraer_texto(imagen)
        
        if not texto:
            logger.error("No se pudo extraer texto de la imagen")
            return []
        
        logger.debug(f"Texto extraído:\n{texto}")
        
        # Parsear nombres
        nombres = self.parsear_nombres(texto)
        
        return nombres
    
    def asignar_numeros_lista(self, nombres):
        """Asignar números de lista automáticamente"""
        return [(i+1, nombre) for i, nombre in enumerate(nombres)]


# Ejemplo de uso
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Crear instancia
    ocr = ListaCaptureOCR()
    
    # Opción 1: Capturar desde cámara
    print("=== Captura desde cámara ===")
    nombres = ocr.capturar_y_procesar(desde_camara=True)
    
    # Opción 2: Procesar desde archivo
    # nombres = ocr.capturar_y_procesar(desde_camara=False, ruta_archivo="lista_alumnos.jpg")
    
    if nombres:
        print(f"\n✅ Se encontraron {len(nombres)} alumnos:")
        lista_numerada = ocr.asignar_numeros_lista(nombres)
        for numero, nombre in lista_numerada:
            print(f"{numero}. {nombre}")
    else:
        print("\n❌ No se pudieron extraer nombres")
