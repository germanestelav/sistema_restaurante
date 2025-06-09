from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from utils.logger import get_logger

logger = get_logger("estado_pension.crud")

def create_estado_pension(db: Session, estado: schemas.EstadoPensionCreate):
    logger.info(f"Creando estado de pensión: {estado.nombre_estado}")
    db_estado = models.EstadoPension(**estado.dict())
    db.add(db_estado)
    db.commit()
    db.refresh(db_estado)
    logger.info(f"Estado de pensión creado con ID {db_estado.id_estado_pension}")
    return db_estado

def get_estados_pension(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Obteniendo estados de pensión (skip={skip}, limit={limit})")
    return db.query(models.EstadoPension).offset(skip).limit(limit).all()

def get_estado_pension(db: Session, id_estado_pension: int):
    logger.info(f"Buscando estado de pensión ID {id_estado_pension}")
    estado = db.query(models.EstadoPension).filter(models.EstadoPension.id_estado_pension == id_estado_pension).first()
    if not estado:
        logger.warning(f"Estado de pensión ID {id_estado_pension} no encontrado")
        raise HTTPException(status_code=404, detail="Estado de pensión no encontrado")
    return estado

def update_estado_pension(db: Session, id_estado_pension: int, estado_update: schemas.EstadoPensionCreate):
    logger.info(f"Actualizando estado de pensión ID {id_estado_pension}")
    estado = db.query(models.EstadoPension).filter(models.EstadoPension.id_estado_pension == id_estado_pension).first()
    if not estado:
        logger.warning(f"Estado de pensión ID {id_estado_pension} no encontrado para actualizar")
        raise HTTPException(status_code=404, detail="Estado de pensión no encontrado")
    for key, value in estado_update.dict().items():
        setattr(estado, key, value)
    db.commit()
    db.refresh(estado)
    logger.info(f"Estado de pensión ID {id_estado_pension} actualizado")
    return estado

def delete_estado_pension(db: Session, id_estado_pension: int):
    logger.info(f"Eliminando estado de pensión ID {id_estado_pension}")
    estado = db.query(models.EstadoPension).filter(models.EstadoPension.id_estado_pension == id_estado_pension).first()
    if not estado:
        logger.warning(f"Estado de pensión ID {id_estado_pension} no encontrado para eliminar")
        raise HTTPException(status_code=404, detail="Estado de pensión no encontrado")
    db.delete(estado)
    db.commit()
    logger.info(f"Estado de pensión ID {id_estado_pension} eliminado")
    return estado