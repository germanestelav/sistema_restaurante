# usuarios/crud.py
from sqlalchemy.orm import Session
from models import Usuario as UsuarioModel
from schemas import UsuarioCreate
from passlib.context import CryptContext  # Para el cifrado de contraseñas

# Inicialización del contexto de cifrado de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para crear un nuevo usuario
def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = db.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).first()
    if db_usuario:
        return None  # Si el usuario ya existe, retornamos None
    
    # Ciframos la contraseña antes de almacenarla
    hashed_password = pwd_context.hash(usuario.contrasena)
    
    db_usuario = UsuarioModel(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        email=usuario.email,
        contrasena=hashed_password,  # Guardamos la contraseña cifrada
        id_rol=usuario.id_rol,
        estado=usuario.estado
    )
    
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Función para obtener un usuario por su ID
def get_usuario(db: Session, id_usuario: int):
    return db.query(UsuarioModel).filter(UsuarioModel.id_usuario == id_usuario).first()

# Función para actualizar un usuario
def update_usuario(db: Session, id_usuario: int, usuario: UsuarioCreate):
    db_usuario = db.query(UsuarioModel).filter(UsuarioModel.id_usuario == id_usuario).first()
    
    if db_usuario:
        # Actualizamos los campos del usuario
        db_usuario.nombre = usuario.nombre
        db_usuario.apellido = usuario.apellido
        db_usuario.email = usuario.email
        db_usuario.contrasena = pwd_context.hash(usuario.contrasena)  # Cifrar la nueva contraseña
        db_usuario.id_rol = usuario.id_rol
        db_usuario.estado = usuario.estado
        
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    
    return None  # Si no se encuentra el usuario, retornamos None

# Función para eliminar un usuario
def delete_usuario(db: Session, id_usuario: int):
    db_usuario = db.query(UsuarioModel).filter(UsuarioModel.id_usuario == id_usuario).first()
    
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
        return db_usuario
    
    return None  # Si el usuario no existe, retornamos None
