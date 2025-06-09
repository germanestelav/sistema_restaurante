from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from utils.logger import get_logger

logger = get_logger("mesas.crud")

# Crear una nueva mesa
def create_mesa(db: Session, mesa: schemas.MesaCreate):
    db_mesa = models.Mesa(
        numero=mesa.numero,
        capacidad=mesa.capacidad,
        estado=mesa.estado
    )
    db.add(db_mesa)
    db.commit()
    db.refresh(db_mesa)
    logger.info(f"Mesa creada: {db_mesa}")
    return db_mesa

# Obtener todas las mesas
def get_mesas(db: Session, skip: int = 0, limit: int = 100):
    mesas = db.query(models.Mesa).offset(skip).limit(limit).all()
    logger.info(f"{len(mesas)} mesas obtenidas (skip={skip}, limit={limit})")
    return mesas

# Obtener una mesa por ID
# Obtener una mesa por ID
def get_mesa(db: Session, mesa_id: int):
    mesa = db.query(models.Mesa).filter(models.Mesa.id_mesa == mesa_id).first()
    if mesa:
        logger.info(f"Mesa obtenida: {mesa}")
    else:
        logger.warning(f"Mesa con ID {mesa_id} no encontrada")
    return mesa

# Actualizar una mesa
def update_mesa(db: Session, mesa_id: int, mesa: schemas.MesaCreate):
    db_mesa = db.query(models.Mesa).filter(models.Mesa.id_mesa == mesa_id).first()
    if not db_mesa:
        logger.warning(f"No se encontró la mesa con ID {mesa_id} para actualizar")
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    db_mesa.numero = mesa.numero
    db_mesa.capacidad = mesa.capacidad
    db_mesa.estado = mesa.estado
    db.commit()
    db.refresh(db_mesa)
    logger.info(f"Mesa actualizada: {db_mesa}")
    return db_mesa

# Eliminar una mesa
def delete_mesa(db: Session, mesa_id: int):
    db_mesa = db.query(models.Mesa).filter(models.Mesa.id_mesa == mesa_id).first()
    if not db_mesa:
        logger.warning(f"No se encontró la mesa con ID {mesa_id} para eliminar")
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    db.delete(db_mesa)
    db.commit()
    logger.info(f"Mesa eliminada: {db_mesa}")
    return db_mesa
