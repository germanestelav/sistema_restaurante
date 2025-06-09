from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db
from utils.logger import get_logger

logger = get_logger("pagos.router")

router = APIRouter()

@router.post("/", response_model=schemas.Pago)
def create_pago(pago: schemas.PagoCreate, db: Session = Depends(get_db)):
    logger.info(f"Crear pago para pedido ID {pago.id_pedido}")
    return crud.create_pago(db=db, pago=pago)

@router.get("/", response_model=list[schemas.Pago])
def read_pagos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Listar pagos skip={skip}, limit={limit}")
    return crud.get_pagos(db=db, skip=skip, limit=limit)

@router.get("/{id_pago}", response_model=schemas.Pago)
def read_pago(id_pago: int, db: Session = Depends(get_db)):
    logger.info(f"Pagos/{id_pago} - Obtener pago")
    return crud.get_pago(db=db, id_pago=id_pago)

@router.put("/{id_pago}", response_model=schemas.Pago)
def update_pago(id_pago: int, pago: schemas.PagoCreate, db: Session = Depends(get_db)):
    logger.info(f"Pagos/{id_pago} - Actualizar pago")
    return crud.update_pago(db=db, id_pago=id_pago, pago_data=pago)

@router.delete("/{id_pago}", response_model=schemas.Pago)
def delete_pago(id_pago: int, db: Session = Depends(get_db)):
    logger.info(f"Pagos/{id_pago} - Eliminar pago")
    return crud.delete_pago(db=db, id_pago=id_pago)
