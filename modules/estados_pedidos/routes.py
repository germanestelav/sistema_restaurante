from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, crud
from database.session import get_db
from utils.logger import get_logger

logger = get_logger("estados_pedidos.routes")
router = APIRouter()


@router.post("/", response_model=schemas.EstadoPedido)
def crear_estado_pedido(estado: schemas.EstadoPedidoCreate, db: Session = Depends(get_db)):
    logger.info(f"Creando estado de pedido: {estado}")
    return crud.create_estado_pedido(db, estado)

@router.get("/", response_model=list[schemas.EstadoPedido])
def listar_estados_pedidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Listando estados de pedido: skip={skip}, limit={limit}")
    return crud.get_estados_pedidos(db, skip=skip, limit=limit)

@router.get("/{id_estado_pedido}", response_model=schemas.EstadoPedido)
def obtener_estado_pedido(id_estado_pedido: int, db: Session = Depends(get_db)):
    logger.info(f"Obteniendo estado de pedido con ID: {id_estado_pedido}")
    return crud.get_estado_pedido(db, id_estado_pedido)

@router.put("/{id_estado_pedido}", response_model=schemas.EstadoPedido)
def actualizar_estado_pedido(id_estado_pedido: int, estado: schemas.EstadoPedidoCreate, db: Session = Depends(get_db)):
    logger.info(f"Actualizando estado de pedido con ID: {id_estado_pedido}")
    return crud.update_estado_pedido(db, id_estado_pedido, estado)

@router.delete("/{id_estado_pedido}", response_model=schemas.EstadoPedido)
def eliminar_estado_pedido(id_estado_pedido: int, db: Session = Depends(get_db)):
    logger.info(f"Eliminando estado de pedido con ID: {id_estado_pedido}")
    return crud.delete_estado_pedido(db, id_estado_pedido)