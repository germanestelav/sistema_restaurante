from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db
from utils.logger import get_logger

logger = get_logger("rol.routes")
router = APIRouter()

@router.post("/", response_model=schemas.Rol)
def create_rol(rol: schemas.RolCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para crear rol: {rol}")
    return crud.create_rol(db=db, rol=rol)

@router.get("/", response_model=list[schemas.Rol])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para obtener todos los roles (skip={skip}, limit={limit})")
    return crud.get_roles(db=db, skip=skip, limit=limit)

@router.get("/{id_rol}", response_model=schemas.Rol)
def read_rol(id_rol: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para obtener rol con ID: {id_rol}")
    return crud.get_rol(db=db, id_rol=id_rol)

@router.put("/{id_rol}", response_model=schemas.Rol)
def update_rol(id_rol: int, rol: schemas.RolCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para actualizar rol con ID: {id_rol} - Nuevos datos: {rol}")
    return crud.update_rol(db=db, id_rol=id_rol, rol_data=rol)

@router.delete("/{id_rol}", response_model=schemas.Rol)
def delete_rol(id_rol: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para eliminar rol con ID: {id_rol}")
    return crud.delete_rol(db=db, id_rol=id_rol)
