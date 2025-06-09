from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db
from utils.logger import get_logger

router = APIRouter()
logger = get_logger("asistencia_pension.routes")

@router.post("/", response_model=schemas.AsistenciaPension)
def crear_asistencia_pension(asistencia: schemas.AsistenciaPensionCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para crear asistencia pensión: {asistencia}")
    return crud.create_asistencia_pension(db=db, asistencia=asistencia)

@router.get("/", response_model=list[schemas.AsistenciaPension])
def listar_asistencias_pension(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para listar asistencias pensión (skip={skip}, limit={limit})")
    return crud.get_asistencias_pension(db=db, skip=skip, limit=limit)

@router.get("/{id_asistencia}", response_model=schemas.AsistenciaPension)
def obtener_asistencia_pension(id_asistencia: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para obtener asistencia pensión ID: {id_asistencia}")
    return crud.get_asistencia_pension(db=db, id_asistencia=id_asistencia)

@router.put("/{id_asistencia}", response_model=schemas.AsistenciaPension)
def actualizar_asistencia_pension(id_asistencia: int, asistencia: schemas.AsistenciaPensionCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para actualizar asistencia pensión ID: {id_asistencia}")
    return crud.update_asistencia_pension(db=db, id_asistencia=id_asistencia, asistencia_update=asistencia)

@router.delete("/{id_asistencia}", response_model=schemas.AsistenciaPension)
def eliminar_asistencia_pension(id_asistencia: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para eliminar asistencia pensión ID: {id_asistencia}")
    return crud.delete_asistencia_pension(db=db, id_asistencia=id_asistencia)
