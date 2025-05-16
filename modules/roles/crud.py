from sqlalchemy.orm import Session
from .models import Rol
from .schemas import RolCreate
from fastapi import HTTPException

def create_rol(db: Session, rol: RolCreate):
    db_rol = Rol(nombre=rol.nombre)
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Rol).offset(skip).limit(limit).all()

def get_rol(db: Session, id_rol: int):
    rol = db.query(Rol).filter(Rol.id_rol == id_rol).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

def update_rol(db: Session, id_rol: int, rol_data: RolCreate):
    rol = db.query(Rol).filter(Rol.id_rol == id_rol).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    rol.nombre = rol_data.nombre
    db.commit()
    db.refresh(rol)
    return rol

def delete_rol(db: Session, id_rol: int):
    rol = db.query(Rol).filter(Rol.id_rol == id_rol).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db.delete(rol)
    db.commit()
    return rol
