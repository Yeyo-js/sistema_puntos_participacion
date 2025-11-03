"""
Gestor de base de datos SQL Server (modo online)
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from src.database.models import Base
from src.config.settings import SQL_SERVER_CONFIG
import logging
import urllib

logger = logging.getLogger(__name__)


class SQLServerManager:
    """Gestor de conexiones y operaciones con SQL Server"""
    
    _instance = None
    _engine = None
    _session_factory = None
    _connected = False
    
    def __new__(cls):
        """Patrón Singleton para una única instancia del gestor"""
        if cls._instance is None:
            cls._instance = super(SQLServerManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializar el gestor"""
        pass
    
    def connect(self):
        """Establecer conexión con SQL Server"""
        try:
            # Construir connection string para SQL Server
            params = urllib.parse.quote_plus(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={SQL_SERVER_CONFIG['host']},{SQL_SERVER_CONFIG['port']};"
                f"DATABASE={SQL_SERVER_CONFIG['database']};"
                f"UID={SQL_SERVER_CONFIG['user']};"
                f"PWD={SQL_SERVER_CONFIG['password']}"
            )
            
            database_url = f"mssql+pyodbc:///?odbc_connect={params}"
            
            # Crear engine de SQL Server
            self._engine = create_engine(
                database_url,
                echo=False,  # Cambiar a True para debug de SQL
                pool_pre_ping=True,  # Verificar conexiones antes de usar
                pool_recycle=3600  # Reciclar conexiones cada hora
            )
            
            # Crear todas las tablas si no existen
            Base.metadata.create_all(self._engine)
            
            # Crear session factory
            self._session_factory = scoped_session(
                sessionmaker(
                    bind=self._engine,
                    autocommit=False,
                    autoflush=False
                )
            )
            
            self._connected = True
            logger.info(f"Conexión exitosa a SQL Server: {SQL_SERVER_CONFIG['host']}")
            return True
            
        except Exception as e:
            self._connected = False
            logger.error(f"Error al conectar con SQL Server: {e}")
            return False
    
    def get_session(self):
        """Obtener una nueva sesión de base de datos"""
        if not self._connected or self._session_factory is None:
            if not self.connect():
                raise Exception("No se pudo conectar a SQL Server")
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
            self._connected = False
            logger.info("Desconectado de SQL Server")
        except Exception as e:
            logger.error(f"Error al desconectar de SQL Server: {e}")
    
    def test_connection(self):
        """Probar la conexión a la base de datos"""
        try:
            if not self._connected:
                return self.connect()
            
            session = self.get_session()
            session.execute("SELECT 1")
            self.close_session(session)
            return True
        except Exception as e:
            logger.error(f"Error en test de conexión SQL Server: {e}")
            self._connected = False
            return False
    
    def is_connected(self):
        """Verificar si hay conexión activa"""
        return self._connected and self.test_connection()


# Instancia global del gestor
sqlserver_manager = SQLServerManager()
