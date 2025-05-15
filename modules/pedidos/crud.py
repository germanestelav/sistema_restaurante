from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from modules.mesas.models import Mesa 

# Crear un nuevo pedido
def create_pedido(db: Session, pedido: schemas.PedidoCreate):
    # Validar que la mesa existe
    db_mesa = db.query(Mesa).filter(Mesa.id_mesa == pedido.id_mesa).first()
    if not db_mesa:
        raise Exception("Mesa no encontrada")

    # Crear pedido
    db_pedido = models.Pedido(
        id_usuario=pedido.id_usuario,
        id_mesa=pedido.id_mesa,
        estado="pendiente"
    )
    
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)

    # Crear los detalles del pedido
    for detalle in pedido.detalles:
        db_detalle = models.DetallePedido(
            id_pedido=db_pedido.id_pedido,
            id_producto=detalle.id_producto,
            cantidad=detalle.cantidad,
            precio_unitario=detalle.precio_unitario
        )
        db.add(db_detalle)

    db.commit()
    return db_pedido

# Obtener todos los pedidos
def get_pedidos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pedido).offset(skip).limit(limit).all()

# Obtener un pedido por su ID
def get_pedido(db: Session, pedido_id: int):
    return db.query(models.Pedido).filter(models.Pedido.id_pedido == pedido_id).first()

# Actualizar un pedido
def update_pedido(db: Session, pedido_id: int, pedido: schemas.PedidoCreate):
    db_pedido = db.query(models.Pedido).filter(models.Pedido.id_pedido == pedido_id).first()
    
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    db_pedido.estado = pedido.estado  # Actualizar solo el estado del pedido
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

# Eliminar un pedido
def delete_pedido(db: Session, pedido_id: int):
    db_pedido = db.query(models.Pedido).filter(models.Pedido.id_pedido == pedido_id).first()
    
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    db.delete(db_pedido)
    db.commit()
    return db_pedido
