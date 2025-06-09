from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from utils.logger import get_logger

logger = get_logger("clientes_pension.crud")

def create_cliente_pension(db: Session, cliente: schemas.ClientePensionCreate):
    logger.info(f"Creando cliente de pensión: {cliente.nombre} {cliente.apellido}")
    db_cliente = models.ClientePension(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    logger.info(f"Cliente de pensión creado con ID {db_cliente.id_cliente_pension}")
    return db_cliente

def get_clientes_pension(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Obteniendo clientes de pensión (skip={skip}, limit={limit})")
    return db.query(models.ClientePension).offset(skip).limit(limit).all()

def get_cliente_pension(db: Session, id_cliente_pension: int):
    logger.info(f"Buscando cliente de pensión ID {id_cliente_pension}")
    cliente = db.query(models.ClientePension).filter(models.ClientePension.id_cliente_pension == id_cliente_pension).first()
    if not cliente:
        logger.warning(f"Cliente de pensión ID {id_cliente_pension} no encontrado")
        raise HTTPException(status_code=404, detail="Cliente de pensión no encontrado")
    return cliente

def update_cliente_pension(db: Session, id_cliente_pension: int, cliente_update: schemas.ClientePensionCreate):
    cliente = db.query(models.ClientePension).filter(models.ClientePension.id_cliente_pension == id_cliente_pension).first()
    if not cliente:
        logger.warning(f"Cliente de pensión ID {id_cliente_pension} no encontrado para actualizar")
        raise HTTPException(status_code=404, detail="Cliente de pensión no encontrado")
    for key, value in cliente_update.dict().items():
        setattr(cliente, key, value)
    db.commit()
    db.refresh(cliente)
    logger.info(f"Cliente de pensión ID {id_cliente_pension} actualizado")
    return cliente

def delete_cliente_pension(db: Session, id_cliente_pension: int):
    cliente = db.query(models.ClientePension).filter(models.ClientePension.id_cliente_pension == id_cliente_pension).first()
    if not cliente:
        logger.warning(f"Cliente de pensión ID {id_cliente_pension} no encontrado para eliminar")
        raise HTTPException(status_code=404, detail="Cliente de pensión no encontrado")
    db.delete(cliente)
    db.commit()
    logger.info(f"Cliente de pensión ID {id_cliente_pension} eliminado")
    return cliente