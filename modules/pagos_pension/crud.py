from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from utils.logger import get_logger

logger = get_logger("pagos_pension.crud")

def create_pago_pension(db: Session, pago: schemas.PagoPensionCreate):
    logger.info(f"Creando pago de pensión para cliente {pago.id_cliente_pension}")
    db_pago = models.PagoPension(**pago.dict())
    db.add(db_pago)
    db.commit()
    db.refresh(db_pago)
    logger.info(f"Pago de pensión creado con ID {db_pago.id_pago_pension}")
    return db_pago

def get_pagos_pension(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Obteniendo pagos de pensión (skip={skip}, limit={limit})")
    return db.query(models.PagoPension).offset(skip).limit(limit).all()

def get_pago_pension(db: Session, id_pago_pension: int):
    logger.info(f"Buscando pago de pensión ID {id_pago_pension}")
    pago = db.query(models.PagoPension).filter(models.PagoPension.id_pago_pension == id_pago_pension).first()
    if not pago:
        logger.warning(f"Pago de pensión ID {id_pago_pension} no encontrado")
        raise HTTPException(status_code=404, detail="Pago de pensión no encontrado")
    return pago

def update_pago_pension(db: Session, id_pago_pension: int, pago_update: schemas.PagoPensionCreate):
    logger.info(f"Actualizando pago de pensión ID {id_pago_pension}")
    pago = db.query(models.PagoPension).filter(models.PagoPension.id_pago_pension == id_pago_pension).first()
    if not pago:
        logger.warning(f"Pago de pensión ID {id_pago_pension} no encontrado para actualizar")
        raise HTTPException(status_code=404, detail="Pago de pensión no encontrado")
    for key, value in pago_update.dict().items():
        setattr(pago, key, value)
    db.commit()
    db.refresh(pago)
    logger.info(f"Pago de pensión ID {id_pago_pension} actualizado")
    return pago

def delete_pago_pension(db: Session, id_pago_pension: int):
    logger.info(f"Eliminando pago de pensión ID {id_pago_pension}")
    pago = db.query(models.PagoPension).filter(models.PagoPension.id_pago_pension == id_pago_pension).first()
    if not pago:
        logger.warning(f"Pago de pensión ID {id_pago_pension} no encontrado para eliminar")
        raise HTTPException(status_code=404, detail="Pago de pensión no encontrado")
    db.delete(pago)
    db.commit()
    logger.info(f"Pago de pensión ID {id_pago_pension} eliminado")
    return pago