from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

# Crear un detalle de pedido
def create_detalle_pedido(db: Session, detalle: schemas.DetallePedidoCreate, id_pedido: int):
    # Verificar si el pedido existe
    db_pedido = db.query(models.Pedido).filter(models.Pedido.id_pedido == id_pedido).first()
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    # Verificar si el producto existe
    db_producto = db.query(models.Producto).filter(models.Producto.id_producto == detalle.id_producto).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Crear el detalle de pedido
    db_detalle = models.DetallePedido(
        id_pedido=id_pedido,
        id_producto=detalle.id_producto,
        cantidad=detalle.cantidad,
        precio_unitario=detalle.precio_unitario
    )
    db.add(db_detalle)
    db.commit()
    db.refresh(db_detalle)
    return db_detalle

def get_detalle_pedidos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DetallePedido).offset(skip).limit(limit).all()

# Obtener todos los detalles de un pedido
def get_detalle_pedido(db: Session, id_pedido: int):
    return db.query(models.DetallePedido).filter(models.DetallePedido.id_pedido == id_pedido).all()

# Actualizar un detalle de pedido
def update_detalle_pedido(db: Session, id_detalle: int, detalle: schemas.DetallePedidoCreate):
    db_detalle = db.query(models.DetallePedido).filter(models.DetallePedido.id_detalle == id_detalle).first()
    if not db_detalle:
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")
    
    db_detalle.cantidad = detalle.cantidad
    db_detalle.precio_unitario = detalle.precio_unitario
    db.commit()
    db.refresh(db_detalle)
    return db_detalle

# Eliminar un detalle de pedido
def delete_detalle_pedido(db: Session, id_detalle: int):
    db_detalle = db.query(models.DetallePedido).filter(models.DetallePedido.id_detalle == id_detalle).first()
    if not db_detalle:
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")
    
    db.delete(db_detalle)
    db.commit()
    return db_detalle
