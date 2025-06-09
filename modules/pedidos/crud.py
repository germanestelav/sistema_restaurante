from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from modules.mesas.models import Mesa 
from modules.productos.models import Producto
from datetime import datetime
from utils.logger import get_logger

logger = get_logger("pedidos.crud")

# Crear un nuevo pedido
def create_pedido(db: Session, pedido: schemas.PedidoCreate, id_usuario: int):
    logger.info(f"Intentando crear pedido para usuario {id_usuario} en mesa {pedido.id_mesa}")
    # Validar que la mesa existe
    db_mesa = db.query(Mesa).filter(Mesa.id_mesa == pedido.id_mesa).first()
    if not db_mesa:
        logger.warning(f"Mesa {pedido.id_mesa} no encontrada")
        raise HTTPException(status_code=404, detail="Mesa no encontrada")

    # Crear pedido
    db_pedido = models.Pedido(
        id_usuario=id_usuario,
        id_mesa=pedido.id_mesa,
        id_estado_pedido=pedido.id_estado_pedido,  # recibe el estado inicial
        fecha=datetime.now()
    )
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    logger.info(f"Pedido {db_pedido.id_pedido} creado con éxito")

    # Crear los detalles y descontar stock
    for detalle in pedido.detalles:
        producto = db.query(Producto).filter(Producto.id_producto == detalle.id_producto, Producto.stock > 0).first()
        if not producto:
            logger.warning(f"Producto {detalle.id_producto} no encontrado o fuera de stock")
            raise HTTPException(status_code=404, detail=f"Producto {detalle.id_producto} no encontrado o fuera de stock")
        if detalle.cantidad <= 0:
            logger.warning(f"Cantidad inválida: {detalle.cantidad}")
            raise HTTPException(status_code=400, detail="Cantidad inválida")
        if producto.stock < detalle.cantidad:
            logger.warning(f"Stock insuficiente para producto {producto.nombre}")
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para el producto: {producto.nombre}")
        producto.stock -= detalle.cantidad
        db_detalle = models.DetallePedido(
            id_pedido=db_pedido.id_pedido,
            id_producto=detalle.id_producto,
            cantidad=detalle.cantidad,
            precio_unitario=producto.precio
        )
        db.add(db_detalle)
        logger.info(f"Detalle agregado: {detalle.cantidad}x {producto.nombre}")
    db.commit()
    logger.info(f"Pedido {db_pedido.id_pedido} y sus detalles guardados correctamente")
    return db_pedido

# Obtener todos los pedidos
def get_pedidos(db: Session, skip: int = 0, limit: int = 100):
    logger.info("Obteniendo lista de pedidos")
    return db.query(models.Pedido).offset(skip).limit(limit).all()

# Obtener un pedido por su ID
def get_pedido(db: Session, pedido_id: int):
    logger.info(f"Buscando pedido con ID {pedido_id}")
    return db.query(models.Pedido).filter(models.Pedido.id_pedido == pedido_id).first()

# Actualizar solo el estado del pedido
def update_pedido(db: Session, pedido_id: int, pedido: schemas.PedidoUpdate):
    logger.info(f"Actualizando pedido {pedido_id}")
    db_pedido = db.query(models.Pedido).filter(models.Pedido.id_pedido == pedido_id).first()
    if not db_pedido:
        logger.warning(f"Pedido {pedido_id} no encontrado")
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if pedido.id_estado_pedido is not None:
        db_pedido.id_estado_pedido = pedido.id_estado_pedido
    db.commit()
    db.refresh(db_pedido)
    logger.info(f"Pedido {pedido_id} actualizado correctamente")
    return db_pedido

# Eliminar un pedido (devuelve stock)
def delete_pedido(db: Session, pedido_id: int):
    logger.info(f"Intentando eliminar pedido {pedido_id}")
    db_pedido = db.query(models.Pedido).filter(models.Pedido.id_pedido == pedido_id).first()
    if not db_pedido:
        logger.warning(f"Pedido {pedido_id} no encontrado")
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    detalles = db.query(models.DetallePedido).filter(models.DetallePedido.id_pedido == pedido_id).all()
    for detalle in detalles:
        producto = db.query(Producto).filter(Producto.id_producto == detalle.id_producto).first()
        if producto:
            producto.stock += detalle.cantidad
        db.delete(detalle)
    db.delete(db_pedido)
    db.commit()
    logger.info(f"Pedido {pedido_id} y sus detalles eliminados correctamente")
    return db_pedido

# Actualizar un pedido y sus detalles
def update_pedido_con_detalles(db: Session, pedido_id: int, pedido_update: schemas.PedidoUpdate):
    # Buscar el pedido por su ID
    db_pedido = db.query(models.Pedido).filter(models.Pedido.id_pedido == pedido_id).first()
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    # Actualizar mesa si se envía en la actualización
    if pedido_update.id_mesa is not None:
        db_pedido.id_mesa = pedido_update.id_mesa

    # Actualizar estado del pedido si se envía
    if pedido_update.id_estado_pedido is not None:
        db_pedido.id_estado_pedido = pedido_update.id_estado_pedido

    # Si no vienen detalles, solo actualizamos pedido (mesa/estado) y guardamos
    if not pedido_update.detalles:
        db.commit()
        db.refresh(db_pedido)
        return db_pedido

    # Obtener detalles actuales relacionados al pedido
    detalles_actuales = db.query(models.DetallePedido).filter(models.DetallePedido.id_pedido == pedido_id).all()
    # Crear diccionario para acceder rápido por id_detalle
    detalles_actuales_dict = {d.id_detalle: d for d in detalles_actuales}

    # Recorrer cada detalle que llega en la actualización
    for detalle_data in pedido_update.detalles:
        # Para actualizar, siempre debe venir el id_detalle
        if not detalle_data.id_detalle:
            raise HTTPException(status_code=400, detail="Debe especificar id_detalle para actualizar")

        # Verificar que ese detalle pertenezca al pedido
        detalle_actual = detalles_actuales_dict.get(detalle_data.id_detalle)
        if not detalle_actual:
            raise HTTPException(status_code=404, detail=f"Detalle {detalle_data.id_detalle} no encontrado en pedido {pedido_id}")

        # Si cambia el producto del detalle:
        if detalle_actual.id_producto != detalle_data.id_producto:
            # Ajustar stock: devolver stock del producto anterior
            producto_ant = db.query(Producto).filter(Producto.id_producto == detalle_actual.id_producto).first()
            producto_nuevo = db.query(Producto).filter(Producto.id_producto == detalle_data.id_producto).first()

            if producto_ant:
                producto_ant.stock += detalle_actual.cantidad

            # Verificar stock suficiente del producto nuevo
            if not producto_nuevo or producto_nuevo.stock < detalle_data.cantidad:
                raise HTTPException(status_code=400, detail="Stock insuficiente para nuevo producto")

            # Descontar stock del producto nuevo
            producto_nuevo.stock -= detalle_data.cantidad

            # Actualizar detalle con nuevo producto, cantidad y precio
            detalle_actual.id_producto = detalle_data.id_producto
            detalle_actual.cantidad = detalle_data.cantidad
            detalle_actual.precio_unitario = producto_nuevo.precio
        else:
            # Si no cambia producto, solo actualizar cantidad y ajustar stock si cambia
            producto = db.query(Producto).filter(Producto.id_producto == detalle_actual.id_producto).first()
            diferencia = detalle_data.cantidad - detalle_actual.cantidad
            if diferencia > 0 and producto.stock < diferencia:
                raise HTTPException(status_code=400, detail="Stock insuficiente para producto")
            producto.stock -= diferencia
            detalle_actual.cantidad = detalle_data.cantidad

    # Guardar cambios en DB
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def delete_detalle_pedido(db: Session, id_detalle: int):
    logger.info(f"Eliminando detalle {id_detalle}")
    detalle = db.query(models.DetallePedido).filter(models.DetallePedido.id_detalle == id_detalle).first()
    if not detalle:
        logger.warning(f"Detalle {id_detalle} no encontrado")
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    # (Opcional) Devolver stock al producto
    producto = db.query(Producto).filter(Producto.id_producto == detalle.id_producto).first()
    if producto:
        producto.stock += detalle.cantidad
    db.delete(detalle)
    db.commit()
    logger.info(f"Detalle {id_detalle} eliminado correctamente")
    return {"ok": True}

def agregar_detalles_a_pedido(db: Session, pedido_id: int, nuevos_detalles: list):
    logger.info(f"Agregando nuevos detalles al pedido {pedido_id}")
    for detalle in nuevos_detalles:
        producto = db.query(Producto).filter(Producto.id_producto == detalle.id_producto, Producto.stock > 0).first()

        if not producto:
            logger.warning(f"Producto {detalle.id_producto} no encontrado o sin stock")
            raise HTTPException(status_code=404, detail=f"Producto {detalle.id_producto} no encontrado o fuera de stock")
        if producto.stock < detalle.cantidad:
            logger.warning(f"Stock insuficiente para producto {producto.nombre}")
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para el producto: {producto.nombre}")
        producto.stock -= detalle.cantidad
        db_detalle = models.DetallePedido(
            id_pedido=pedido_id,
            id_producto=detalle.id_producto,
            cantidad=detalle.cantidad,
            precio_unitario=producto.precio
        )
        db.add(db_detalle)
        logger.info(f"Detalle agregado: {detalle.cantidad}x {producto.nombre}")
    db.commit()
    logger.info(f"Nuevos detalles agregados al pedido {pedido_id}")
    return {"ok": True}

def update_detalle_pedido(db: Session, id_detalle: int, detalle_update: schemas.DetallePedidoUpdate):
    logger.info(f"Actualizando detalle {id_detalle}")
    detalle = db.query(models.DetallePedido).filter(models.DetallePedido.id_detalle == id_detalle).first()
    if not detalle:
        logger.warning(f"Detalle {id_detalle} no encontrado")
        raise HTTPException(status_code=404, detail="Detalle no encontrado")

    producto = db.query(Producto).filter(Producto.id_producto == detalle.id_producto).first()
    if not producto:
        logger.warning("Producto anterior no encontrado")
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Devolver stock anterior
    producto.stock += detalle.cantidad

    # Si se cambia el producto, buscar el nuevo y ajustar stock
    if detalle_update.id_producto != detalle.id_producto:
        nuevo_producto = db.query(Producto).filter(Producto.id_producto == detalle_update.id_producto).first()
        if not nuevo_producto:
            logger.warning("Nuevo producto no encontrado")
            raise HTTPException(status_code=404, detail="Nuevo producto no encontrado")
        if nuevo_producto.stock < detalle_update.cantidad:
            logger.warning("Stock insuficiente para nuevo producto")
            raise HTTPException(status_code=400, detail="Stock insuficiente para el nuevo producto")
        nuevo_producto.stock -= detalle_update.cantidad
        detalle.id_producto = detalle_update.id_producto
        detalle.cantidad = detalle_update.cantidad
        detalle.precio_unitario = nuevo_producto.precio
    else:
        # Si solo cambia la cantidad
        if producto.stock < detalle_update.cantidad:
            logger.warning("Stock insuficiente al actualizar cantidad")
            raise HTTPException(status_code=400, detail="Stock insuficiente")
        producto.stock -= detalle_update.cantidad
        detalle.cantidad = detalle_update.cantidad

    db.commit()
    db.refresh(detalle)
    logger.info(f"Detalle {id_detalle} actualizado correctamente")
    return detalle

def update_estado_pedido(db: Session, pedido_id: int, estado_update: schemas.PedidoEstadoUpdate):
    logger.info(f"Actualizando estado del pedido {pedido_id}")
    pedido = db.query(models.Pedido).filter(models.Pedido.id_pedido == pedido_id).first()
    if not pedido:
        logger.warning(f"Pedido {pedido_id} no encontrado")
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    pedido.id_estado_pedido = estado_update.id_estado_pedido
    db.commit()
    db.refresh(pedido)
    logger.info(f"Estado del pedido {pedido_id} actualizado correctamente")
    return pedido
