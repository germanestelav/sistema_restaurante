# usuarios/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from .crud import create_usuario, update_usuario, delete_usuario, get_usuario
from .schemas import UsuarioCreate, Usuario

router = APIRouter()

# Ruta para crear un nuevo usuario
@router.post("/usuarios/", response_model=Usuario)
def create_usuario_route(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = create_usuario(db=db, usuario=usuario)
    if not db_usuario:
        raise HTTPException(status_code=400, detail="El usuario con este email ya existe")
    return db_usuario

# Ruta para obtener un usuario por su ID
@router.get("/usuarios/{id_usuario}", response_model=Usuario)
def get_usuario(id_usuario: int, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

# Ruta para actualizar un usuario
@router.put("/usuarios/{id_usuario}", response_model=Usuario)
def update_usuario_route(id_usuario: int, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = update_usuario(db, id_usuario, usuario)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

# Ruta para eliminar un usuario
@router.delete("/usuarios/{id_usuario}", response_model=Usuario)
def delete_usuario_route(id_usuario: int, db: Session = Depends(get_db)):
    db_usuario = delete_usuario(db, id_usuario)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

