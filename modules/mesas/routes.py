from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db

router = APIRouter()

# Ruta para crear una nueva mesa
@router.post("/", response_model=schemas.Mesa)
def crear_mesa(mesa: schemas.MesaCreate, db: Session = Depends(get_db)):
    return crud.create_mesa(db=db, mesa=mesa)

# Ruta para obtener todas las mesas
@router.get("/", response_model=list[schemas.Mesa])
def leer_mesas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_mesas(db=db, skip=skip, limit=limit)

# Ruta para obtener una mesa por ID
@router.get("/{mesa_id}", response_model=schemas.Mesa)
def leer_mesa(mesa_id: int, db: Session = Depends(get_db)):
    db_mesa = crud.get_mesa(db=db, mesa_id=mesa_id)
    if db_mesa is None:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return db_mesa

# Ruta para actualizar una mesa
@router.put("/{mesa_id}", response_model=schemas.Mesa)
def actualizar_mesa(mesa_id: int, mesa: schemas.MesaCreate, db: Session = Depends(get_db)):
    db_mesa = crud.update_mesa(db=db, mesa_id=mesa_id, mesa=mesa)
    if db_mesa is None:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return db_mesa

# Ruta para eliminar una mesa
@router.delete("/{mesa_id}", response_model=schemas.Mesa)
def eliminar_mesa(mesa_id: int, db: Session = Depends(get_db)):
    db_mesa = crud.delete_mesa(db=db, mesa_id=mesa_id)
    if db_mesa is None:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return db_mesa

