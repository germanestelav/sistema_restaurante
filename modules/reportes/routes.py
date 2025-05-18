from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modules.consultas.ventas_por_mozo import obtener_ventas_por_mozo
from database.session import get_db

router = APIRouter()

@router.get("/ventas-por-mozo")
def ventas_por_mozo(db: Session = Depends(get_db)):
    """
    Devuelve la cantidad de ventas realizadas por cada mozo.
    """
    return obtener_ventas_por_mozo(db)