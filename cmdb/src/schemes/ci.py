from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from src.models.ci import CITipo, EstadoActual, NivelSeguridad, Cumplimiento, EstadoConfiguración

class CIBase(BaseModel):
    nombre: str
    tipo: CITipo
    descripción: Optional[str] = None
    número_serie: Optional[str] = None
    versión: Optional[str] = None
    fecha_adquisición: Optional[datetime] = None
    estado_actual: EstadoActual
    relaciones: Optional[dict] = None
    ubicación_física: Optional[str] = None
    propietario_responsable: Optional[str] = None
    fecha_cambio: Optional[datetime] = None
    descripción_cambio: Optional[str] = None
    documentación_relacionada: Optional[str] = None
    enlaces_incidentes_problemas: Optional[str] = None
    nivel_seguridad: Optional[NivelSeguridad] = None
    cumplimiento: Optional[Cumplimiento] = None
    estado_configuración: Optional[EstadoConfiguración] = None
    número_licencia: Optional[str] = None
    fecha_vencimiento: Optional[datetime] = None

class CICrear(CIBase):
    pass

class CIActualizar(CIBase):
    nombre: Optional[str] = None
    tipo: Optional[CITipo] = None
    estado_actual: Optional[EstadoActual] = None

class CIRespuesta(CIBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        orm_mode = True

class CIRelacionBase(BaseModel):
    ci_origen_id: int
    ci_destino_id: int
    tipo: str

class CIRelacionCrear(CIRelacionBase):
    pass

class CIRelacionRespuesta(CIRelacionBase):
    id: int
    creado_en: datetime

    class Config:
        orm_mode = True