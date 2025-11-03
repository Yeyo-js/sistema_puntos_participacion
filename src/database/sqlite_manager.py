"""
Gestor de base de datos SQLite (modo offline)
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from src.database.models import Base
from src.config.settings import SQLITE_DB_PATH
import logging

logger = logging.getLogger(__name__)


class SQLiteManager:
    """Gestor de conexiones y operaciones con SQLite"""
    
    _instance = None
    _engine = None
    _session_factory = None
    
    def __new__(cls):
        """Patrón Singleton para una única instancia del gestor"""
        if cls._instance is None:
            cls._instance = super(SQLiteManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializar el gestor si aún no está inicializado"""
        if self._engine is None:
            self.connect()
    
    def connect(self):
        """Establecer conexión con SQLite"""
        try:
            # Crear engine de SQLite
            database_url = f"sqlite:///{SQLITE_DB_PATH}"
            self._engine = create_engine(
                database_url,
                echo=False,  # Cambiar a True para debug de SQL
                connect_args={"check_same_thread": False}  # Necesario para SQLite
            )
            
            # Crear todas las tablas
            Base.metadata.create_all(self._engine)
            
            # Crear session factory
            self._session_factory = scoped_session(
                sessionmaker(
                    bind=self._engine,
                    autocommit=False,
                    autoflush=False
                )
            )
            
            logger.info(f"Conexión exitosa a SQLite: {SQLITE_DB_PATH}")
            return True
            
        except Exception as e:
            logger.error(f"Error al conectar con SQLite: {e}")
            return False
    
    def get_session(self):
        """Obtener una nueva sesión de base de datos"""
        if self._session_factory is None:
            self.connect()
        return self._session_factory()
    
    def close_session(self, session):
        """Cerrar una sesión de base de datos"""
        try:
            if session:
                session.close()
        except Exception as e:
            logger.error(f"Error al cerrar sesión: {e}")
    
    def disconnect(self):
        """Cerrar todas las conexiones"""
        try:
            if self._session_factory:
                self._session_factory.remove()
            if self._engine:
                self._engine.dispose()
            logger.info("Desconectado de SQLite")
        except Exception as e:
            logger.error(f"Error al desconectar de SQLite: {e}")
    
    def test_connection(self):
        """Probar la conexión a la base de datos"""
        try:
            session = self.get_session()
            session.execute("SELECT 1")
            self.close_session(session)
            return True
        except Exception as e:
            logger.error(f"Error en test de conexión: {e}")
            return False
    
    def reset_database(self):
        """Eliminar y recrear todas las tablas (usar con precaución)"""
        try:
            Base.metadata.drop_all(self._engine)
            Base.metadata.create_all(self._engine)
            logger.info("Base de datos reseteada exitosamente")
            return True
        except Exception as e:
            logger.error(f"Error al resetear base de datos: {e}")
            return False


# Instancia global del gestor
sqlite_manager = SQLiteManager()
