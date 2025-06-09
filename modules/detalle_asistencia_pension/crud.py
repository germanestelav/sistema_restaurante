from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from utils.logger import get_logger
from modules.productos.models import Producto

logger = get_logger("detalle_asistencia_pension.crud")

def create_detalle_asistencia_pension(db: Session, detalle: schemas.DetalleAsistenciaPensionCreate):
    logger.info(f"Registrando detalle de asistencia: asistencia {detalle.id_asistencia}, producto {detalle.id_producto}")
    db_detalle = models.DetalleAsistenciaPension(**detalle.dict())
    db.add(db_detalle)

    # Descontar stock del producto
    producto = db.query(Producto).filter(Producto.id_producto == detalle.id_producto).first()
    if producto:
        if producto.stock < detalle.cantidad:
            logger.warning(f"Stock insuficiente para el producto ID {detalle.id_producto}")
            raise HTTPException(status_code=400, detail="Stock insuficiente para el producto")
        producto.stock -= detalle.cantidad
        logger.info(f"Stock del producto ID {detalle.id_producto} actualizado a {producto.stock}")
    else:
        logger.warning(f"Producto ID {detalle.id_producto} no encontrado")
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.commit()
    db.refresh(db_detalle)
    logger.info(f"Detalle de asistencia registrado con ID {db_detalle.id_detalle_asistencia}")
    return db_detalle

def get_detalles_asistencia_pension(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Obteniendo detalles de asistencia de pensión (skip={skip}, limit={limit})")
    return db.query(models.DetalleAsistenciaPension).offset(skip).limit(limit).all()

def get_detalle_asistencia_pension(db: Session, id_detalle_asistencia: int):
    logger.info(f"Buscando detalle de asistencia ID {id_detalle_asistencia}")
    detalle = db.query(models.DetalleAsistenciaPension).filter(models.DetalleAsistenciaPension.id_detalle_asistencia == id_detalle_asistencia).first()
    if not detalle:
        logger.warning(f"Detalle de asistencia ID {id_detalle_asistencia} no encontrado")
        raise HTTPException(status_code=404, detail="Detalle de asistencia no encontrado")
    return detalle

def update_detalle_asistencia_pension(db: Session, id_detalle_asistencia: int, detalle_update: schemas.DetalleAsistenciaPensionCreate):
    detalle = db.query(models.DetalleAsistenciaPension).filter(models.DetalleAsistenciaPension.id_detalle_asistencia == id_detalle_asistencia).first()
    if not detalle:
        logger.warning(f"Detalle de asistencia ID {id_detalle_asistencia} no encontrado para actualizar")
        raise HTTPException(status_code=404, detail="Detalle de asistencia no encontrado")

    # Devolver stock al producto anterior
    producto_anterior = db.query(Producto).filter(Producto.id_producto == detalle.id_producto).first()
    if producto_anterior:
        producto_anterior.stock += detalle.cantidad

    # Descontar stock al producto nuevo
    producto_nuevo = db.query(Producto).filter(Producto.id_producto == detalle_update.id_producto).first()
    if producto_nuevo:
        if producto_nuevo.stock < detalle_update.cantidad:
            logger.warning(f"Stock insuficiente para el producto ID {detalle_update.id_producto}")
            raise HTTPException(status_code=400, detail="Stock insuficiente para el producto")
        producto_nuevo.stock -= detalle_update.cantidad
    else:
        logger.warning(f"Producto ID {detalle_update.id_producto} no encontrado")
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Actualiza el detalle
    for key, value in detalle_update.dict().items():
        setattr(detalle, key, value)
    db.commit()
    db.refresh(detalle)
    logger.info(f"Detalle de asistencia ID {id_detalle_asistencia} actualizado")
    return detalle

def delete_detalle_asistencia_pension(db: Session, id_detalle_asistencia: int):
    detalle = db.query(models.DetalleAsistenciaPension).filter(models.DetalleAsistenciaPension.id_detalle_asistencia == id_detalle_asistencia).first()
    if not detalle:
        logger.warning(f"Detalle de asistencia ID {id_detalle_asistencia} no encontrado para eliminar")
        raise HTTPException(status_code=404, detail="Detalle de asistencia no encontrado")
    
    # Devolver stock al producto
    producto = db.query(Producto).filter(Producto.id_producto == detalle.id_producto).first()
    if producto:
        producto.stock += detalle.cantidad

    db.delete(detalle)
    db.commit()
    logger.info(f"Detalle de asistencia ID {id_detalle_asistencia} eliminado")
    return detalle