from sqlalchemy.orm import Session
from .models import MetodoPago
from .schemas import MetodoPagoCreate
from fastapi import HTTPException
from utils.logger import get_logger

logger = get_logger("pagos.crud.metodos_pago")

def create_metodo_pago(db: Session, metodo: MetodoPagoCreate):
    db_metodo = MetodoPago(nombre_metodo=metodo.nombre_metodo)
    db.add(db_metodo)
    db.commit()
    db.refresh(db_metodo)
    logger.info(f"Nuevo método de pago creado con ID {db_metodo.id_metodo_pago}")
    return db_metodo

def get_metodos_pagos(db: Session, skip: int = 0, limit: int = 100):
    metodos = db.query(MetodoPago).offset(skip).limit(limit).all()
    logger.info(f"Se obtuvieron {len(metodos)} métodos de pago")
    return metodos

def get_metodo_pago(db: Session, id_metodo_pago: int):
    metodo = db.query(MetodoPago).filter(MetodoPago.id_metodo_pago == id_metodo_pago).first()
    if not metodo:
        logger.warning(f"Método de pago con ID {id_metodo_pago} no encontrado")
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")
    return metodo

def update_metodo_pago(db: Session, id_metodo_pago: int, metodo_data: MetodoPagoCreate):
    metodo = db.query(MetodoPago).filter(MetodoPago.id_metodo_pago == id_metodo_pago).first()
    if not metodo:
        logger.warning(f"No se pudo actualizar. Método de pago con ID {id_metodo_pago} no encontrado")
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")
    metodo.nombre_metodo = metodo_data.nombre_metodo
    db.commit()
    db.refresh(metodo)
    return metodo

def delete_metodo_pago(db: Session, id_metodo_pago: int):
    metodo = db.query(MetodoPago).filter(MetodoPago.id_metodo_pago == id_metodo_pago).first()
    if not metodo:
        logger.warning(f"No se pudo eliminar. Método de pago con ID {id_metodo_pago} no encontrado")
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")
    db.delete(metodo)
    db.commit()
    logger.info(f"Método de pago eliminado con ID {id_metodo_pago}")
    return metodo