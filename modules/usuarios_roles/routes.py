from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db
from utils.logger import get_logger

router = APIRouter()
logger = get_logger("usuario_rol.routes")

@router.post("/", response_model=schemas.UsuarioRol)
def create_usuario_rol(usuario_rol: schemas.UsuarioRolCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para crear UsuarioRol (id_usuario={usuario_rol.id_usuario}, id_rol={usuario_rol.id_rol})")
    return crud.create_usuario_rol(db=db, usuario_rol=usuario_rol)

@router.get("/", response_model=list[schemas.UsuarioRol])
def read_usuario_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para obtener lista de UsuarioRol (skip={skip}, limit={limit})")
    return crud.get_usuario_roles(db=db, skip=skip, limit=limit)

@router.get("/{id_usuario_rol}", response_model=schemas.UsuarioRol)
def read_usuario_rol(id_usuario_rol: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para obtener UsuarioRol por ID: {id_usuario_rol}")
    db_usuario_rol = crud.get_usuario_rol(db=db, id_usuario_rol=id_usuario_rol)
    if not db_usuario_rol:
        logger.warning(f"UsuarioRol no encontrado: {id_usuario_rol}")
        raise HTTPException(status_code=404, detail="UsuarioRol no encontrado")
    return db_usuario_rol

@router.put("/{id_usuario_rol}", response_model=schemas.UsuarioRol)
def update_usuario_rol(id_usuario_rol: int, usuario_rol: schemas.UsuarioRolUpdate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para actualizar UsuarioRol ID: {id_usuario_rol}")
    db_usuario_rol = crud.update_usuario_rol(db=db, id_usuario_rol=id_usuario_rol, usuario_rol_update=usuario_rol)
    if not db_usuario_rol:
        logger.warning(f"UsuarioRol no encontrado para actualizar: {id_usuario_rol}")
        raise HTTPException(status_code=404, detail="UsuarioRol no encontrado")
    return db_usuario_rol

@router.delete("/{id_usuario_rol}", response_model=schemas.UsuarioRol)
def delete_usuario_rol(id_usuario_rol: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para eliminar UsuarioRol ID: {id_usuario_rol}")
    return crud.delete_usuario_rol(db=db, id_usuario_rol=id_usuario_rol)
