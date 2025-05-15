from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db

router = APIRouter()

# Ruta para crear un detalle de pedido
@router.post("/{id_pedido}", response_model=schemas.DetallePedido)
def crear_detalle_pedido(id_pedido: int, detalle: schemas.DetallePedidoCreate, db: Session = Depends(get_db)):
    return crud.create_detalle_pedido(db=db, detalle=detalle, id_pedido=id_pedido)

@router.get("/", response_model=list[schemas.DetallePedido])
def obtener_detalles_pedidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    detalles = crud.get_detalle_pedidos(db=db, skip=skip, limit=limit)
    if not detalles:
        raise HTTPException(status_code=404, detail="No se encontraron detalles de pedidos")
    return detalles

# Ruta para obtener todos los detalles de un pedido
@router.get("/{id_pedido}", response_model=list[schemas.DetallePedido])
def obtener_detalles_pedido(id_pedido: int, db: Session = Depends(get_db)):
    return crud.get_detalle_pedido(db=db, id_pedido=id_pedido)

# Ruta para actualizar un detalle de pedido
@router.put("/{id_detalle}", response_model=schemas.DetallePedido)
def actualizar_detalle_pedido(id_detalle: int, detalle: schemas.DetallePedidoCreate, db: Session = Depends(get_db)):
    return crud.update_detalle_pedido(db=db, id_detalle=id_detalle, detalle=detalle)

# Ruta para eliminar un detalle de pedido
@router.delete("/{id_detalle}", response_model=schemas.DetallePedido)
def eliminar_detalle_pedido(id_detalle: int, db: Session = Depends(get_db)):
    return crud.delete_detalle_pedido(db=db, id_detalle=id_detalle)
