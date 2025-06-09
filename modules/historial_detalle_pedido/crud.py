from sqlalchemy.orm import Session
from .models import HistorialDetallePedido
from .schemas import HistorialDetallePedidoCreate
from fastapi import HTTPException
from utils.logger import get_logger

logger = get_logger("historiales.crud")

def create_historial(db: Session, historial: HistorialDetallePedidoCreate):
    db_historial = HistorialDetallePedido(
        id_detalle_original=historial.id_detalle_original,
        id_producto_anterior=historial.id_producto_anterior,
        cantidad_anterior=historial.cantidad_anterior,
        precio_unitario_anterior=historial.precio_unitario_anterior,
        motivo=historial.motivo
    )
    db.add(db_historial)
    db.commit()
    db.refresh(db_historial)
    logger.info(f"Historial creado: {db_historial}")
    return db_historial

def get_historiales(db: Session, skip: int = 0, limit: int = 100):
    historiales = db.query(HistorialDetallePedido).offset(skip).limit(limit).all()
    logger.info(f"Historiales listados desde {skip} hasta {skip + limit}, total: {len(historiales)}")
    return historiales

def get_historial(db: Session, id_historial: int):
    historial = db.query(HistorialDetallePedido).filter(HistorialDetallePedido.id_historial == id_historial).first()
    if not historial:
        logger.error(f"Historial no encontrado con id: {id_historial}")
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    logger.info(f"Historial obtenido: {historial}")
    return historial

def update_historial(db: Session, id_historial: int, historial_data: HistorialDetallePedidoCreate):
    historial = db.query(HistorialDetallePedido).filter(HistorialDetallePedido.id_historial == id_historial).first()
    if not historial:
        logger.error(f"Intento de actualizar historial no encontrado con id: {id_historial}")
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    historial.id_detalle_original = historial_data.id_detalle_original
    historial.id_producto_anterior = historial_data.id_producto_anterior
    historial.cantidad_anterior = historial_data.cantidad_anterior
    historial.precio_unitario_anterior = historial_data.precio_unitario_anterior
    historial.motivo = historial_data.motivo
    db.commit()
    db.refresh(historial)
    logger.info(f"Historial actualizado: {historial}")
    return historial

def delete_historial(db: Session, id_historial: int):
    historial = db.query(HistorialDetallePedido).filter(HistorialDetallePedido.id_historial == id_historial).first()
    if not historial:
        logger.error(f"Intento de eliminar historial no encontrado con id: {id_historial}")
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    db.delete(historial)
    db.commit()
    logger.info(f"Historial eliminado: {historial}")
    return historial
