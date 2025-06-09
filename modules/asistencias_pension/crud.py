from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from utils.logger import get_logger

logger = get_logger("asistencias_pension.crud")

def create_asistencia_pension(db: Session, asistencia: schemas.AsistenciaPensionCreate):
    logger.info(f"Registrando asistencia para cliente pensión {asistencia.id_cliente_pension}")
    db_asistencia = models.AsistenciaPension(**asistencia.dict())
    db.add(db_asistencia)
    db.commit()
    db.refresh(db_asistencia)
    logger.info(f"Asistencia registrada con ID {db_asistencia.id_asistencia}")
    return db_asistencia

def get_asistencias_pension(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Obteniendo asistencias de pensión (skip={skip}, limit={limit})")
    return db.query(models.AsistenciaPension).offset(skip).limit(limit).all()

def get_asistencia_pension(db: Session, id_asistencia: int):
    logger.info(f"Buscando asistencia de pensión ID {id_asistencia}")
    asistencia = db.query(models.AsistenciaPension).filter(models.AsistenciaPension.id_asistencia == id_asistencia).first()
    if not asistencia:
        logger.warning(f"Asistencia de pensión ID {id_asistencia} no encontrada")
        raise HTTPException(status_code=404, detail="Asistencia de pensión no encontrada")
    return asistencia

def update_asistencia_pension(db: Session, id_asistencia: int, asistencia_update: schemas.AsistenciaPensionCreate):
    asistencia = db.query(models.AsistenciaPension).filter(models.AsistenciaPension.id_asistencia == id_asistencia).first()
    if not asistencia:
        logger.warning(f"Asistencia de pensión ID {id_asistencia} no encontrada para actualizar")
        raise HTTPException(status_code=404, detail="Asistencia de pensión no encontrada")
    for key, value in asistencia_update.dict().items():
        setattr(asistencia, key, value)
    db.commit()
    db.refresh(asistencia)
    logger.info(f"Asistencia de pensión ID {id_asistencia} actualizada")
    return asistencia

def delete_asistencia_pension(db: Session, id_asistencia: int):
    asistencia = db.query(models.AsistenciaPension).filter(models.AsistenciaPension.id_asistencia == id_asistencia).first()
    if not asistencia:
        logger.warning(f"Asistencia de pensión ID {id_asistencia} no encontrada para eliminar")
        raise HTTPException(status_code=404, detail="Asistencia de pensión no encontrada")
    db.delete(asistencia)
    db.commit()
    logger.info(f"Asistencia de pensión ID {id_asistencia} eliminada")
    return asistencia