from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db
from utils.logger import get_logger

router = APIRouter()
logger = get_logger("estado_pension.routes")

@router.post("/", response_model=schemas.EstadoPension)
def crear_estado_pension(estado: schemas.EstadoPensionCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para crear estado de pensión: {estado}")
    return crud.create_estado_pension(db=db, estado=estado)

@router.get("/", response_model=list[schemas.EstadoPension])
def listar_estados_pension(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para listar estados de pensión (skip={skip}, limit={limit})")
    return crud.get_estados_pension(db=db, skip=skip, limit=limit)

@router.get("/{id_estado_pension}", response_model=schemas.EstadoPension)
def obtener_estado_pension(id_estado_pension: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para obtener estado de pensión ID: {id_estado_pension}")
    return crud.get_estado_pension(db=db, id_estado_pension=id_estado_pension)

@router.put("/{id_estado_pension}", response_model=schemas.EstadoPension)
def actualizar_estado_pension(id_estado_pension: int, estado: schemas.EstadoPensionCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para actualizar estado de pensión ID: {id_estado_pension}")
    return crud.update_estado_pension(db=db, id_estado_pension=id_estado_pension, estado_update=estado)

@router.delete("/{id_estado_pension}", response_model=schemas.EstadoPension)
def eliminar_estado_pension(id_estado_pension: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para eliminar estado de pensión ID: {id_estado_pension}")
    return crud.delete_estado_pension(db=db, id_estado_pension=id_estado_pension)