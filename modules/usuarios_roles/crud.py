from sqlalchemy.orm import Session
from .models import UsuarioRol
from .schemas import UsuarioRolCreate
from fastapi import HTTPException
from .schemas import UsuarioRolUpdate

def create_usuario_rol(db: Session, usuario_rol: UsuarioRolCreate):
    db_usuario_rol = UsuarioRol(
        id_usuario=usuario_rol.id_usuario,
        id_rol=usuario_rol.id_rol
    )
    db.add(db_usuario_rol)
    db.commit()
    db.refresh(db_usuario_rol)
    return db_usuario_rol

def get_usuario_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UsuarioRol).offset(skip).limit(limit).all()

def get_usuario_rol(db: Session, id_usuario_rol: int):
    return db.query(UsuarioRol).filter(UsuarioRol.id_usuario_rol == id_usuario_rol).first()

def update_usuario_rol(db: Session, id_usuario_rol: int, usuario_rol_update: UsuarioRolUpdate):
    usuario_rol = db.query(UsuarioRol).filter(UsuarioRol.id_usuario_rol == id_usuario_rol).first()
    if usuario_rol is None:
        raise HTTPException(status_code=404, detail="UsuarioRol no encontrado")
    usuario_rol.id_usuario = usuario_rol_update.id_usuario
    usuario_rol.id_rol = usuario_rol_update.id_rol
    db.commit()
    db.refresh(usuario_rol)
    return usuario_rol

def delete_usuario_rol(db: Session, id_usuario_rol: int):
    usuario_rol = db.query(UsuarioRol).filter(UsuarioRol.id_usuario_rol == id_usuario_rol).first()
    if usuario_rol is None:
        raise HTTPException(status_code=404, detail="UsuarioRol no encontrado")
    db.delete(usuario_rol)
    db.commit()
    return usuario_rol
