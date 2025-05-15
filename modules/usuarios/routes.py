from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db  # Función que conecta a la base de datos

router = APIRouter()

# Ruta para crear un nuevo usuario
@router.post("/", response_model=schemas.Usuario)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.create_usuario(db=db, usuario=usuario)

# Ruta para obtener todos los usuarios
@router.get("/", response_model=list[schemas.Usuario])
def leer_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_usuarios(db=db, skip=skip, limit=limit)

# Ruta para obtener un usuario por ID
@router.get("/{usuario_id}", response_model=schemas.Usuario)
def leer_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario(db=db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

# Ruta para actualizar un usuario
@router.put("/{usuario_id}", response_model=schemas.Usuario)
def actualizar_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud.update_usuario(db=db, usuario_id=usuario_id, usuario=usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

# Ruta para eliminar un usuario
@router.delete("/{usuario_id}", response_model=schemas.Usuario)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.delete_usuario(db=db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario
