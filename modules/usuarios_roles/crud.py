from sqlalchemy.orm import Session
from .models import UsuarioRol
from .schemas import UsuarioRolCreate
from fastapi import HTTPException
from .schemas import UsuarioRolUpdate
from utils.logger import get_logger

logger = get_logger("usuario_rol.crud")

def create_usuario_rol(db: Session, usuario_rol: UsuarioRolCreate):
    logger.info(f"Creando UsuarioRol con id_usuario={usuario_rol.id_usuario} y id_rol={usuario_rol.id_rol}")
    db_usuario_rol = UsuarioRol(
        id_usuario=usuario_rol.id_usuario,
        id_rol=usuario_rol.id_rol
    )
    db.add(db_usuario_rol)
    db.commit()
    db.refresh(db_usuario_rol)
    logger.info(f"UsuarioRol creado con ID: {db_usuario_rol.id_usuario_rol}")
    return db_usuario_rol

def get_usuario_roles(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Obteniendo lista de UsuarioRol (skip={skip}, limit={limit})")
    return db.query(UsuarioRol).offset(skip).limit(limit).all()

def get_usuario_rol(db: Session, id_usuario_rol: int):
    logger.info(f"Buscando UsuarioRol por ID: {id_usuario_rol}")
    return db.query(UsuarioRol).filter(UsuarioRol.id_usuario_rol == id_usuario_rol).first()

def update_usuario_rol(db: Session, id_usuario_rol: int, usuario_rol_update: UsuarioRolUpdate):
    logger.info(f"Intentando actualizar UsuarioRol ID: {id_usuario_rol}")
    usuario_rol = db.query(UsuarioRol).filter(UsuarioRol.id_usuario_rol == id_usuario_rol).first()
    if usuario_rol is None:
        raise HTTPException(status_code=404, detail="UsuarioRol no encontrado")
    usuario_rol.id_usuario = usuario_rol_update.id_usuario
    usuario_rol.id_rol = usuario_rol_update.id_rol
    db.commit()
    db.refresh(usuario_rol)
    logger.info(f"UsuarioRol actualizado: {id_usuario_rol}")
    return usuario_rol

def delete_usuario_rol(db: Session, id_usuario_rol: int):
    logger.info(f"Intentando eliminar UsuarioRol ID: {id_usuario_rol}")
    usuario_rol = db.query(UsuarioRol).filter(UsuarioRol.id_usuario_rol == id_usuario_rol).first()
    if usuario_rol is None:
        logger.warning(f"UsuarioRol no encontrado para eliminar: {id_usuario_rol}")
        raise HTTPException(status_code=404, detail="UsuarioRol no encontrado")
    db.delete(usuario_rol)
    db.commit()
    logger.info(f"UsuarioRol eliminado: {id_usuario_rol}")
    return usuario_rol
