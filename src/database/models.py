"""
Modelos de base de datos usando SQLAlchemy
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Usuario(Base):
    """Modelo para profesores/usuarios del sistema"""
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    es_admin = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.now)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    clases = relationship("Clase", back_populates="profesor", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}')>"


class Institucion(Base):
    """Modelo para colegios e institutos"""
    __tablename__ = "instituciones"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    tipo = Column(String(50), nullable=False)  # "colegio" o "instituto"
    direccion = Column(String(255))
    telefono = Column(String(20))
    fecha_creacion = Column(DateTime, default=datetime.now)
    
    # Relaciones
    niveles = relationship("Nivel", back_populates="institucion", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Institucion(id={self.id}, nombre='{self.nombre}', tipo='{self.tipo}')>"


class Nivel(Base):
    """Modelo para ciclos/grados"""
    __tablename__ = "niveles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    institucion_id = Column(Integer, ForeignKey("instituciones.id"), nullable=False)
    nombre = Column(String(100), nullable=False)  # Ej: "Primer Ciclo", "Quinto Grado"
    descripcion = Column(Text)
    orden = Column(Integer)  # Para ordenar los niveles
    fecha_creacion = Column(DateTime, default=datetime.now)
    
    # Relaciones
    institucion = relationship("Institucion", back_populates="niveles")
    secciones = relationship("Seccion", back_populates="nivel", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Nivel(id={self.id}, nombre='{self.nombre}')>"


class Seccion(Base):
    """Modelo para secciones dentro de un nivel"""
    __tablename__ = "secciones"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nivel_id = Column(Integer, ForeignKey("niveles.id"), nullable=False)
    nombre = Column(String(50), nullable=False)  # Ej: "A", "B", "C"
    capacidad_maxima = Column(Integer)
    fecha_creacion = Column(DateTime, default=datetime.now)
    
    # Relaciones
    nivel = relationship("Nivel", back_populates="secciones")
    clases = relationship("Clase", back_populates="seccion", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Seccion(id={self.id}, nombre='{self.nombre}')>"


class Clase(Base):
    """Modelo para clases/cursos que dicta un profesor"""
    __tablename__ = "clases"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    profesor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    seccion_id = Column(Integer, ForeignKey("secciones.id"), nullable=False)
    nombre = Column(String(100), nullable=False)  # Ej: "Matemáticas", "Historia"
    descripcion = Column(Text)
    anio_academico = Column(Integer, nullable=False)  # Ej: 2025
    activa = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.now)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    profesor = relationship("Usuario", back_populates="clases")
    seccion = relationship("Seccion", back_populates="clases")
    alumnos = relationship("Alumno", back_populates="clase", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Clase(id={self.id}, nombre='{self.nombre}', año={self.anio_academico})>"


class Alumno(Base):
    """Modelo para alumnos"""
    __tablename__ = "alumnos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    clase_id = Column(Integer, ForeignKey("clases.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    numero_lista = Column(Integer, nullable=False)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.now)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    clase = relationship("Clase", back_populates="alumnos")
    participaciones = relationship("Participacion", back_populates="alumno", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Alumno(id={self.id}, nombre='{self.nombre}', num_lista={self.numero_lista})>"


class Participacion(Base):
    """Modelo para registro de puntos de participación"""
    __tablename__ = "participaciones"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    alumno_id = Column(Integer, ForeignKey("alumnos.id"), nullable=False)
    puntos = Column(Float, nullable=False, default=0.0)
    fecha = Column(DateTime, default=datetime.now)
    descripcion = Column(Text)  # Opcional: razón de los puntos
    tipo = Column(String(50))  # Ej: "positivo", "negativo", "ajuste"
    
    # Relaciones
    alumno = relationship("Alumno", back_populates="participaciones")
    
    def __repr__(self):
        return f"<Participacion(id={self.id}, alumno_id={self.alumno_id}, puntos={self.puntos})>"


class SyncLog(Base):
    """Modelo para registrar sincronizaciones entre SQLite y SQL Server"""
    __tablename__ = "sync_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_sync = Column(DateTime, default=datetime.now)
    tipo = Column(String(50))  # "upload", "download", "bidireccional"
    estado = Column(String(50))  # "exitoso", "error", "parcial"
    registros_afectados = Column(Integer, default=0)
    mensaje = Column(Text)
    
    def __repr__(self):
        return f"<SyncLog(id={self.id}, fecha='{self.fecha_sync}', estado='{self.estado}')>"
