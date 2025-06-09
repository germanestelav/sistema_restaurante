from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db
from utils.logger import get_logger

router = APIRouter()
logger = get_logger("pago_pension.routes")

@router.post("/", response_model=schemas.PagoPension)
def crear_pago_pension(pago: schemas.PagoPensionCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para crear pago de pensión: {pago}")
    return crud.create_pago_pension(db=db, pago=pago)

@router.get("/", response_model=list[schemas.PagoPension])
def listar_pagos_pension(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para listar pagos de pensión (skip={skip}, limit={limit})")
    return crud.get_pagos_pension(db=db, skip=skip, limit=limit)

@router.get("/{id_pago_pension}", response_model=schemas.PagoPension)
def obtener_pago_pension(id_pago_pension: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para obtener pago de pensión ID: {id_pago_pension}")
    return crud.get_pago_pension(db=db, id_pago_pension=id_pago_pension)

@router.put("/{id_pago_pension}", response_model=schemas.PagoPension)
def actualizar_pago_pension(id_pago_pension: int, pago: schemas.PagoPensionCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para actualizar pago de pensión ID: {id_pago_pension}")
    return crud.update_pago_pension(db=db, id_pago_pension=id_pago_pension, pago_update=pago)

@router.delete("/{id_pago_pension}", response_model=schemas.PagoPension)
def eliminar_pago_pension(id_pago_pension: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para eliminar pago de pensión ID: {id_pago_pension}")
    return crud.delete_pago_pension(db=db, id_pago_pension=id_pago_pension)