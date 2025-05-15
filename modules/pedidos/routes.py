from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db  # Función que conecta a la base de datos

router = APIRouter()

# Ruta para crear un pedido
@router.post("/", response_model=schemas.Pedido)
def crear_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    return crud.create_pedido(db=db, pedido=pedido)

# Ruta para obtener todos los pedidos
@router.get("/", response_model=list[schemas.Pedido])
def leer_pedidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_pedidos(db=db, skip=skip, limit=limit)

# Ruta para obtener un pedido por ID
@router.get("/{pedido_id}", response_model=schemas.Pedido)
def leer_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = crud.get_pedido(db=db, pedido_id=pedido_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido

# Ruta para actualizar un pedido
@router.put("/{pedido_id}", response_model=schemas.Pedido)
def actualizar_pedido(pedido_id: int, pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    db_pedido = crud.update_pedido(db=db, pedido_id=pedido_id, pedido=pedido)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido

# Ruta para eliminar un pedido
@router.delete("/{pedido_id}", response_model=schemas.Pedido)
def eliminar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = crud.delete_pedido(db=db, pedido_id=pedido_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido
