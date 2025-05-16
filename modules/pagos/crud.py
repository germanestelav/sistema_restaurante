from sqlalchemy.orm import Session
from .models import Pago
from .schemas import PagoCreate
from fastapi import HTTPException

def create_pago(db: Session, pago: PagoCreate):
    db_pago = Pago(
        id_pedido=pago.id_pedido,
        monto_total=pago.monto_total,
        metodo_pago=pago.metodo_pago,
    )
    db.add(db_pago)
    db.commit()
    db.refresh(db_pago)
    return db_pago

def get_pagos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Pago).offset(skip).limit(limit).all()

def get_pago(db: Session, id_pago: int):
    pago = db.query(Pago).filter(Pago.id_pago == id_pago).first()
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago

def update_pago(db: Session, id_pago: int, pago_data: PagoCreate):
    pago = db.query(Pago).filter(Pago.id_pago == id_pago).first()
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    pago.id_pedido = pago_data.id_pedido
    pago.monto_total = pago_data.monto_total
    pago.metodo_pago = pago_data.metodo_pago
    db.commit()
    db.refresh(pago)
    return pago

def delete_pago(db: Session, id_pago: int):
    pago = db.query(Pago).filter(Pago.id_pago == id_pago).first()
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    db.delete(pago)
    db.commit()
    return pago
