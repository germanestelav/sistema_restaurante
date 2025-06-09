from sqlalchemy.orm import Session
from .models import Rol
from .schemas import RolCreate
from fastapi import HTTPException
from utils.logger import get_logger

logger = get_logger("rol.crud")

def create_rol(db: Session, rol: RolCreate):
    logger.info(f"Creando rol con nombre: {rol.nombre}")
    db_rol = Rol(nombre=rol.nombre)
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    logger.info(f"Rol creado con ID: {db_rol.id_rol}")
    return db_rol

def get_roles(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Listando roles (skip={skip}, limit={limit})")
    return db.query(Rol).offset(skip).limit(limit).all()

def get_rol(db: Session, id_rol: int):
    logger.info(f"Buscando rol con ID: {id_rol}")
    rol = db.query(Rol).filter(Rol.id_rol == id_rol).first()
    if not rol:
        logger.warning(f"Rol no encontrado con ID: {id_rol}")
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

def update_rol(db: Session, id_rol: int, rol_data: RolCreate):
    logger.info(f"Actualizando rol con ID: {id_rol}")
    rol = db.query(Rol).filter(Rol.id_rol == id_rol).first()
    if not rol:
        logger.warning(f"Rol no encontrado para actualizar con ID: {id_rol}")
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    rol.nombre = rol_data.nombre
    db.commit()
    db.refresh(rol)
    logger.info(f"Rol actualizado con ID: {rol.id_rol}")
    return rol

def delete_rol(db: Session, id_rol: int):
    logger.info(f"Eliminando rol con ID: {id_rol}")
    rol = db.query(Rol).filter(Rol.id_rol == id_rol).first()
    if not rol:
        logger.warning(f"Rol no encontrado para eliminar con ID: {id_rol}")
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db.delete(rol)
    db.commit()
    logger.info(f"Rol eliminado con ID: {id_rol}")
    return rol
