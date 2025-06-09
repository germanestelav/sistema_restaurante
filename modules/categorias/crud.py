from sqlalchemy.orm import Session
from .models import Categoria
from .schemas import CategoriaCreate
from fastapi import HTTPException
from utils.logger import get_logger

logger = get_logger("categorias.crud")

def create_categoria(db: Session, categoria: CategoriaCreate):
    logger.info(f"Creando categoría con nombre: {categoria.nombre}")
    db_categoria = Categoria(nombre=categoria.nombre)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    logger.info(f"Categoría creada exitosamente: {db_categoria}")
    return db_categoria

def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Obteniendo lista de categorías: skip={skip}, limit={limit}")
    categorias = db.query(Categoria).offset(skip).limit(limit).all()
    logger.info(f"{len(categorias)} categorías obtenidas")
    return categorias

def get_categoria(db: Session, id_categoria: int):
    logger.info(f"Buscando categoría con ID: {id_categoria}")
    categoria = db.query(Categoria).filter(Categoria.id_categoria == id_categoria).first()
    if categoria:
        logger.info(f"Categoría encontrada: {categoria}")
    else:
        logger.warning(f"Categoría con ID {id_categoria} no encontrada")
    return categoria

def update_categoria(db: Session, id_categoria: int, categoria: CategoriaCreate):
    logger.info(f"Actualizando categoría con ID: {id_categoria}")
    db_categoria = db.query(Categoria).filter(Categoria.id_categoria == id_categoria).first()
    if not db_categoria:
        logger.warning(f"Categoría con ID {id_categoria} no encontrada para actualizar")
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db_categoria.nombre = categoria.nombre
    db.commit()
    db.refresh(db_categoria)
    logger.info(f"Categoría actualizada: {db_categoria}")
    return db_categoria

def delete_categoria(db: Session, id_categoria: int):
    logger.info(f"Eliminando categoría con ID: {id_categoria}")
    db_categoria = db.query(Categoria).filter(Categoria.id_categoria == id_categoria).first()
    if not db_categoria:
        logger.warning(f"Categoría con ID {id_categoria} no encontrada para eliminar")
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(db_categoria)
    db.commit()
    logger.info(f"Categoría eliminada: {db_categoria}")
    return db_categoria
