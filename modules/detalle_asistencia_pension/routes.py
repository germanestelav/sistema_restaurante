from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db
from utils.logger import get_logger

router = APIRouter()
logger = get_logger("detalle_asistencia_pension.routes")

@router.post("/", response_model=schemas.DetalleAsistenciaPension)
def crear_detalle_asistencia_pension(detalle: schemas.DetalleAsistenciaPensionCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para crear detalle de asistencia a pensión: {detalle}")
    return crud.create_detalle_asistencia_pension(db=db, detalle=detalle)

@router.get("/", response_model=list[schemas.DetalleAsistenciaPension])
def listar_detalles_asistencia_pension(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para listar detalles de asistencia (skip={skip}, limit={limit})")
    return crud.get_detalles_asistencia_pension(db=db, skip=skip, limit=limit)

@router.get("/{id_detalle_asistencia}", response_model=schemas.DetalleAsistenciaPension)
def obtener_detalle_asistencia_pension(id_detalle_asistencia: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para obtener detalle de asistencia ID: {id_detalle_asistencia}")
    return crud.get_detalle_asistencia_pension(db=db, id_detalle_asistencia=id_detalle_asistencia)

@router.put("/{id_detalle_asistencia}", response_model=schemas.DetalleAsistenciaPension)
def actualizar_detalle_asistencia_pension(id_detalle_asistencia: int, detalle: schemas.DetalleAsistenciaPensionCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para actualizar detalle de asistencia ID: {id_detalle_asistencia}")
    return crud.update_detalle_asistencia_pension(db=db, id_detalle_asistencia=id_detalle_asistencia, detalle_update=detalle)

@router.delete("/{id_detalle_asistencia}", response_model=schemas.DetalleAsistenciaPension)
def eliminar_detalle_asistencia_pension(id_detalle_asistencia: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para eliminar detalle de asistencia ID: {id_detalle_asistencia}")
    return crud.delete_detalle_asistencia_pension(db=db, id_detalle_asistencia=id_detalle_asistencia)