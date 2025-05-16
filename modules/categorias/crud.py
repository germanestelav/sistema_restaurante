from sqlalchemy.orm import Session
from .models import Categoria
from .schemas import CategoriaCreate
from fastapi import HTTPException

def create_categoria(db: Session, categoria: CategoriaCreate):
    db_categoria = Categoria(nombre=categoria.nombre)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Categoria).offset(skip).limit(limit).all()

def get_categoria(db: Session, id_categoria: int):
    return db.query(Categoria).filter(Categoria.id_categoria == id_categoria).first()

def update_categoria(db: Session, id_categoria: int, categoria: CategoriaCreate):
    db_categoria = db.query(Categoria).filter(Categoria.id_categoria == id_categoria).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db_categoria.nombre = categoria.nombre
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def delete_categoria(db: Session, id_categoria: int):
    db_categoria = db.query(Categoria).filter(Categoria.id_categoria == id_categoria).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(db_categoria)
    db.commit()
    return db_categoria
