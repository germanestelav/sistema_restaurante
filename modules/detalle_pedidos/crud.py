from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from modules.pedidos.models import Pedido
from modules.productos.models import Producto
from utils.logger import get_logger

logger = get_logger("detalles_pedidos.crud")

# Crear un detalle de pedido

def create_detalle_pedido(db: Session, detalle: schemas.DetallePedidoCreate, id_pedido: int):
    logger.info(f"Creando detalle de pedido para el pedido con ID {id_pedido}")
    # Verificar si el pedido existe
    db_pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()
    if not db_pedido:
        logger.warning(f"Pedido con ID {id_pedido} no encontrado")
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    # Verificar si el producto existe
    db_producto = db.query(Producto).filter(Producto.id_producto == detalle.id_producto).first()
    if not db_producto:
        logger.warning(f"Producto con ID {detalle.id_producto} no encontrado")
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
    logger.info(f"Detalle de pedido creado exitosamente: {db_detalle}")
    return db_detalle

def get_detalle_pedidos(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Obteniendo detalles de pedido con skip={skip}, limit={limit}")
    detalles = db.query(models.DetallePedido).offset(skip).limit(limit).all()
    logger.info(f"{len(detalles)} detalles obtenidos")
    return detalles

# Obtener todos los detalles de un pedido
def get_detalle_pedido(db: Session, id_pedido: int):
    logger.info(f"Obteniendo detalles del pedido con ID {id_pedido}")
    detalles = db.query(models.DetallePedido).filter(models.DetallePedido.id_pedido == id_pedido).all()
    logger.info(f"Se encontraron {len(detalles)} detalles para el pedido {id_pedido}")
    return detalles

# Actualizar un detalle de pedido
def update_detalle_pedido(db: Session, id_detalle: int, detalle: schemas.DetallePedidoCreate):
    logger.info(f"Actualizando detalle con ID {id_detalle}")
    db_detalle = db.query(models.DetallePedido).filter(models.DetallePedido.id_detalle == id_detalle).first()
    if not db_detalle:
        logger.warning(f"Detalle con ID {id_detalle} no encontrado")
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")
    
    db_detalle.cantidad = detalle.cantidad
    db_detalle.precio_unitario = detalle.precio_unitario
    db.commit()
    db.refresh(db_detalle)
    logger.info(f"Detalle actualizado exitosamente: {db_detalle}")
    return db_detalle

# Eliminar un detalle de pedido
def delete_detalle_pedido(db: Session, id_detalle: int):
    logger.info(f"Eliminando detalle con ID {id_detalle}")
    db_detalle = db.query(models.DetallePedido).filter(models.DetallePedido.id_detalle == id_detalle).first()
    if not db_detalle:
        logger.warning(f"Detalle con ID {id_detalle} no encontrado")
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")
    
    db.delete(db_detalle)
    db.commit()
    logger.info(f"Detalle eliminado exitosamente: ID {id_detalle}")
    return db_detalle
