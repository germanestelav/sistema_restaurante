from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db
from modules.permisos.dependencias import permiso_requerido
from modules.auth.dependencias import get_current_user
from typing import List
from utils.logger import get_logger

logger = get_logger("pedidos.routes")

router = APIRouter()

# Ruta para crear un pedido
@router.post("/", response_model=schemas.Pedido, dependencies=[permiso_requerido(["Mozo", "Administrador"])])
def crear_pedido(
    pedido: schemas.PedidoCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    logger.info(f"Creando pedido para usuario {user.id_usuario} con datos: {pedido}")
    resultado = crud.create_pedido(db=db, pedido=pedido, id_usuario=user.id_usuario)
    logger.info(f"Pedido creado con ID: {resultado.id_pedido}")
    return resultado

# Ruta para obtener todos los pedidos
@router.get("/", response_model=List[schemas.Pedido])
def leer_pedidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Obteniendo pedidos con skip={skip} y limit={limit}")
    resultado = crud.get_pedidos(db=db, skip=skip, limit=limit)
    logger.info(f"Se obtuvieron {len(resultado)} pedidos")
    return resultado

# Ruta para obtener un pedido por ID
@router.get("/{pedido_id}", response_model=schemas.Pedido)
def leer_pedido(pedido_id: int, db: Session = Depends(get_db)):
    logger.info(f"Buscando pedido con ID: {pedido_id}")
    db_pedido = crud.get_pedido(db=db, pedido_id=pedido_id)
    if db_pedido is None:
        logger.warning(f"Pedido con ID {pedido_id} no encontrado")
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    logger.info(f"Pedido encontrado: id={db_pedido.id_pedido}, mesa={db_pedido.id_mesa}, usuario={db_pedido.id_usuario}")
    return db_pedido

# Ruta para actualizar un pedido (y sus detalles)
@router.put("/{pedido_id}", response_model=schemas.Pedido)
def actualizar_pedido(pedido_id: int, pedido: schemas.PedidoUpdate, db: Session = Depends(get_db)):
    logger.info(f"Actualizando pedido ID {pedido_id} con datos: {pedido}")
    resultado = crud.update_pedido_con_detalles(db, pedido_id, pedido)
    logger.info(f"Pedido ID {pedido_id} actualizado")
    return resultado

# Ruta para eliminar un pedido
@router.delete("/{pedido_id}", response_model=schemas.Pedido)
def eliminar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    logger.info(f"Eliminando pedido ID {pedido_id}")
    resultado = crud.delete_pedido(db=db, pedido_id=pedido_id)
    if resultado is None:
        logger.warning(f"No se encontró pedido con ID {pedido_id} para eliminar")
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    logger.info(f"Pedido ID {pedido_id} eliminado")
    return resultado

# Ruta para eliminar un detalle de pedido
@router.delete("/detalles/{id_detalle}")
def eliminar_detalle_pedido(id_detalle: int, db: Session = Depends(get_db)):
    logger.info(f"Eliminando detalle pedido ID {id_detalle}")
    resultado = crud.delete_detalle_pedido(db, id_detalle)
    logger.info(f"Detalle pedido ID {id_detalle} eliminado")
    return resultado

# Ruta para agregar productos (detalles) a un pedido existente
@router.post("/pedidos/{pedido_id}/agregar-detalles")
def agregar_detalles(pedido_id: int, detalles: List[schemas.DetallePedidoCreate], db: Session = Depends(get_db)):
    logger.info(f"Agregando detalles a pedido ID {pedido_id}")
    resultado = crud.agregar_detalles_a_pedido(db, pedido_id, detalles)
    logger.info(f"Detalles agregados a pedido ID {pedido_id}")
    return resultado

# Ruta para actualizar un detalle de pedido
@router.put("/detalles/{id_detalle}", response_model=schemas.DetallePedido)
def editar_detalle_pedido(id_detalle: int, detalle: schemas.DetallePedidoUpdate, db: Session = Depends(get_db)):
    logger.info(f"Actualizando detalle pedido ID {id_detalle} con datos: {detalle}")
    resultado = crud.update_detalle_pedido(db, id_detalle, detalle)
    logger.info(f"Detalle pedido ID {id_detalle} actualizado")
    return resultado

# Ruta para actualizar solo el estado del pedido
@router.put("/estado/{pedido_id}", response_model=schemas.Pedido)
def actualizar_estado_pedido(pedido_id: int, estado: schemas.PedidoEstadoUpdate, db: Session = Depends(get_db)):
    logger.info(f"Actualizando estado del pedido ID {pedido_id} a: {estado}")
    resultado = crud.update_estado_pedido(db, pedido_id, estado)
    logger.info(f"Estado del pedido ID {pedido_id} actualizado")
    return resultado