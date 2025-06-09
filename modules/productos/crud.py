# productos/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from utils.logger import get_logger

logger = get_logger("productos.crud")

def create_producto(db: Session, producto: schemas.ProductoCreate):
    logger.info(f"Creando producto: {producto}")
    db_producto = models.Producto(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        stock=producto.stock,
        estado=producto.estado,
        id_categoria=producto.id_categoria
    )
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    logger.info(f"Producto creado con ID: {db_producto.id_producto}")
    return db_producto

def get_productos(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Obteniendo productos (skip={skip}, limit={limit})")
    return db.query(models.Producto).offset(skip).limit(limit).all()

def get_producto(db: Session, producto_id: int):
    logger.info(f"Obteniendo producto con ID: {producto_id}")
    producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()
    if not producto:
        logger.warning(f"Producto no encontrado con ID: {producto_id}")
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

def get_productos_con_stock(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Obteniendo productos con stock > 0 (skip={skip}, limit={limit})")
    return db.query(models.Producto).filter(models.Producto.stock > 0).offset(skip).limit(limit).all()


def update_producto(db: Session, producto_id: int, producto: schemas.ProductoCreate):
    logger.info(f"Actualizando producto ID: {producto_id} con datos: {producto}")
    db_producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()
    if not db_producto:
        logger.warning(f"No se encontró producto para actualizar con ID: {producto_id}")
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db_producto.nombre = producto.nombre
    db_producto.descripcion = producto.descripcion
    db_producto.precio = producto.precio
    db_producto.stock = producto.stock
    db_producto.estado = producto.estado
    db_producto.id_categoria = producto.id_categoria

    db.commit()
    db.refresh(db_producto)
    logger.info(f"Producto actualizado con ID: {producto_id}")
    return db_producto

def delete_producto(db: Session, producto_id: int):
    logger.info(f"Eliminando producto con ID: {producto_id}")
    db_producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()
    if not db_producto:
        logger.warning(f"Producto no encontrado para eliminar con ID: {producto_id}")
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(db_producto)
    db.commit()
    logger.info(f"Producto eliminado con ID: {producto_id}")
    return db_producto