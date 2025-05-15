# modules/usuarios/crud.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas  # Asegúrate de importar schemas aquí
from .models import Usuario
from .schemas import UsuarioCreate  # Importamos el esquema UsuarioCreate desde schemas.py

# Configuramos el contexto para cifrar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para cifrar la contraseña
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Función para verificar la contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    # Verificar si el correo ya existe
    existing_user_by_email = db.query(models.Usuario).filter(models.Usuario.correo == usuario.correo).first()
    if existing_user_by_email:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")
    
    # Verificar si el número de identificación ya existe
    existing_user_by_id = db.query(models.Usuario).filter(models.Usuario.numero_identificacion == usuario.numero_identificacion).first()
    if existing_user_by_id:
        raise HTTPException(status_code=400, detail="El número de identificación ya está registrado.")
    
    # Si no existe, crear un nuevo usuario
    db_usuario = models.Usuario(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        correo=usuario.correo,
        contrasena=hash_password(usuario.contrasena),
        estado=usuario.estado,
        numero_identificacion=usuario.numero_identificacion
    )
    
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Obtener todos los usuarios
def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()

# Obtener un usuario por su ID
def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

# Actualizar un usuario con contraseña cifrada
def update_usuario(db: Session, usuario_id: int, usuario: UsuarioCreate):
    db_usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if db_usuario:
        db_usuario.nombre = usuario.nombre
        db_usuario.apellido = usuario.apellido
        db_usuario.correo = usuario.correo
        db_usuario.contrasena = hash_password(usuario.contrasena)  # Ciframos la nueva contraseña
        db_usuario.estado = usuario.estado
        db_usuario.numero_identificacion = usuario.numero_identificacion
        db.commit()
        db.refresh(db_usuario)
    return db_usuario

# Eliminar un usuario
def delete_usuario(db: Session, usuario_id: int):
    db_usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
    return db_usuario
