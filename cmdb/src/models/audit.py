from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from src.database.db import Base
from datetime import datetime

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    ci_id = Column(Integer, ForeignKey("cis.id"))
    acción = Column(String, nullable=False)
    valor_anterior = Column(JSON)
    valor_nuevo = Column(JSON)
    creado_en = Column(DateTime, default=datetime.utcnow)