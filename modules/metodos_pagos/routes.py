from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import schemas, crud
from database.session import get_db
from utils.logger import get_logger

router = APIRouter()
logger = get_logger("pagos.routes.metodos_pago")

@router.post("/", response_model=schemas.MetodoPago)
def crear_metodo_pago(metodo: schemas.MetodoPagoCreate, db: Session = Depends(get_db)):
    logger.info(f"Creando nuevo método de pago: {metodo.nombre_metodo}")
    return crud.create_metodo_pago(db, metodo)

@router.get("/", response_model=list[schemas.MetodoPago])
def listar_metodos_pagos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Listando métodos de pago (skip={skip}, limit={limit})")
    return crud.get_metodos_pagos(db, skip=skip, limit=limit)

@router.get("/{id_metodo_pago}", response_model=schemas.MetodoPago)
def obtener_metodo_pago(id_metodo_pago: int, db: Session = Depends(get_db)):
    logger.info(f"Buscando método de pago con ID {id_metodo_pago}")
    return crud.get_metodo_pago(db, id_metodo_pago)

@router.put("/{id_metodo_pago}", response_model=schemas.MetodoPago)
def actualizar_metodo_pago(id_metodo_pago: int, metodo: schemas.MetodoPagoCreate, db: Session = Depends(get_db)):
    logger.info(f"Actualizando método de pago con ID {id_metodo_pago}")
    return crud.update_metodo_pago(db, id_metodo_pago, metodo)

@router.delete("/{id_metodo_pago}", response_model=schemas.MetodoPago)
def eliminar_metodo_pago(id_metodo_pago: int, db: Session = Depends(get_db)):
    logger.info(f"Eliminando método de pago con ID {id_metodo_pago}")
    return crud.delete_metodo_pago(db, id_metodo_pago)