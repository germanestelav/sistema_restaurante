from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from database.session import get_db

router = APIRouter()

@router.post("/", response_model=schemas.HistorialDetallePedido)
def create_historial(historial: schemas.HistorialDetallePedidoCreate, db: Session = Depends(get_db)):
    return crud.create_historial(db=db, historial=historial)

@router.get("/", response_model=list[schemas.HistorialDetallePedido])
def read_historiales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_historiales(db=db, skip=skip, limit=limit)

@router.get("/{id_historial}", response_model=schemas.HistorialDetallePedido)
def read_historial(id_historial: int, db: Session = Depends(get_db)):
    return crud.get_historial(db=db, id_historial=id_historial)

@router.put("/{id_historial}", response_model=schemas.HistorialDetallePedido)
def update_historial(id_historial: int, historial: schemas.HistorialDetallePedidoCreate, db: Session = Depends(get_db)):
    return crud.update_historial(db=db, id_historial=id_historial, historial_data=historial)

@router.delete("/{id_historial}", response_model=schemas.HistorialDetallePedido)
def delete_historial(id_historial: int, db: Session = Depends(get_db)):
    return crud.delete_historial(db=db, id_historial=id_historial)
