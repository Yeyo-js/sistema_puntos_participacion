"""
Gestor de sincronización entre SQLite (offline) y SQL Server (online)
"""
import threading
import time
from datetime import datetime
from src.database.sqlite_manager import sqlite_manager
from src.database.sqlserver_manager import sqlserver_manager
from src.database.models import (
    Usuario, Institucion, Nivel, Seccion, Clase, Alumno, Participacion, SyncLog
)
from src.config.settings import SYNC_INTERVAL, AUTO_SYNC
import logging

logger = logging.getLogger(__name__)


class SyncManager:
    """Gestor de sincronización automática entre bases de datos"""
    
    def __init__(self):
        self._sync_thread = None
        self._running = False
        self._last_sync = None
    
    def start_auto_sync(self):
        """Iniciar sincronización automática en un hilo separado"""
        if not AUTO_SYNC:
            logger.info("Sincronización automática deshabilitada")
            return
        
        if self._running:
            logger.warning("Sincronización automática ya está en ejecución")
            return
        
        self._running = True
        self._sync_thread = threading.Thread(target=self._auto_sync_loop, daemon=True)
        self._sync_thread.start()
        logger.info(f"Sincronización automática iniciada (intervalo: {SYNC_INTERVAL}s)")
    
    def stop_auto_sync(self):
        """Detener sincronización automática"""
        self._running = False
        if self._sync_thread:
            self._sync_thread.join(timeout=5)
        logger.info("Sincronización automática detenida")
    
    def _auto_sync_loop(self):
        """Loop de sincronización automática"""
        while self._running:
            try:
                # Verificar si SQL Server está disponible
                if sqlserver_manager.test_connection():
                    self.sync_to_server()
                else:
                    logger.warning("SQL Server no disponible, se omite sincronización")
                
                # Esperar el intervalo configurado
                time.sleep(SYNC_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error en loop de sincronización: {e}")
                time.sleep(SYNC_INTERVAL)
    
    def sync_to_server(self):
        """
        Sincronizar datos de SQLite a SQL Server
        Sube los cambios locales al servidor
        """
        try:
            logger.info("Iniciando sincronización hacia SQL Server...")
            
            sqlite_session = sqlite_manager.get_session()
            server_session = sqlserver_manager.get_session()
            
            registros_sincronizados = 0
            
            try:
                # Obtener todos los modelos a sincronizar
                modelos = [Usuario, Institucion, Nivel, Seccion, Clase, Alumno, Participacion]
                
                for modelo in modelos:
                    # Obtener registros locales
                    registros_locales = sqlite_session.query(modelo).all()
                    
                    for registro in registros_locales:
                        # Verificar si existe en el servidor
                        registro_servidor = server_session.query(modelo).filter_by(
                            id=registro.id
                        ).first()
                        
                        if registro_servidor:
                            # Actualizar registro existente
                            for key, value in registro.__dict__.items():
                                if not key.startswith('_'):
                                    setattr(registro_servidor, key, value)
                        else:
                            # Crear nuevo registro
                            nuevo_registro = modelo(**{
                                key: value for key, value in registro.__dict__.items()
                                if not key.startswith('_')
                            })
                            server_session.add(nuevo_registro)
                        
                        registros_sincronizados += 1
                
                # Confirmar cambios
                server_session.commit()
                
                # Registrar sincronización exitosa
                self._log_sync(sqlite_session, "upload", "exitoso", registros_sincronizados)
                
                self._last_sync = datetime.now()
                logger.info(f"Sincronización exitosa: {registros_sincronizados} registros")
                
            except Exception as e:
                server_session.rollback()
                self._log_sync(sqlite_session, "upload", "error", 0, str(e))
                logger.error(f"Error durante sincronización: {e}")
                raise
            
            finally:
                sqlite_manager.close_session(sqlite_session)
                sqlserver_manager.close_session(server_session)
        
        except Exception as e:
            logger.error(f"Error al sincronizar con servidor: {e}")
            return False
        
        return True
    
    def sync_from_server(self):
        """
        Sincronizar datos de SQL Server a SQLite
        Descarga cambios del servidor a local
        """
        try:
            logger.info("Iniciando sincronización desde SQL Server...")
            
            sqlite_session = sqlite_manager.get_session()
            server_session = sqlserver_manager.get_session()
            
            registros_sincronizados = 0
            
            try:
                # Obtener todos los modelos a sincronizar
                modelos = [Usuario, Institucion, Nivel, Seccion, Clase, Alumno, Participacion]
                
                for modelo in modelos:
                    # Obtener registros del servidor
                    registros_servidor = server_session.query(modelo).all()
                    
                    for registro in registros_servidor:
                        # Verificar si existe localmente
                        registro_local = sqlite_session.query(modelo).filter_by(
                            id=registro.id
                        ).first()
                        
                        if registro_local:
                            # Actualizar registro existente
                            for key, value in registro.__dict__.items():
                                if not key.startswith('_'):
                                    setattr(registro_local, key, value)
                        else:
                            # Crear nuevo registro
                            nuevo_registro = modelo(**{
                                key: value for key, value in registro.__dict__.items()
                                if not key.startswith('_')
                            })
                            sqlite_session.add(nuevo_registro)
                        
                        registros_sincronizados += 1
                
                # Confirmar cambios
                sqlite_session.commit()
                
                # Registrar sincronización exitosa
                self._log_sync(sqlite_session, "download", "exitoso", registros_sincronizados)
                
                self._last_sync = datetime.now()
                logger.info(f"Sincronización desde servidor exitosa: {registros_sincronizados} registros")
                
            except Exception as e:
                sqlite_session.rollback()
                self._log_sync(sqlite_session, "download", "error", 0, str(e))
                logger.error(f"Error durante sincronización: {e}")
                raise
            
            finally:
                sqlite_manager.close_session(sqlite_session)
                sqlserver_manager.close_session(server_session)
        
        except Exception as e:
            logger.error(f"Error al sincronizar desde servidor: {e}")
            return False
        
        return True
    
    def manual_sync(self, direction="bidireccional"):
        """
        Sincronización manual
        direction: "upload", "download", "bidireccional"
        """
        if direction in ["upload", "bidireccional"]:
            self.sync_to_server()
        
        if direction in ["download", "bidireccional"]:
            self.sync_from_server()
    
    def _log_sync(self, session, tipo, estado, registros, mensaje=""):
        """Registrar sincronización en la base de datos"""
        try:
            log = SyncLog(
                tipo=tipo,
                estado=estado,
                registros_afectados=registros,
                mensaje=mensaje
            )
            session.add(log)
            session.commit()
        except Exception as e:
            logger.error(f"Error al registrar log de sincronización: {e}")
    
    def get_last_sync_time(self):
        """Obtener la fecha/hora de la última sincronización"""
        return self._last_sync


# Instancia global del gestor de sincronización
sync_manager = SyncManager()
