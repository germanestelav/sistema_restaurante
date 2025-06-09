from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db
from utils.logger import get_logger

logger = get_logger("historiales.router")

router = APIRouter()

@router.post("/", response_model=schemas.HistorialDetallePedido)
def create_historial(historial: schemas.HistorialDetallePedidoCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para crear historial: {historial}")
    resultado = crud.create_historial(db=db, historial=historial)
    logger.info(f"Historial creado con id: {resultado.id_historial}")
    return resultado

@router.get("/", response_model=list[schemas.HistorialDetallePedido])
def read_historiales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para listar historiales desde {skip} con límite {limit}")
    resultado = crud.get_historiales(db=db, skip=skip, limit=limit)
    logger.info(f"Se retornaron {len(resultado)} historiales")
    return resultado

@router.get("/{id_historial}", response_model=schemas.HistorialDetallePedido)
def read_historial(id_historial: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para obtener historial con id: {id_historial}")
    try:
        resultado = crud.get_historial(db=db, id_historial=id_historial)
        logger.info(f"Historial encontrado: {resultado}")
        return resultado
    except HTTPException as e:
        logger.error(f"Error al obtener historial con id {id_historial}: {e.detail}")
        raise e

@router.put("/{id_historial}", response_model=schemas.HistorialDetallePedido)
def update_historial(id_historial: int, historial: schemas.HistorialDetallePedidoCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para actualizar historial id {id_historial} con datos: {historial}")
    try:
        resultado = crud.update_historial(db=db, id_historial=id_historial, historial_data=historial)
        logger.info(f"Historial actualizado: {resultado}")
        return resultado
    except HTTPException as e:
        logger.error(f"Error al actualizar historial con id {id_historial}: {e.detail}")
        raise e

@router.delete("/{id_historial}", response_model=schemas.HistorialDetallePedido)
def delete_historial(id_historial: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para eliminar historial con id: {id_historial}")
    try:
        resultado = crud.delete_historial(db=db, id_historial=id_historial)
        logger.info(f"Historial eliminado: {resultado}")
        return resultado
    except HTTPException as e:
        logger.error(f"Error al eliminar historial con id {id_historial}: {e.detail}")
        raise e