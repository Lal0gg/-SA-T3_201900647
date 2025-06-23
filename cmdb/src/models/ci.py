from sqlalchemy import Column, Integer, String, Enum, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base
import enum
from datetime import datetime

class CITipo(enum.Enum):
    HARDWARE = "Hardware"
    SOFTWARE = "Software"

class EstadoActual(enum.Enum):
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"

class NivelSeguridad(enum.Enum):
    ALTO = "Alto"
    MEDIO = "Medio"
    BAJO = "Bajo"

class Cumplimiento(enum.Enum):
    CUMPLE = "Cumple"
    NO_CUMPLE = "No Cumple"

class EstadoConfiguración(enum.Enum):
    APROBADO = "Aprobado"
    NO_APROBADO = "No Aprobado"

class CIRelacion(Base):
    __tablename__ = "ci_relaciones"
    id = Column(Integer, primary_key=True)
    ci_origen_id = Column(Integer, ForeignKey("cis.id"))
    ci_destino_id = Column(Integer, ForeignKey("cis.id"))
    tipo = Column(String)
    creado_en = Column(DateTime, default=datetime.utcnow)

class CI(Base):
    __tablename__ = "cis"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    tipo = Column(Enum(CITipo), nullable=False)
    descripción = Column(String)
    número_serie = Column(String)
    versión = Column(String)
    fecha_adquisición = Column(DateTime)
    estado_actual = Column(Enum(EstadoActual), nullable=False)
    relaciones = Column(JSON)  # Para padres/hijos
    ubicación_física = Column(String)
    propietario_responsable = Column(String)
    fecha_cambio = Column(DateTime)
    descripción_cambio = Column(String)
    documentación_relacionada = Column(String)
    enlaces_incidentes_problemas = Column(String)
    nivel_seguridad = Column(Enum(NivelSeguridad))
    cumplimiento = Column(Enum(Cumplimiento))
    estado_configuración = Column(Enum(EstadoConfiguración))
    número_licencia = Column(String)
    fecha_vencimiento = Column(DateTime)
    creado_en = Column(DateTime, default=datetime.utcnow)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    relaciones_obj = relationship("CIRelacion", 
                                foreign_keys=[CIRelacion.ci_origen_id],
                                back_populates="ci_origen")