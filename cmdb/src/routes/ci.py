from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.db import get_db
from src.models.ci import CI, CIRelacion
from src.models.audit import AuditLog
from src.schemas.ci import CICrear, CIActualizar, CIRespuesta, CIRelacionCrear, CIRelacionRespuesta

router = APIRouter()

@router.post("/cis", response_model=CIRespuesta)
def crear_ci(ci: CICrear, db: Session = Depends(get_db)):
    db_ci = CI(**ci.dict())
    db.add(db_ci)
    db.commit()
    db.refresh(db_ci)
    
    audit = AuditLog(ci_id=db_ci.id, acción="CREAR", valor_nuevo=ci.dict())
    db.add(audit)
    db.commit()
    
    return db_ci

@router.get("/cis", response_model=List[CIRespuesta])
def obtener_cis(
    tipo: str = None,
    estado_actual: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(CI)
    if tipo:
        query = query.filter(CI.tipo == tipo)
    if estado_actual:
        query = query.filter(CI.estado_actual == estado_actual)
    return query.all()

@router.get("/cis/{ci_id}", response_model=CIRespuesta)
def obtener_ci(ci_id: int, db: Session = Depends(get_db)):
    ci = db.query(CI).filter(CI.id == ci_id).first()
    if not ci:
        raise HTTPException(status_code=404, detail="CI no encontrado")
    return ci

@router.put("/cis/{ci_id}", response_model=CIRespuesta)
def actualizar_ci(ci_id: int, ci_actualizar: CIActualizar, db: Session = Depends(get_db)):
    ci = db.query(CI).filter(CI.id == ci_id).first()
    if not ci:
        raise HTTPException(status_code=404, detail="CI no encontrado")
    
    valor_anterior = {k: v for k, v in ci.__dict__.items() if k in ci_actualizar.dict(exclude_unset=True)}
    for key, value in ci_actualizar.dict(exclude_unset=True).items():
        setattr(ci, key, value)
    
    db.commit()
    db.refresh(ci)
    
    audit = AuditLog(ci_id=ci_id, acción="ACTUALIZAR", valor_anterior=valor_anterior, valor_nuevo=ci_actualizar.dict(exclude_unset=True))
    db.add(audit)
    db.commit()
    
    return ci

@router.delete("/cis/{ci_id}")
def eliminar_ci(ci_id: int, db: Session = Depends(get_db)):
    ci = db.query(CI).filter(CI.id == ci_id).first()
    if not ci:
        raise HTTPException(status_code=404, detail="CI no encontrado")
    
    audit = AuditLog(ci_id=ci_id, acción="ELIMINAR", valor_anterior={k: v for k, v in ci.__dict__.items()})
    db.add(audit)
    db.delete(ci)
    db.commit()
    return {"mensaje": "CI eliminado"}

@router.post("/relaciones", response_model=CIRelacionRespuesta)
def crear_relacion(relacion: CIRelacionCrear, db: Session = Depends(get_db)):
    db_relacion = CIRelacion(**relacion.dict())
    db.add(db_relacion)
    db.commit()
    db.refresh(db_relacion)
    return db_relacion