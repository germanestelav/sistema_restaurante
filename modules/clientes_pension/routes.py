from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db
from utils.logger import get_logger

router = APIRouter()
logger = get_logger("cliente_pension.routes")


@router.post("/", response_model=schemas.ClientePension)
def crear_cliente_pension(cliente: schemas.ClientePensionCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para crear cliente de pensión: {cliente}")
    return crud.create_cliente_pension(db=db, cliente=cliente)

@router.get("/", response_model=list[schemas.ClientePension])
def listar_clientes_pension(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para listar clientes de pensión (skip={skip}, limit={limit})")
    return crud.get_clientes_pension(db=db, skip=skip, limit=limit)

@router.get("/{id_cliente_pension}", response_model=schemas.ClientePension)
def obtener_cliente_pension(id_cliente_pension: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para obtener cliente de pensión ID: {id_cliente_pension}")
    return crud.get_cliente_pension(db=db, id_cliente_pension=id_cliente_pension)

@router.put("/{id_cliente_pension}", response_model=schemas.ClientePension)
def actualizar_cliente_pension(id_cliente_pension: int, cliente: schemas.ClientePensionCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para actualizar cliente de pensión ID: {id_cliente_pension}")
    return crud.update_cliente_pension(db=db, id_cliente_pension=id_cliente_pension, cliente_update=cliente)

@router.delete("/{id_cliente_pension}", response_model=schemas.ClientePension)
def eliminar_cliente_pension(id_cliente_pension: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para eliminar cliente de pensión ID: {id_cliente_pension}")
    return crud.delete_cliente_pension(db=db, id_cliente_pension=id_cliente_pension)