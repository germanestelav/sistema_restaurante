from sqlalchemy.orm import Session
from .models import EstadoPedido
from .schemas import EstadoPedidoCreate
from fastapi import HTTPException
from utils.logger import get_logger

logger = get_logger("estados_pedidos.crud")

def create_estado_pedido(db: Session, estado: EstadoPedidoCreate):
    db_estado = EstadoPedido(nombre_estado=estado.nombre_estado)
    db.add(db_estado)
    db.commit()
    db.refresh(db_estado)
    logger.info(f"Estado de pedido creado: {db_estado.id_estado_pedido}")
    return db_estado

def get_estados_pedidos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(EstadoPedido).offset(skip).limit(limit).all()

def get_estado_pedido(db: Session, id_estado_pedido: int):
    estado = db.query(EstadoPedido).filter(EstadoPedido.id_estado_pedido == id_estado_pedido).first()
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return estado

def update_estado_pedido(db: Session, id_estado_pedido: int, estado_data: EstadoPedidoCreate):
    estado = db.query(EstadoPedido).filter(EstadoPedido.id_estado_pedido == id_estado_pedido).first()
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    estado.nombre_estado = estado_data.nombre_estado
    db.commit()
    db.refresh(estado)
    return estado

def delete_estado_pedido(db: Session, id_estado_pedido: int):
    estado = db.query(EstadoPedido).filter(EstadoPedido.id_estado_pedido == id_estado_pedido).first()
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    db.delete(estado)
    db.commit()
    return estado