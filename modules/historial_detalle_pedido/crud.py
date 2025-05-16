from sqlalchemy.orm import Session
from .models import HistorialDetallePedido
from .schemas import HistorialDetallePedidoCreate
from fastapi import HTTPException

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
    return db_historial

def get_historiales(db: Session, skip: int = 0, limit: int = 100):
    return db.query(HistorialDetallePedido).offset(skip).limit(limit).all()

def get_historial(db: Session, id_historial: int):
    historial = db.query(HistorialDetallePedido).filter(HistorialDetallePedido.id_historial == id_historial).first()
    if not historial:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    return historial

def update_historial(db: Session, id_historial: int, historial_data: HistorialDetallePedidoCreate):
    historial = db.query(HistorialDetallePedido).filter(HistorialDetallePedido.id_historial == id_historial).first()
    if not historial:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    historial.id_detalle_original = historial_data.id_detalle_original
    historial.id_producto_anterior = historial_data.id_producto_anterior
    historial.cantidad_anterior = historial_data.cantidad_anterior
    historial.precio_unitario_anterior = historial_data.precio_unitario_anterior
    historial.motivo = historial_data.motivo
    db.commit()
    db.refresh(historial)
    return historial

def delete_historial(db: Session, id_historial: int):
    historial = db.query(HistorialDetallePedido).filter(HistorialDetallePedido.id_historial == id_historial).first()
    if not historial:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    db.delete(historial)
    db.commit()
    return historial
