from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Categoria)
def create_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return crud.create_categoria(db=db, categoria=categoria)

@router.get("/", response_model=list[schemas.Categoria])
def read_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_categorias(db=db, skip=skip, limit=limit)

@router.get("/{id_categoria}", response_model=schemas.Categoria)
def read_categoria(id_categoria: int, db: Session = Depends(get_db)):
    db_categoria = crud.get_categoria(db=db, id_categoria=id_categoria)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria

@router.put("/{id_categoria}", response_model=schemas.Categoria)
def update_categoria(id_categoria: int, categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return crud.update_categoria(db=db, id_categoria=id_categoria, categoria=categoria)

@router.delete("/{id_categoria}", response_model=schemas.Categoria)
def delete_categoria(id_categoria: int, db: Session = Depends(get_db)):
    return crud.delete_categoria(db=db, id_categoria=id_categoria)
