from sqlalchemy.orm import Session
from .models import Pago
from .schemas import PagoCreate
from fastapi import HTTPException
from datetime import datetime
from modules.pedidos.models import Pedido
from modules.mesas.models import Mesa
from modules.detalle_pedidos.models import DetallePedido
from utils.logger import get_logger

logger = get_logger("pagos.crud")


def create_pago(db: Session, pago: PagoCreate):
    logger.info(f"Creando pago para pedido ID {pago.id_pedido}")
    # Calcular el monto total sumando cantidad * precio_unitario de cada detalle
    detalles = db.query(DetallePedido).filter(DetallePedido.id_pedido == pago.id_pedido).all()
    monto_total = sum(detalle.cantidad * float(detalle.precio_unitario) for detalle in detalles)

    db_pago = Pago(
        id_pedido=pago.id_pedido,
        monto_total=monto_total,
        id_metodo_pago=pago.id_metodo_pago,
        fecha_pago=datetime.now()
    )
    db.add(db_pago)
    db.commit()
    db.refresh(db_pago)

    # Liberar la mesa asociada al pedido pagado
    pedido = db.query(Pedido).filter(Pedido.id_pedido == pago.id_pedido).first()
    if pedido:
        mesa = db.query(Mesa).filter(Mesa.id_mesa == pedido.id_mesa).first()
        if mesa:
            mesa.estado = "libre"
            db.commit()
            db.refresh(mesa)
    logger.info(f"Pago creado con ID {db_pago.id_pago} para pedido ID {pago.id_pedido}")
    return db_pago

def get_pagos(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Obteniendo pagos, skip={skip}, limit={limit}")
    return db.query(Pago).offset(skip).limit(limit).all()

def get_pago(db: Session, id_pago: int):
    logger.info(f"Buscando pago ID {id_pago}")
    pago = db.query(Pago).filter(Pago.id_pago == id_pago).first()
    if not pago:
        logger.error(f"Pago ID {id_pago} no encontrado")
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago

def update_pago(db: Session, id_pago: int, pago_data: PagoCreate):
    pago = db.query(Pago).filter(Pago.id_pago == id_pago).first()
    if not pago:
        logger.warning(f"No se encontró el pago con ID {id_pago}")
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    
    # Recalcular el monto total como en create_pago
    detalles = db.query(DetallePedido).filter(DetallePedido.id_pedido == pago_data.id_pedido).all()
    monto_total = sum(detalle.cantidad * float(detalle.precio_unitario) for detalle in detalles)

    pago.id_pedido = pago_data.id_pedido
    pago.monto_total = monto_total
    pago.id_metodo_pago = pago_data.id_metodo_pago
    db.commit()
    db.refresh(pago)

    logger.info(f"Pago actualizado correctamente con ID {id_pago}")
    return pago

def delete_pago(db: Session, id_pago: int):
    logger.info(f"Eliminando pago ID {id_pago}")
    pago = db.query(Pago).filter(Pago.id_pago == id_pago).first()
    if not pago:
        logger.error(f"Pago ID {id_pago} no encontrado para eliminar")
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    db.delete(pago)
    db.commit()
    logger.info(f"Pago ID {id_pago} eliminado correctamente")
    return pago
