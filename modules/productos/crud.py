# productos/crud.py
from sqlalchemy.orm import Session
from . import models, schemas

def create_producto(db: Session, producto: schemas.ProductoCreate):
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
    return db_producto

def get_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Producto).offset(skip).limit(limit).all()

def get_producto(db: Session, producto_id: int):
    return db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()

def update_producto(db: Session, producto_id: int, producto: schemas.ProductoCreate):
    db_producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()
    if db_producto:
        db_producto.nombre = producto.nombre
        db_producto.descripcion = producto.descripcion
        db_producto.precio = producto.precio
        db_producto.stock = producto.stock
        db_producto.estado = producto.estado
        db_producto.id_categoria = producto.id_categoria
        db.commit()
        db.refresh(db_producto)
    return db_producto

def delete_producto(db: Session, producto_id: int):
    db_producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()
    if db_producto:
        db.delete(db_producto)
        db.commit()
    return db_producto
