from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Rol)
def create_rol(rol: schemas.RolCreate, db: Session = Depends(get_db)):
    return crud.create_rol(db=db, rol=rol)

@router.get("/", response_model=list[schemas.Rol])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_roles(db=db, skip=skip, limit=limit)

@router.get("/{id_rol}", response_model=schemas.Rol)
def read_rol(id_rol: int, db: Session = Depends(get_db)):
    return crud.get_rol(db=db, id_rol=id_rol)

@router.put("/{id_rol}", response_model=schemas.Rol)
def update_rol(id_rol: int, rol: schemas.RolCreate, db: Session = Depends(get_db)):
    return crud.update_rol(db=db, id_rol=id_rol, rol_data=rol)

@router.delete("/{id_rol}", response_model=schemas.Rol)
def delete_rol(id_rol: int, db: Session = Depends(get_db)):
    return crud.delete_rol(db=db, id_rol=id_rol)
