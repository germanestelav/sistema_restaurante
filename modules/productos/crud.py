# productos/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

# Crear un nuevo producto
def create_producto(db: Session, producto: schemas.ProductoCreate):
    db_producto = models.Producto(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        categoria=producto.categoria,
        stock=producto.stock
    )
    
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

# Obtener todos los productos
def get_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Producto).offset(skip).limit(limit).all()

# Obtener un producto por su ID
def get_producto(db: Session, producto_id: int):
    return db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()

# Actualizar un producto
def update_producto(db: Session, producto_id: int, producto: schemas.ProductoCreate):
    db_producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()
    if db_producto:
        db_producto.nombre = producto.nombre
        db_producto.descripcion = producto.descripcion
        db_producto.precio = producto.precio
        db_producto.categoria = producto.categoria
        db_producto.stock = producto.stock
        db.commit()
        db.refresh(db_producto)
    return db_producto

# Eliminar un producto
def delete_producto(db: Session, producto_id: int):
    db_producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()
    if db_producto:
        db.delete(db_producto)
        db.commit()
    return db_producto
