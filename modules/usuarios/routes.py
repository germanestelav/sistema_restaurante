from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db  # Función que conecta a la base de datos
from utils.logger import get_logger

router = APIRouter()
logger = get_logger("usuarios.routes")

# Ruta para crear un nuevo usuario
@router.post("/", response_model=schemas.Usuario)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para crear usuario: {usuario.correo}")
    return crud.create_usuario(db=db, usuario=usuario)

# Ruta para obtener todos los usuarios
@router.get("/", response_model=list[schemas.Usuario])
def leer_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para obtener usuarios (skip={skip}, limit={limit})")
    return crud.get_usuarios(db=db, skip=skip, limit=limit)

# Ruta para obtener un usuario por ID
@router.get("/{usuario_id}", response_model=schemas.Usuario)
def leer_usuario(usuario_id: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para obtener usuario por ID: {usuario_id}")
    db_usuario = crud.get_usuario(db=db, usuario_id=usuario_id)
    if db_usuario is None:
        logger.warning(f"Usuario no encontrado: {usuario_id}")
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

# Ruta para actualizar un usuario
@router.put("/{usuario_id}", response_model=schemas.Usuario)
def actualizar_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para actualizar usuario ID: {usuario_id}")
    db_usuario = crud.update_usuario(db=db, usuario_id=usuario_id, usuario=usuario)
    if db_usuario is None:
        logger.warning(f"Usuario no encontrado para actualizar: {usuario_id}")
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

# Ruta para eliminar un usuario
@router.delete("/{usuario_id}", response_model=schemas.Usuario)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para eliminar usuario ID: {usuario_id}")
    db_usuario = crud.delete_usuario(db=db, usuario_id=usuario_id)
    if db_usuario is None:
        logger.warning(f"Usuario no encontrado para eliminar: {usuario_id}")
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario
